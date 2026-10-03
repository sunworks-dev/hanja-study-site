#!/usr/bin/env python3
"""Compose the product film from real Phi captures, never simulated app UI.

Usage: python scripts/build-product-film.py /tmp/hanja-film
Requires Pillow, numpy, fontTools, ffmpeg. Input folders contain capture.ffconcat.
"""
import json
import math
from pathlib import Path
import subprocess
import sys
import wave
from urllib.request import urlretrieve

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
RAW = Path(sys.argv[1]).resolve()
OUT = ROOT / 'public/assets/video'
OUT.mkdir(parents=True, exist_ok=True)
APP_FONTS = ROOT.parent.parent / 'apps/hanja-study-app/flutter_app/assets/fonts'
JUA = RAW / 'Jua-Regular.ttf'
if not JUA.exists():
    urlretrieve('https://raw.githubusercontent.com/google/fonts/main/ofl/jua/Jua-Regular.ttf', JUA)
BODY = APP_FONTS / 'Pretendard-Regular.otf'
BOLD = APP_FONTS / 'Pretendard-Bold.otf'

SCENES = [
    ('intro', 3.0, '한 글자에서,\n말의 힘으로.', '우리말이 더 선명해지는 한자 공부.', 'home-screen.png', '#fff9ed', '#233f35'),
    ('recall', 7.5, '보기 전에,\n먼저 떠올려요.', '맞혀 보고, 뜻을 연결하며 익혀요.', None, '#233f35', '#fff9ed'),
    ('strokes', 8.5, '모양은 손끝에.\n뜻은 머릿속에.', '획순과 연상, 연결된 단어까지.', None, '#f7d681', '#233f35'),
    ('story', 7.5, '다음 이야기가\n궁금한 공부.', '빈칸을 채우면 이야기가 이어져요.', None, '#233f35', '#fff9ed'),
    ('collection', 7.5, '한 글자씩 쌓이는\n나의 한자 도감.', '읽기·뜻·쓰기·부수, 배운 흔적을 확인해요.', None, '#dfead5', '#233f35'),
    ('outro', 4.0, '오늘, 한 글자와\n친해져 볼까요?', '어흥!한자 · 웹에서 먼저 만나 보세요.', 'study-screen.png', '#fff9ed', '#233f35'),
]
TOTAL = sum(s[1] for s in SCENES) - .4 * (len(SCENES) - 1)


def run(args):
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', *args], check=True)


def plate(scene, portrait):
    name, _, title, subtitle, _, background, ink = scene
    w, h = (720, 1280) if portrait else (1280, 720)
    image = Image.new('RGB', (w, h), background)
    d = ImageDraw.Draw(image)
    if portrait:
        d.text((48, 34), '어흥!한자', font=ImageFont.truetype(str(JUA), 28), fill=ink)
        d.multiline_text((48, 88), title, font=ImageFont.truetype(str(JUA), 57), fill=ink, spacing=2)
        d.text((48, 232), subtitle, font=ImageFont.truetype(str(BODY), 22), fill=ink)
        d.text((48, 1234), '실제 웹 베타 시연 · 화면과 기능은 달라질 수 있어요', font=ImageFont.truetype(str(BODY), 17), fill=ink)
        box = (140, 320, 580, 1200)
    else:
        icon = Image.open(ROOT / 'public/assets/hanja-icon.webp').convert('RGBA').resize((44, 44))
        image.paste(icon, (65, 47), icon)
        d.text((122, 51), '어흥!한자', font=ImageFont.truetype(str(JUA), 30), fill=ink)
        d.multiline_text((64, 222), title, font=ImageFont.truetype(str(JUA), 68), fill=ink, spacing=5)
        d.text((66, 410), subtitle, font=ImageFont.truetype(str(BODY), 25), fill=ink)
        d.line((66, 478, 585, 478), fill=ink, width=1)
        character = Image.open(ROOT / 'public/assets/horang-reading.webp').convert('RGBA').resize((142, 142))
        image.paste(character, (62, 500), character)
        d.text((218, 550), '연결하고. 직접 쓰고. 다시 떠올리고.', font=ImageFont.truetype(str(BODY), 19), fill=ink)
        d.text((66, 672), '실제 웹 베타 시연 · 화면과 기능은 달라질 수 있어요', font=ImageFont.truetype(str(BODY), 16), fill=ink)
        box = (815, 50, 1115, 650)
    # A simple device edge frames the real screen without inventing its content.
    x, y, xx, yy = box
    d.rounded_rectangle((x-8, y-8, xx+8, yy+8), radius=20, fill='#172c25')
    filename = RAW / f'{name}-{w}.png'
    image.save(filename)
    return filename, box


