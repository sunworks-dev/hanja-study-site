#!/usr/bin/env python3
"""Render the 32-second kinetic product film from genuine Phi app captures.

Usage: python scripts/build-product-film.py /tmp/hanja-film --out /tmp/hanja-motion
       add --boards for representative frames only; --orientation portrait/landscape.
Requires Pillow, numpy, opencv-python-headless, ffmpeg. No browser renderer.
"""
from pathlib import Path
from functools import lru_cache
import argparse, bisect, json, math, os, subprocess, time, wave
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(); parser.add_argument('captures',type=Path);parser.add_argument('--out',type=Path,default=Path('/tmp/hanja-motion'));parser.add_argument('--boards',action='store_true');parser.add_argument('--orientation',choices=['landscape','portrait']);args=parser.parse_args()
RAW=args.captures.resolve(); OUT=args.out.resolve();OUT.mkdir(parents=True,exist_ok=True)
FONT=ROOT.parent.parent/'apps/hanja-study-app/flutter_app/assets/fonts'
ASSETS=ROOT/'public/assets'
COLORS={'paper':'#fff9ed','ink':'#233f35','orange':'#be411f','mint':'#dfead5','yellow':'#f7d681','white':'#fffef9'}
S=1.5; FPS=30; DURATION=32
CUTS=[0,2,4,7,10,13,17,21,25,28,32]
FRAMES={k:json.loads((RAW/k/'frames.json').read_text()) for k in ['recall','strokes','story','collection']}
TIMES={k:[f['t'] for f in v] for k,v in FRAMES.items()}
cv2.setNumThreads(2)

def clamp(t):return min(max(t,0),1)
def ease(t):return 1-(1-clamp(t))**4
def smooth(t):t=clamp(t);return t*t*(3-2*t)
def lerp(a,b,t):return a+(b-a)*t
def rgb(color):return tuple(bytes.fromhex(COLORS.get(color,color).lstrip('#')))
def mix(a,b,t):return tuple(round(lerp(x,y,t)) for x,y in zip(rgb(a),rgb(b)))
def source(clip,t):return FRAMES[clip][min(bisect.bisect_right(TIMES[clip],t)-1,len(FRAMES[clip])-1)]['file']

@lru_cache(maxsize=180)
def font(size,kind='display'):
 path=RAW/'Jua-Regular.ttf' if kind=='display' else FONT/('NotoSerifKR-SemiBold.otf' if kind=='hanja' else 'Pretendard-Bold.otf' if kind=='bold' else 'Pretendard-Regular.otf')
 return ImageFont.truetype(str(path),round(size*S))

@lru_cache(maxsize=300)
def text_sprite(text,size,color='ink',kind='display'):
 f=font(size,kind); box=f.getbbox(text); margin=round(5*S)
 im=Image.new('RGBA',(box[2]-box[0]+margin*2,box[3]-box[1]+margin*2))
 ImageDraw.Draw(im).text((margin-box[0],margin-box[1]),text,font=f,fill=rgb(color))
 return im

@lru_cache(maxsize=60)
def picture(path):return Image.open(path).convert('RGBA')

@lru_cache(maxsize=40)
def phone_texture(path):
 # Generic device hardware surrounds the unmodified real app screen.
 p=40; w,h=450,900
 mask=Image.new('L',(w,h));ImageDraw.Draw(mask).rounded_rectangle((0,0,w-1,h-1),radius=44,fill=255)
 shadow=Image.new('RGBA',(w+p*2,h+p*2)); alpha=Image.new('L',shadow.size)
 alpha.paste(mask,(p,p+12));alpha=alpha.filter(ImageFilter.GaussianBlur(17));alpha=alpha.point(lambda x:int(x*.2));shadow.putalpha(alpha)
 d=ImageDraw.Draw(shadow);d.rounded_rectangle((p,p,p+w-1,p+h-1),radius=44,fill='#10281f')
 d.rounded_rectangle((p+3,p+3,p+w-4,p+h-4),radius=42,outline='#8d9f94',width=3)
 screen=picture(path).resize((420,840),Image.Resampling.LANCZOS)
 sm=Image.new('L',screen.size);ImageDraw.Draw(sm).rounded_rectangle((0,0,419,839),radius=26,fill=255)
 shadow.paste(screen,(p+15,p+30),sm)
 d.line((p+60,p+8,p+w-60,p+8),fill='#b4bdb3',width=2)
 d.rounded_rectangle((p+166,p+h-17,p+284,p+h-13),radius=2,fill='#73877b')
 return np.asarray(shadow)

class Frame:
 def __init__(self,portrait,bg):
  self.bg=bg;self.p=portrait;self.w,self.h=(720,1280) if portrait else (1280,720)
  self.im=Image.new('RGBA',(round(self.w*S),round(self.h*S)),rgb(bg))
 def rect(self,box,color,radius=0,alpha=255):
  layer=Image.new('RGBA',self.im.size);d=ImageDraw.Draw(layer);b=tuple(round(v*S) for v in box)
  d.rounded_rectangle(b,radius=round(radius*S),fill=(*rgb(color),alpha));self.im.alpha_composite(layer)
 def circle(self,x,y,r,color,alpha=255,outline=False):
  layer=Image.new('RGBA',self.im.size);d=ImageDraw.Draw(layer);box=((x-r)*S,(y-r)*S,(x+r)*S,(y+r)*S)
  d.ellipse(box,outline=(*rgb(color),alpha) if outline else None,fill=None if outline else (*rgb(color),alpha),width=round(2*S));self.im.alpha_composite(layer)
 def stamp(self,img,x,y,width=None,angle=0,opacity=1,squash=1):
  if opacity<=0:return
  if width is not None:
   w=max(1,round(width*S));img=img.resize((w,max(1,round(img.height*w/img.width*squash))),Image.Resampling.BICUBIC)
  if abs(angle)>.01:img=img.rotate(angle,Image.Resampling.BICUBIC,expand=True)
  if opacity<.999:img=img.copy();img.putalpha(img.getchannel('A').point(lambda a:round(a*clamp(opacity))))
  self.im.alpha_composite(img,(round(x*S-img.width/2),round(y*S-img.height/2)))
 def text(self,text,x,y,size=64,color='ink',kind='display',align='left',enter=1,angle=0,zoom=1):
  img=text_sprite(text,size,color,kind);progress=ease(enter)
  if zoom!=1:img=img.resize((round(img.width*zoom),round(img.height*zoom)),Image.Resampling.BICUBIC)
  # Actual vertical masking, not a generic dissolve.
  if progress<1:
   shifted=Image.new('RGBA',img.size);shifted.alpha_composite(img,(0,round(img.height*(1-progress))));img=shifted
  cx=x if align=='center' else x+img.width/S/2
  self.stamp(img,cx,y+img.height/S/2,angle=angle)
 def line(self,points,color,width=2,alpha=255):
  layer=Image.new('RGBA',self.im.size);ImageDraw.Draw(layer).line([(x*S,y*S) for x,y in points],fill=(*rgb(color),alpha),width=round(width*S),joint='curve');self.im.alpha_composite(layer)
 def phone(self,path,x,y,height,yaw=0,pitch=0,roll=0,opacity=1):
  tex=phone_texture(str(path));th,tw=tex.shape[:2];w=height*tw/th;h=height
  pts=np.array([[-w/2,-h/2,0],[w/2,-h/2,0],[w/2,h/2,0],[-w/2,h/2,0]],np.float32)
  a,b,c=np.radians([yaw,pitch,roll]);ry=np.array([[np.cos(a),0,np.sin(a)],[0,1,0],[-np.sin(a),0,np.cos(a)]])
  rx=np.array([[1,0,0],[0,np.cos(b),-np.sin(b)],[0,np.sin(b),np.cos(b)]]);rz=np.array([[np.cos(c),-np.sin(c),0],[np.sin(c),np.cos(c),0],[0,0,1]])
  pts=pts@(rz@rx@ry).T;persp=1400/(1400+pts[:,2]);dest=np.column_stack([pts[:,0]*persp+x,pts[:,1]*persp+y])*S
  lo=np.floor(dest.min(axis=0)).astype(int);hi=np.ceil(dest.max(axis=0)).astype(int)
  if hi[0]<0 or hi[1]<0 or lo[0]>=self.im.width or lo[1]>=self.im.height:return
  matrix=cv2.getPerspectiveTransform(np.float32([[0,0],[tw-1,0],[tw-1,th-1],[0,th-1]]),np.float32(dest-lo))
  warp=cv2.warpPerspective(tex,matrix,tuple(hi-lo),flags=cv2.INTER_LINEAR)
  if opacity<1:warp[:,:,3]=(warp[:,:,3]*opacity).astype(np.uint8)
  self.im.alpha_composite(Image.fromarray(warp),(int(lo[0]),int(lo[1])))
 def character(self,name,x,y,width,t,delay=0,angle=0):
  q=ease((t-delay)/.65);lift=(1-q)*220
  self.stamp(picture(ASSETS/f'{name}.webp'),x,y+lift,width*(.86+.14*q),angle+2*math.sin(t*2),opacity=q,squash=1+.025*math.sin(t*3))
 def footer(self,dark=False):
  self.rect((0,self.h-42,self.w,self.h),self.bg)
  self.text('실제 웹 베타 화면 · 일부 재생 속도 편집',30,self.h-32,20 if self.p else 14,'paper' if dark else 'muted',kind='body')