def music():
    """An original, quiet marimba-like score; no stock or sampled music."""
    sr = 44100
    samples = np.zeros(int((TOTAL + .5) * sr), dtype=np.float64)
    melody = [67, 71, 74, 79, 76, 74, 71, 69, 67, 74, 76, 79, 81, 79, 74, 71]
    for i in range(math.ceil(TOTAL / .48)):
        start = i * .48
        n = int(1.6 * sr)
        t = np.arange(n) / sr
        freq = 440 * 2 ** ((melody[i % len(melody)] - 69) / 12)
        tone = (np.sin(2*np.pi*freq*t) + .23*np.sin(2*np.pi*freq*2*t)) * np.exp(-t*4.3)
        tone *= np.minimum(t/.012, 1) * .075
        index = int(start * sr)
        end = min(index+n, len(samples))
        samples[index:end] += tone[:end-index]
    for i, note in enumerate([43, 48, 40, 45] * 5):
        start = i * 1.92
        if start >= TOTAL:
            break
        t = np.arange(int(2.4*sr)) / sr
        tone = np.sin(2*np.pi*(440*2**((note-69)/12))*t) * np.exp(-t*1.7) * .04
        tone *= np.minimum(t/.06, 1)
        index = int(start*sr)
        end = min(index+len(tone),len(samples))
        samples[index:end] += tone[:end-index]
    t = np.arange(len(samples))/sr
    samples *= np.minimum(t/.7,1) * np.clip((TOTAL-t)/1.6,0,1)
    audio = RAW/'score.wav'
    with wave.open(str(audio),'wb') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(sr)
        f.writeframes((np.clip(samples,-1,1)*32767).astype('<i2').tobytes())
    return audio


audio = music()
for portrait in (False, True):
    tag = 'portrait' if portrait else 'landscape'
    scenes = []
    for scene in SCENES:
        name, duration, _, _, still, _, _ = scene
        background, (x, y, xx, yy) = plate(scene, portrait)
        output = RAW/f'{tag}-{name}.mp4'
        source = ['-loop','1','-framerate','30','-i',str(RAW/still)] if still else ['-safe','0','-f','concat','-i',str(RAW/name/'capture.ffconcat')]
        # Screen eases into its final position; all interaction pixels are recorded.
        graph = f'[1:v]scale={xx-x}:{yy-y}:flags=lanczos,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=2[screen];[0:v][screen]overlay=x={x}:y=\'{y}+14*exp(-5*t)\':shortest=1,format=yuv420p[v]'
        run(['-loop','1','-framerate','30','-i',str(background),*source,'-filter_complex',graph,'-map','[v]','-t',str(duration),'-an','-c:v','libx264','-preset','fast','-crf','19',str(output)])
        scenes.append(output)
    inputs=[]
    for s in scenes: inputs += ['-i',str(s)]
    filters=[]
    prior='0:v'; offset=SCENES[0][1]-.4
    for i in range(1,len(scenes)):
        filters.append(f'[{prior}][{i}:v]xfade=transition=fade:duration=0.4:offset={offset:.3f}[v{i}]')
        prior=f'v{i}'; offset+=SCENES[i][1]-.4
    output=OUT/f'hanja-film-{tag}.mp4'
    run([*inputs,'-i',str(audio),'-filter_complex',';'.join(filters),'-map',f'[{prior}]','-map',f'{len(scenes)}:a','-t',str(TOTAL),'-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(output)])
    run(['-ss','5','-i',str(output),'-frames:v','1','-update','1',str(RAW/f'poster-{tag}.png')])
    subprocess.run(['cwebp','-quiet','-q','88',str(RAW/f'poster-{tag}.png'),'-o',str(OUT/f'poster-{tag}.webp')],check=True)
    provenance={'prompt':'Authored product-film frame composed from actual Phi Agent Space captures of https://bryannamd.github.io/hanja-web/ on 2026-10-03. Original typography and original synthesized instrumental score. No simulated app UI or invented learning results.','source':'https://bryannamd.github.io/hanja-web/','duration':TOTAL,'format':tag,'script':'scripts/build-product-film.py'}
    (OUT/f'poster-{tag}.webp.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2))
    (OUT/f'hanja-film-{tag}.mp4.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2))
    print(output.name, round(output.stat().st_size/1024/1024,2),'MB',flush=True)
print('Duration:',TOTAL,flush=True)