# A local muted color, same source palette role.
COLORS['muted']='#57655a'

def scene(index,s,p):
 bg=['paper','orange','ink','yellow','paper','ink','orange','paper','yellow','ink'][index];f=Frame(p,bg);w,h=f.w,f.h
 if index==0:
  for j,(ch,x,y) in enumerate([('日',.13,.19),('月',.86,.78)]):f.text(ch,w*x,h*y,210,'mint','hanja',align='center',angle=(-12 if j==0 else 10)+s*2)
  f.text('한자 공부,',w/2,h*.37,116 if p else 148,align='center',enter=s/.65,zoom=1+.03*s)
  f.text('우리말을 만나는 새로운 리듬',w/2,h*.61,25 if p else 29,'ink','body',align='center',enter=(s-.65)/.5)
  f.rect((w*.21,h*.57,w*.21+w*.58*ease((s-.5)/.7),h*.58),'orange',4)
 elif index==1:
  f.text('어흥',w/2,h*.27,178 if p else 208,'paper',align='center',enter=s/.4,angle=-3)
  f.text('하게.',w/2,h*.49,168 if p else 186,'paper',align='center',enter=(s-.25)/.4,angle=2)
  f.character('horang-welcome',w*(.78 if p else .85),h*.76,230 if p else 275,s,.2,-8)
  f.text('한 글자부터 신나게.',w*.1,h*.84,27,'paper','bold',enter=(s-.65)/.5)
 elif index==2:
  f.text('한 글자에,',w/2,74 if p else 25,76 if p else 48,'paper',align='center',enter=s/.5)
  if p:f.text('이 모든 걸.',w/2,160,76,'yellow',align='center',enter=(s-.1)/.5)
  else:f.text('이 모든 걸.',w/2+250,30,48,'yellow',align='center',enter=(s-.1)/.5)
  q=ease(s/.9);cy=800 if p else 415
  f.phone(RAW/'story-screen.png',lerp(-200,w*.21,q),cy+30,680 if p else 520,yaw=18,roll=-12+2*math.sin(s))
  f.phone(RAW/'collection-screen.png',lerp(w+200,w*.79,q),cy,680 if p else 520,yaw=-18,roll=12-2*math.sin(s))
  f.phone(RAW/'study-screen.png',w/2,lerp(h+450,cy,ease((s-.16)/.9)),900 if p else 650,yaw=lerp(-28,7,smooth(s/3)),pitch=-3,roll=lerp(-7,3,smooth(s/3)))
  f.footer(True)
 elif index==3:
  if p:
   f.text('먼저,',48,98,84,enter=s/.45);f.text('떠올려요.',48,192,84,enter=(s-.12)/.45)
   x,y,ph=w/2,835,850
  else:
   f.text('먼저,',80,180,99,enter=s/.45);f.text('떠올려요.',80,286,99,enter=(s-.12)/.45);x,y,ph=920,365,700
  f.phone(source('recall',min(s*1.9,6.9)),x+(1-ease(s/.65))*230,y,ph,yaw=lerp(25,-5,smooth(s/3)),roll=lerp(9,-3,smooth(s/3)))
  f.text('정답을 보기 전, 나의 생각부터.',48 if p else 86,340 if p else 452,24,'ink','body',enter=(s-.5)/.5)
  f.footer()
 elif index==4:
  f.text('한 글자가,',48 if p else 78,90 if p else 55,68 if p else 75,enter=s/.5)
  f.text('아는 낱말로.',48 if p else 78,177 if p else 138,68 if p else 75,'orange',enter=(s-.14)/.5)
  cx,cy=(w/2,485) if p else (330,430)
  f.text('校',cx,cy-170,270,'orange','hanja',align='center',enter=(s-.1)/.7,angle=-6+2*s)
  words=[('學校','학교'),('大學校','대학교'),('中學校','중학교')]
  for j,(hanja,ko) in enumerate(words):
   q=ease((s-.4-j*.18)/.6);xx=48 if p else 675;yy=(700+j*142) if p else (300+j*118)
   f.rect((xx+(1-q)*80,yy,xx+(1-q)*80+(624 if p else 500),yy+108),'mint' if j%2==0 else 'yellow',16,round(q*255))
   f.text(hanja,xx+28+(1-q)*80,yy+19,48,'ink','hanja',enter=(s-.4-j*.18)/.5)
   f.text(ko,xx+(430 if p else 340)+(1-q)*80,yy+34,28,'ink','bold',enter=(s-.4-j*.18)/.5)
  f.footer()
 elif index==5:
  f.text('획순을 따라.',48 if p else 80,90 if p else 142,70 if p else 76,'paper',enter=s/.55)
  f.text('뜻까지 연결.',48 if p else 80,180 if p else 230,70 if p else 76,'yellow',enter=(s-.16)/.55)
  q=smooth(s/3.8);x,y,ph=(w/2,850,880) if p else (930,380,710)
  f.phone(source('strokes',s*1.9),x+lerp(50,0,q),y+lerp(150,0,q),ph*lerp(1.25,1,q),yaw=lerp(-14,8,q),pitch=lerp(10,0,q),roll=lerp(-6,2,q))
  f.text('모양 · 훈음 · 연상 · 연결 어휘',48 if p else 86,305 if p else 374,23,'mint','body',enter=(s-.6)/.6)
  if not p:f.character('horang-writing',240,565,260,s,.45,-5)
  f.footer(True)
 elif index==6:
  if p:
   f.text('이야기',w/2,72,100,'paper',align='center',enter=s/.5)
   f.text('속으로.',w/2,180,100,'yellow',align='center',enter=(s-.1)/.5)
  else:f.text('이야기 속으로.',w/2,32,78,'paper',align='center',enter=s/.5)
  if p:
   f.phone(source('story',s*1.7),w/2,835+(1-ease(s/.7))*180,890,yaw=lerp(-18,5,smooth(s/4)),roll=lerp(-9,2,smooth(s/4)))
  else:
   f.phone(RAW/'stories-screen.png',360,435,560,yaw=18,roll=-10,opacity=.88)
   f.phone(source('story',s*1.7),850,430+(1-ease(s/.7))*250,595,yaw=lerp(-20,4,smooth(s/4)),roll=lerp(12,-2,smooth(s/4)))
   f.character('horang-reading',585,578,235,s,.55)
  f.footer(True)
 elif index==7:
  # Content tiles establish the collection, then let the actual collection lead.
  for row in range(4):
   for col,ch in enumerate('學校日月山水'):
    xx=col*210-80+(s*16 if row%2==0 else -s*16); yy=row*225-50
    f.text(ch,xx,yy,150,'mint','hanja',angle=-6)
  f.text('한 글자씩,',48 if p else 65,95 if p else 135,78 if p else 85,enter=s/.5)
  f.text('나의 도감으로.',48 if p else 65,191 if p else 230,70 if p else 80,'orange',enter=(s-.15)/.5)
  x,y,ph=(w/2,840,890) if p else (938,365,725)
  f.phone(source('collection',s*1.75),x,y+lerp(160,0,ease(s/.85)),ph,yaw=lerp(25,-5,smooth(s/4)),roll=lerp(10,-3,smooth(s/4)))
  if not p:
   f.text('읽기 · 뜻 · 쓰기 · 부수',72,382,29,'ink','bold',enter=(s-.65)/.5)
   f.text('배운 흔적을 한눈에.',72,435,27,'muted','body',enter=(s-.8)/.5)
  f.footer()
 elif index==8:
  f.text('매일 만나고 싶은',w/2,110 if p else 54,60 if p else 80,align='center',enter=s/.5)
  f.text('한자 공부.',w/2,190 if p else 149,104 if p else 110,'orange',align='center',enter=(s-.16)/.5)
  if p:
   positions=[('ttotto',120,550,220),('gureumi',590,590,230),('waewae',160,1020,240),('atcha',570,1060,225),('horang-celebrate',360,815,485)]
  else:positions=[('ttotto',150,490,240),('gureumi',380,487,235),('waewae',905,485,240),('atcha',1130,490,230),('horang-celebrate',640,492,355)]
  for j,(name,x,y,size) in enumerate(positions):f.character(name,x,y,size,s,.12+j*.11,(-1)**j*5)
  f.text('오늘도, 한 글자 더.',w/2,h-82,28,'ink','bold',align='center',enter=(s-1)/.5)
 elif index==9:
  if p:
   f.text('한 글자에서,',w/2,88,74,'paper',align='center',enter=s/.6)
   f.text('말의 힘으로.',w/2,175,74,'paper',align='center',enter=(s-.12)/.6)
   f.text('어흥!한자',w/2,305,104,'yellow',align='center',enter=(s-.3)/.6)
   f.phone(RAW/'recall-screen.png',225,794,600,yaw=15,roll=-12)
   f.phone(RAW/'study-screen.png',460,789,650,yaw=-12+2*math.sin(s),roll=7)
   f.rect((70,1118,650,1190),'orange',16);f.text('웹에서 먼저 만나보세요',w/2,1139,30,'paper','bold',align='center',enter=(s-.7)/.5)
   f.text('hanja-app.sunw.kr',w/2,1222,24,'mint','body',align='center')
  else:
   f.text('한 글자에서,',78,112,70,'paper',enter=s/.6)
   f.text('말의 힘으로.',78,194,70,'paper',enter=(s-.12)/.6)
   f.text('어흥!한자',78,326,115,'yellow',enter=(s-.3)/.6)
   f.rect((82,518,549,586),'orange',16);f.text('웹에서 먼저 만나보세요',314,537,28,'paper','bold',align='center',enter=(s-.7)/.5)
   f.text('hanja-app.sunw.kr',84,621,24,'mint','body')
   f.phone(RAW/'recall-screen.png',842,375,565,yaw=17,roll=-13)
   f.phone(RAW/'study-screen.png',1050,365,685,yaw=-15+2*math.sin(s),roll=7)
 return f


def render(t,p):
 index=min(bisect.bisect_right(CUTS,t)-1,9);s=t-CUTS[index];f=scene(index,s,p)
 # A fast editorial wipe gives direction at scene changes; never fade between slides.
 if index>0 and s<.24:
  progress=ease(s/.24);colors=['paper','orange','ink','yellow','paper','ink','orange','paper','yellow','ink']
  f.rect((0,0,f.w*(1-progress),f.h),colors[index-1])
 return f.im.convert('RGB')


def soundtrack():
 sr=48000;n=int(DURATION*sr);audio=np.zeros((n,2),np.float64);rng=np.random.default_rng(20261003)
 def add(sig,start,pan=0,gain=1):
  offset=int(start*sr)
  if offset>=n:return
  if offset<0:sig=sig[-offset:];offset=0
  count=min(len(sig),n-offset);audio[offset:offset+count,0]+=sig[:count]*gain*math.sqrt((1-pan)/2);audio[offset:offset+count,1]+=sig[:count]*gain*math.sqrt((1+pan)/2)
 def noise(seconds):
  x=rng.normal(0,1,int(seconds*sr));return x
 chords=[[48,55,60,64,67],[45,52,57,60,64],[41,48,53,57,60],[43,50,55,59,62]]
 for beat in range(64):
  at=beat*.5
  # Rounded electronic kick and tight backbeat, 120 BPM.
  t=np.arange(int(.32*sr))/sr;phase=2*np.pi*(48*t+70*.035*(1-np.exp(-t/.035)))
  add(np.sin(phase)*np.exp(-t*17)*(1-np.exp(-t*550)),at,gain=.42)
  if beat%2:
   t=np.arange(int(.16*sr))/sr;x=noise(.16);hp=np.r_[0,np.diff(x)];add(hp*np.exp(-t*38)*(1-np.exp(-t*900)),at,pan=.12,gain=.06)
  for sub in [0,.25]:
   t=np.arange(int(.045*sr))/sr;x=noise(.045);add(np.r_[0,np.diff(x)]*np.exp(-t*95),at+sub,pan=-.36 if sub==0 else .35,gain=.021)
  chord=chords[(beat//4)%4];root=chord[0]-12
  t=np.arange(int(.44*sr))/sr;hz=440*2**((root-69)/12);bass=(np.sin(2*np.pi*hz*t)+.16*np.sin(4*np.pi*hz*t))*np.exp(-t*7)*np.minimum(t/.012,1)
  add(bass,at,gain=.22)
  if beat%2==0:
   t=np.arange(int(.8*sr))/sr;tone=np.zeros(len(t))
   for note in chord[1:]:
    hz=440*2**((note-69)/12);tone+=np.sin(2*np.pi*hz*t+.5*np.sin(2*np.pi*hz*2*t))
   tone=tone/4*np.minimum(t/.014,1)*np.exp(-t*4.4);add(tone,at+.25,pan=-.2,gain=.105)
  melody=[0,2,3,4,2,1,3,2]
  note=chord[melody[beat%8]%len(chord)]+12;t=np.arange(int(.62*sr))/sr;hz=440*2**((note-69)/12)
  bell=(np.sin(2*np.pi*hz*t)+.22*np.sin(2*np.pi*hz*3*t))*np.exp(-t*8)*np.minimum(t/.008,1)
  add(bell,at+.125,pan=.24,gain=.074);add(bell,at+.375,pan=-.24,gain=.022)
 for cut in CUTS[1:-1]:
  t=np.arange(int(.36*sr))/sr;x=noise(.36);kernel=np.ones(12)/12;soft=np.convolve(x,kernel,'same');env=np.sin(np.pi*t/.36)**1.8
  add(soft*env,cut-.27,pan=-.3,gain=.16)
  t=np.arange(int(.4*sr))/sr;ping=np.sin(2*np.pi*(880*t+90*t*t))*np.exp(-t*15)*np.minimum(t/.005,1);add(ping,cut,pan=.28,gain=.07)
 fade=np.minimum(np.arange(n)/sr/.06,1)*np.clip((DURATION-np.arange(n)/sr)/.85,0,1);audio*=fade[:,None]
 audio=np.tanh(audio*1.5);audio*=.88/max(np.max(np.abs(audio)),.001)
 path=OUT/'motion-score.wav'
 with wave.open(str(path),'wb') as stream:stream.setnchannels(2);stream.setsampwidth(2);stream.setframerate(sr);stream.writeframes((audio*32767).astype('<i2').tobytes())
 return path


def main():
 print(json.dumps({'pid':os.getpid(),'ppid':os.getppid(),'started':time.time(),'task':'hanja-motion-render'}),flush=True)
 tags=[args.orientation] if args.orientation else ['landscape','portrait']
 if args.boards:
  for tag in tags:
   for t in [.9,2.9,5.8,8.4,11.5,15.6,19.4,23.3,26.6,30.4]:render(t,tag=='portrait').save(OUT/f'{tag}-{t:04.1f}.jpg',quality=94)
  print('Storyboards rendered',flush=True);return
 audio=soundtrack()
 for tag in tags:
  p=tag=='portrait';width,height=(1080,1920) if p else (1920,1080);silent=OUT/f'{tag}-silent.mp4'
  proc=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{width}x{height}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(silent)],stdin=subprocess.PIPE)
  print(json.dumps({'encoder_pid':proc.pid,'parent':os.getpid(),'started':time.time(),'orientation':tag}),flush=True)
  try:
   for i in range(DURATION*FPS):
    proc.stdin.write(render(i/FPS,p).tobytes())
    if i%(FPS*4)==0:print(f'{tag} {i/FPS:.0f}/{DURATION}s',flush=True)
  finally:proc.stdin.close()
  if proc.wait()!=0:raise RuntimeError('Video encoding failed')
  output=OUT/f'hanja-motion-{tag}.mp4'
  subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(silent),'-i',str(audio),'-map','0:v','-map','1:a','-c:v','copy','-af','loudnorm=I=-16:TP=-1.5:LRA=9','-c:a','aac','-b:a','160k','-t','32','-movflags','+faststart',str(output)],check=True)
  render(5.8,p).save(OUT/f'poster-motion-{tag}.webp',quality=90)
  print(f'{output.name}: {output.stat().st_size/1024/1024:.2f} MiB',flush=True)
if __name__=='__main__':main()
