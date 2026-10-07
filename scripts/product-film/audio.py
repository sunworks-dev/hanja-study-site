#!/usr/bin/env python3
"""어흥!한자 38초 소개 영상용 배경 음악 + 효과음 합성 (numpy만 사용, 외부 음원 없음).

사용법: python scripts/product-film/audio.py --out out.wav
48kHz / 16bit / 스테레오 / 38.000초 (1,824,000 프레임). 120BPM, C 장조 5음 음계.
"""
import argparse
import wave

import numpy as np

SR = 48000
DUR = 38.0
N = int(SR * DUR)
BEAT = 0.5
rng = np.random.default_rng(20261006)  # 결정적 결과를 위한 고정 시드

mf = lambda m: 440.0 * 2 ** ((m - 69) / 12)  # MIDI -> Hz


def tt(sec):
    return np.arange(int(sec * SR)) / SR


def noise(sec):
    return rng.standard_normal(int(sec * SR))


def smooth(x, k):  # 이동평균 저역 통과
    return np.convolve(x, np.ones(k) / k, mode="same")


def hp(x):  # 단순 고역 통과(1차 차분)
    return np.diff(x, prepend=0.0)


def lp_sweep(x, a):  # 가변 1차 저역 통과 (a: 샘플별 계수 0~1)
    y = np.empty_like(x)
    s = 0.0
    for i in range(len(x)):
        s += a[i] * (x[i] - s)
        y[i] = s
    return y


# 버스: 악기군을 나눠 두고 마지막에 잔향·사이드체인을 적용한다
Z = lambda: np.zeros((N, 2))
mel, drm, bas, pad, fxb = Z(), Z(), Z(), Z(), Z()
rev_send = Z()
kicks = []  # 사이드체인용 킥 시각


def put(bus, t0, x, g=1.0, pan=0.0, send=0.0):
    """t0초 위치에 모노 신호를 팬(-1~1)과 함께 더한다. send는 잔향 보냄량."""
    i = int(round(t0 * SR))
    if i >= N or i + len(x) <= 0:
        return
    j = min(N, i + len(x))
    seg = x[: j - i] * g
    th = (pan + 1) * np.pi / 4  # 등전력 팬
    for tgt, k in ((bus, 1.0), (mrev if bus is mus else rev_send, send)):
        if k:
            tgt[i:j, 0] += seg * np.cos(th) * k
            tgt[i:j, 1] += seg * np.sin(th) * k


# ---------- 악기 ----------
def pluck(f, dur=0.9, bright=1.0, kal=False):
    """FM 마림바/칼림바: 빠른 변조 감쇠로 어택에 배음을 싣고 몸통은 맑게 남긴다."""
    t = tt(dur)
    r = 5.4 if kal else 4.0  # 칼림바는 비조화 비율로 금속성 추가
    idx = 3.0 * bright * np.exp(-t * (18 if kal else 14))
    y = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * r * t))
    y += 0.35 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 10)
    env = np.exp(-t * (5.5 if kal else 7.0)) * np.minimum(1, t / 0.002)
    return y * env * 0.5


def kick(vel=1.0):
    t = tt(0.4)
    ph = 2 * np.pi * np.cumsum(46 + 100 * np.exp(-t * 32)) / SR
    y = np.sin(ph) * np.exp(-t * 9) + 0.25 * smooth(noise(0.4), 6) * np.exp(-t * 180)
    return y * vel


def bass(f, dur=0.45):
    t = tt(dur)
    y = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t) * np.exp(-t * 8)
    return y * np.exp(-t * 3.5) * np.minimum(1, t / 0.006) * np.minimum(1, (dur - t) / 0.04)


def padv(notes, dur=2.4):
    """살짝 어긋난 사인 + 2배음으로 만든 부드러운 패드."""
    t = tt(dur)
    y = 0
    for m in notes:
        f = mf(m)
        for d in (-0.15, 0.0, 0.15):  # 약간의 코러스
            ff = f * 2 ** (d / 12)
            y = y + np.sin(2 * np.pi * ff * t + d * 5) + 0.3 * np.sin(4 * np.pi * ff * t)
    env = np.minimum(1, t / 0.35) * np.minimum(1, (dur - t) / 0.7) ** 2
    return y * env / (len(notes) * 4)


def shaker(vel=1.0):
    t = tt(0.1)
    return hp(hp(noise(0.1))) * np.exp(-t * 45) * np.minimum(1, t / 0.004) * 0.25 * vel


def wood(f=1000.0, vel=1.0):
    """나무 딱: 짧은 두 사인 + 클릭."""
    t = tt(0.12)
    y = np.sin(2 * np.pi * f * t) + 0.6 * np.sin(2 * np.pi * f * 1.52 * t)
    y = y * np.exp(-t * 55) + 0.5 * hp(noise(0.12)) * np.exp(-t * 300)
    return y * 0.5 * vel


def tick(f=2200.0, vel=1.0):
    t = tt(0.05)
    return (smooth(hp(noise(0.05)), 3) * 2 + np.sin(2 * np.pi * f * t)) * np.exp(-t * 110) * 0.22 * vel


def glide(f0, f1, dur, k=3.0):
    t = tt(dur)
    ph = 2 * np.pi * np.cumsum(np.linspace(f0, f1, len(t))) / SR
    return np.sin(ph) * np.sin(np.pi * np.minimum(1, t / dur * 1.0)) ** 0.5 * np.exp(-t * k) * np.minimum(1, t / 0.01)


def whoosh(dur, up=True, peak=0.5, soft=1.0):
    n = int(dur * SR)
    t = np.linspace(0, 1, n)
    c = (0.02 + 0.35 * (t if up else 1 - t) ** 1.5) * soft
    env = np.sin(np.pi * t) ** 2
    return lp_sweep(noise(dur), np.clip(c, 0.005, 0.8)) * env * 3.0 * peak


def riser(dur):
    n = int(dur * SR)
    t = np.linspace(0, 1, n)
    nz = lp_sweep(noise(dur), 0.02 + 0.5 * t ** 2) * 2.5
    ph = 2 * np.pi * np.cumsum(300 * 2 ** (3 * t)) / SR
    # 끝 60ms는 급히 줄여 도장 직전에 숨 쉬는 틈을 둔다
    return (nz * 0.7 + np.sin(ph) * 0.3) * t ** 2.2 * np.clip((1 - t) / 0.03, 0, 1)


def stamp(f0=70.0, vel=1.0):
    """나무 도장: 낮은 몸통 + 짧은 노이즈 어택 + 종이 마찰."""
    t = tt(0.6)
    body = np.sin(2 * np.pi * np.cumsum(f0 * (1 + 0.8 * np.exp(-t * 45))) / SR) * np.exp(-t * 13)
    thock = np.sin(2 * np.pi * f0 * 2.7 * t) * np.exp(-t * 55) * 0.5  # 나무 울림
    sub = np.sin(2 * np.pi * 42 * t) * np.exp(-t * 9) * 0.6
    atk = smooth(noise(0.6), 5) * np.exp(-t * 260) * 1.6  # 쾅 하는 어택
    fric = smooth(hp(noise(0.6)), 3) * (np.exp(-t * 28) - np.exp(-t * 90)) * 0.5  # 종이 마찰
    return (body + thock + sub + atk + fric) * 0.9 * vel


def crash(dur=1.2, vel=1.0):
    t = tt(dur)
    return hp(hp(noise(dur))) * np.exp(-t * 4) * 0.22 * vel


# ---------- 화성 ----------
PROG = [  # C - Am - F - G (장조 5음 기반)
    dict(pad=[48, 55, 60, 64, 67], root=36, arp=[72, 76, 79, 84], lead=[79, 76, 74, 72]),
    dict(pad=[45, 52, 57, 60, 64], root=33, arp=[69, 72, 76, 81], lead=[76, 72, 76, 81]),
    dict(pad=[41, 48, 57, 60, 64], root=41, arp=[69, 72, 74, 81], lead=[72, 69, 72, 76]),
    dict(pad=[43, 50, 55, 59, 62], root=43, arp=[67, 74, 76, 79], lead=[74, 79, 76, 74]),
]
chord = lambda t: PROG[int(t // 2) % 4]
def hit_chord(t, vel=1.0, ms=(72, 76, 79, 84, 88), pan_w=0.5):
    for k, m in enumerate(ms):  # 살짝 펼쳐서 반짝임
        put(mel, t + k * 0.012, pluck(mf(m), 1.4, 1.2), 0.9 * vel, (k - 2) * pan_w * 0.5, 0.5)


# ---------- 어쿠스틱 배경음악 ----------
# 음악은 별도 버스·별도 난수로 만든다. 효과음의 난수 순서와 소리를 건드리지 않기 위해서다.
mus, mrev = Z(), Z()
mr = np.random.default_rng(20261007)
GTR = [[48, 52, 55, 60, 64], [45, 52, 57, 60, 64], [41, 48, 53, 57, 60], [43, 47, 50, 55, 59]]  # 기타 개방 코드 보이싱
PICK = [0, 3, 1, 4, 0, 2, 1, None]  # 8분 핑거피킹: 저음 교대 + 고음, 마디 끝은 쉬어 숨을 둔다
hum = lambda t: t + mr.uniform(-0.009, 0.009)  # 사람 손 타이밍 흔들림
vj = lambda v: v * mr.uniform(0.82, 1.0)  # 벨로시티 변화


def ks(f, dur, tau=1.2, bright=0.5, pick=0.18):
    """Karplus-Strong 현: 노이즈 버스트를 지연선+평균 필터로 되먹여 줄 소리를 만든다."""
    P = max(2, int(round(SR / f - 0.5)))  # 평균 필터가 반 샘플 지연을 더한다
    n = int(dur * SR)
    exc = smooth(mr.standard_normal(P), 1 + int((1 - bright) * 8))  # 부드러운 손끝 = 고역 적은 버스트
    exc = exc - np.roll(exc, max(1, int(pick * P)))  # 피킹 위치 콤 필터
    d = np.exp(-(P + 0.5) / (SR * tau))
    buf = np.zeros(n + 2 * P + 2)
    buf[1:P + 1] = exc
    for s in range(P + 1, len(buf), P):
        e = min(s + P, len(buf))
        buf[s:e] = d * 0.5 * (buf[s - P:e - P] + buf[s - P - 1:e - P - 1])
    y = buf[1:n + 1]
    y = np.interp(np.arange(n) * f * (P + 0.5) / SR, np.arange(n), y)  # 정수 지연의 음정 오차 보정
    t = tt(dur)[:n]
    return y * np.minimum(1, t / 0.002) * np.minimum(1, (dur - t) / 0.03) / (np.std(exc) + 1e-9) * 0.3


def gtr(t, m, v, dur=1.6, pan=0.0, tau=1.2, bright=0.45):
    # 살짝 어긋난 두 현을 좌우로 겹쳐 12현 같은 넓이를 준다
    t, v = hum(t), vj(v)  # 두 현은 한 손가락이 치므로 같은 시각·세기
    for dc, p in ((0.04, -0.12), (-0.04, 0.12)):
        put(mus, t, ks(mf(m) * 2 ** (dc / 12), dur, tau, bright), v * 0.5, pan + p, 0.35)


def piano(f, dur=2.0):
    """비조화 배음 가산 합성 + 해머 노이즈: 따뜻한 업라이트 피아노 느낌."""
    t = tt(dur)
    y = np.zeros_like(t)
    for k in range(1, 9):
        fk = k * f * np.sqrt(1 + 0.0004 * k * k)  # 현의 강성 때문에 배음이 조금 높아진다
        if fk > 6000:
            break
        y += np.sin(2 * np.pi * fk * t) / k ** 1.4 * np.exp(-t * (0.9 + 0.7 * k))
    y += 0.4 * np.sin(2 * np.pi * f * t) * np.exp(-t * 0.5)  # 긴 여운(2단 감쇠)
    y += smooth(mr.standard_normal(len(t)), 12) * np.exp(-t * 90) * 0.15
    return y * np.minimum(1, t / 0.004) * np.minimum(1, (dur - t) / 0.08) * 0.3


def brush(v, swish=False):
    """브러시: 대역 제한 노이즈. 스위시는 어택을 느리게 해 쓸어내는 소리를 낸다."""
    dur = 0.4 if swish else 0.16
    t = tt(dur)
    x = mr.standard_normal(len(t))
    x = smooth(x, 5) - smooth(x, 60)
    env = np.minimum(1, t / (0.07 if swish else 0.004)) * np.exp(-t * (7 if swish else 22))
    return x * env * v * 0.12


def softkick(v):
    t = tt(0.3)
    ph = 2 * np.pi * np.cumsum(60 + 15 * np.exp(-t * 30)) / SR
    return np.sin(ph) * np.minimum(1, t / 0.008) * np.exp(-t * 13) * v * 0.5


# 구간별 편성: (시작, 끝, 피킹 'full'|'quarter'|None, 베이스, 브러시, 우쿨렐레, 피아노 선율, 음량)
ARR = [
    (0.5, 2.0, "full", True, False, False, False, 0.8),
    (4.0, 6.0, "full", True, False, False, False, 0.8),
    (6.0, 14.0, "full", True, True, False, True, 0.9),
    (14.0, 15.0, "quarter", True, False, False, False, 0.6),
    (18.0, 22.5, "full", True, True, True, True, 1.0),
    (23.0, 28.0, "full", True, True, True, True, 1.0),  # 22.5~23은 비워 동시 도장을 또렷하게
    (28.0, 32.0, "quarter", True, False, False, True, 0.85),
    (32.0, 34.0, "full", True, True, False, False, 0.85),
    (34.5, 36.0, "quarter", False, False, False, False, 0.6),
]


def music():
    for a, b, pk, bs, br, uk, pn, lv in ARR:
        t = a
        while t < b - 1e-9:
            ci = int(t // 2) % 4
            v, c = GTR[ci], PROG[ci]
            st = round((t % 2) / 0.25)  # 마디 안 8분 위치 0~7
            if PICK[st] is not None and (pk == "full" or (pk == "quarter" and st % 2 == 0)):
                sw = 0.03 if st % 2 else 0.0  # 가벼운 셔플
                m = v[PICK[st]]
                # 구간 끝에서 줄을 손으로 막아 다음 효과음 앞을 비운다
                gtr(t + sw, m, lv * (0.55 if PICK[st] < 2 else 0.4), min(1.8, b - t + 0.12), -0.15 + 0.1 * PICK[st])
            if bs and st in (0, 4):  # 하프타임: 마디에 두 번만 저음
                put(mus, hum(t), ks(mf(c["root"] - (0 if c["root"] < 40 else 12) + (7 if st == 4 else 0)), 1.0, 0.5, 0.15, 0.3),
                    vj(lv) * 0.9, 0, 0.1)
                if st == 0 and br:
                    put(mus, hum(t), softkick(vj(lv)), 0.8)
            if br and st in (2, 6):
                put(mus, hum(t), brush(vj(lv), swish=True), 1, 0.25, 0.2)
            if uk and st in (2, 6):  # 우쿨렐레 업스트로크: 높은 음부터 빠르게 긁는다
                for k, m in enumerate(sorted(c["arp"][:3], reverse=True)):
                    put(mus, hum(t) + k * 0.014, ks(mf(m - 12), 0.5, 0.35, 0.6), vj(lv) * 0.22, 0.4, 0.3)
            if pn and st == 0:
                for s, m in enumerate(c["lead"][:2]):
                    put(mus, hum(t + s * 1.25), piano(mf(m), 1.8), vj(lv) * 0.5, 0.1, 0.45)
            t += 0.25
    # 0.0 첫 화음과 2~4 조용한 피아노
    for k, m in enumerate(GTR[0]):
        gtr(0.02 + k * 0.022, m, 0.6, 2.2, -0.2 + 0.1 * k)
    for tm, m in ((2.0, 76), (2.75, 72), (3.5, 67)):
        put(mus, hum(tm), piano(mf(m), 1.6), 0.35, 0.1, 0.5)
    put(mus, 15.0, ks(mf(36), 0.95, 0.6, 0.15), 0.6, 0, 0.1)  # 도장 직전 저음 하나로 비운다
    gtr(15.0, 64, 0.35, 0.95)
    # 34.0 마무리: 느린 스트럼 + 피아노 주제 + 끝 화음
    for k, m in enumerate(GTR[0]):
        gtr(34.02 + k * 0.03, m, 0.7, 2.4, -0.2 + 0.1 * k)
    for tm, m, d in ((34.5, 79, 1.0), (35.0, 76, 1.0), (35.5, 74, 1.0), (36.0, 72, 2.0)):
        put(mus, hum(tm), piano(mf(m), d + 0.6), 0.55, 0.0, 0.6)
    for k, m in enumerate(GTR[0] + [67]):
        gtr(36.0 + k * 0.045, m, 0.5, 2.0, -0.25 + 0.1 * k, tau=2.0)
    put(mus, 36.0, ks(mf(36), 2.0, 1.0, 0.15), 0.7, 0, 0.1)


# 22~24는 패드를 빼 23.0 동시 도장 앞을 비운다
PADLEV = [(0, 2, 0.4), (2, 4, 0.45), (4, 14, 0.35), (14, 15.5, 0.3), (18, 22, 0.45), (24, 34, 0.45), (34, 36.5, 0.6)]


def pads():
    for a, b, lv in PADLEV:
        t = a
        while t < b - 1e-9:
            put(mus, t, padv(chord(t)["pad"], 2.4), lv, 0, 0.35)
            t += 2.0
    put(mus, 36.0, padv([48, 55, 60, 64, 67], 2.0), 0.6, 0, 0.5)


# ---------- 장면별 이벤트 ----------
def events():
    # 0.0 팡파르
    put(drm, 0, kick(1.3)); kicks.append(0.0)
    put(bas, 0, np.sin(2 * np.pi * 36 * tt(1.4)) * np.exp(-tt(1.4) * 2.2), 1.0)
    put(fxb, 0, crash(1.4, 1.0), 1, 0, 0.4)
    hit_chord(0.0, 1.0)
    # 2.0 얇아짐: 하강음 + 시계 틱
    put(fxb, 2.0, glide(420, 130, 0.9, 2.0), 0.6, 0, 0.5)
    for k in range(4):
        put(fxb, 2.5 + k * 0.5, tick(2400 if k % 2 == 0 else 1800), 1, -0.4 if k % 2 == 0 else 0.4, 0.2)
    # 4.0 브랜드 히트 + 팝
    put(drm, 4.0, kick(1.1)); kicks.append(4.0)
    hit_chord(4.0, 1.0, (60, 76, 79, 84, 88))
    for k, tm in enumerate((4.25, 4.5, 4.75, 5.25)):
        put(fxb, tm, glide(300 + 80 * k, 900 + 150 * k, 0.12, 6.0), 0.6, (k % 2) * 0.8 - 0.4, 0.3)
    # 7~10 나무 딱
    for k, tm in enumerate((7.0, 8.0, 9.0, 10.0)):
        put(fxb, tm, wood(900 * 2 ** (k * 2 / 12)), 1, -0.3 + k * 0.2, 0.25)
    # 12.0 휙(카드 입장)
    put(fxb, 11.8, whoosh(0.7, True, 0.5), 1, -0.3, 0.3)
    # 14~16 틱 가속 + 라이저
    tm, iv = 14.0, 0.5
    while tm < 16.0:
        put(fxb, tm, tick(2600, 0.6 + 0.4 * (tm - 14) / 2), 1, 0.3, 0.1)
        iv = max(0.07, iv * 0.82)
        tm += iv
    put(fxb, 14.0, riser(2.0), 0.28, 0, 0.3)
    # 16~17.5 도장 4번(음높이 상승) — 이 구간은 다른 소리가 거의 없다
    for k, tm in enumerate((16.0, 16.5, 17.0, 17.5)):
        put(fxb, tm, stamp(70 * 2 ** (k * 1.5 / 12)), 1.6, (k - 1.5) * 0.15, 0.12)
    # 18.0 해소
    put(drm, 18.0, kick(1.3)); kicks.append(18.0)
    put(fxb, 18.0, crash(1.4, 0.8), 1, 0, 0.4)
    hit_chord(18.0, 1.1, (72, 76, 79, 81, 86))
    put(bas, 18.0, bass(mf(36), 1.0), 0.9)
    # 21.5 도장이 흐려지는 하강음
    put(fxb, 21.5, glide(700, 180, 1.2, 2.0), 0.5, 0, 0.6)
    # 23.0 도장 동시 4개 + 화음
    for k in range(4):
        put(fxb, 23.0, stamp(70 * 2 ** (k * 1.5 / 12)), 0.55, (k - 1.5) * 0.25, 0.15)
    hit_chord(23.0, 0.8, (60, 72, 76, 79, 84))
    put(drm, 23.0, kick(1.0)); kicks.append(23.0)
    # 24~27 올라가는 플럭 + 블립
    for k, m in enumerate((72, 74, 76, 79)):
        put(mel, 24.0 + k, pluck(mf(m + 12), 1.0, 1.4), 0.8, -0.5 + k * 0.33, 0.5)
        put(fxb, 24.0 + k, glide(500, 1400, 0.1, 5.0), 0.3, -0.5 + k * 0.33, 0.3)
    # 28.0 책장 휙
    put(fxb, 27.85, whoosh(0.9, False, 0.4, 0.5), 1, 0.2, 0.5)
    # 32~33.5 캐릭터 블립
    for k, m in enumerate((84, 88, 91, 93)):
        put(mel, 32.0 + k * 0.5, pluck(mf(m), 0.8, 1.5), 0.8, -0.6 + k * 0.4, 0.4)
        put(fxb, 32.0 + k * 0.5, glide(400, 1600, 0.09, 5.0), 0.3, -0.6 + k * 0.4, 0.3)
    # 34.0 마지막 히트 + 주제 선율 정리
    put(drm, 34.0, kick(1.4)); kicks.append(34.0)
    put(bas, 34.0, np.sin(2 * np.pi * 36 * tt(2.0)) * np.exp(-tt(2.0) * 1.8), 1.0)
    put(fxb, 34.0, crash(2.0, 1.0), 1, 0, 0.5)
    hit_chord(34.0, 1.1, (72, 76, 79, 84, 88))


def events_minimal():
    # 외부 배경음악 위에 얹는 최소 효과음(2026-10-07). 시간 흐름과 도장만 남기고 로고·전환음은 뺀다.
    # 14~16 시계 틱: 반복 간격이 줄며 12시간이 지나가는 느낌
    tm, iv = 14.0, 0.5
    while tm < 16.0:
        put(fxb, tm, tick(2200, 0.4 + 0.3 * (tm - 14) / 2), 0.7, 0.2, 0.08)
        iv = max(0.09, iv * 0.84)
        tm += iv
    # 16~17.5 도장 4번(음높이 상승)
    for k, tm in enumerate((16.0, 16.5, 17.0, 17.5)):
        put(fxb, tm, stamp(70 * 2 ** (k * 1.5 / 12)), 1.2, (k - 1.5) * 0.15, 0.1)
    # 23.0 도장 동시 4개, 앞보다 약하게
    for k in range(4):
        put(fxb, 23.0, stamp(70 * 2 ** (k * 1.5 / 12)), 0.4, (k - 1.5) * 0.25, 0.12)


# ---------- 마스터 ----------
MUS_GAIN = 1.0  # 음악 버스를 효과음보다 약 6dB 낮게 두는 값


def music_bus():
    # 음악 전용 잔향: 짧고 어두운 룸. 효과음 잔향과 따로 둬 효과음 꼬리를 바꾸지 않는다
    n_ir = int(0.9 * SR)
    ti = np.arange(n_ir) / SR
    L = N + n_ir
    sz = 1 << (L - 1).bit_length()
    y = mus.copy()
    for c in (0, 1):
        ir = smooth(mr.standard_normal(n_ir), 9) * np.exp(-ti * 5.0)
        ir[: int(0.015 * SR)] *= np.linspace(0, 1, int(0.015 * SR))
        ir /= np.sqrt(np.sum(ir ** 2))
        y[:, c] += 0.45 * np.fft.irfft(np.fft.rfft(mrev[:, c], sz) * np.fft.rfft(ir, sz), sz)[:N]
    # 7kHz 위를 부드럽게 깎아 날카로운 고역을 없앤다
    fr = np.fft.rfftfreq(N, 1 / SR)
    lp = 1 / np.sqrt(1 + (fr / 7000) ** 4)
    return np.stack([np.fft.irfft(np.fft.rfft(y[:, c]) * lp, N) for c in (0, 1)], 1)


def master():
    t = np.arange(N) / SR
    # 사이드체인: 킥 직후 패드·베이스를 눌렀다 복귀
    g = np.ones(N)
    for k in kicks:
        i = int(k * SR)
        seg = np.arange(min(N - i, int(0.35 * SR))) / SR
        g[i:i + len(seg)] *= 1 - 0.55 * np.exp(-seg / 0.09)
    pad_b = pad * g[:, None]
    bas_b = bas * g[:, None]
    # 핑퐁 딜레이(점8분음표 0.375초)를 플럭 버스에 적용
    dl = int(0.375 * SR)
    wet = mel.copy()
    wet[dl:, 1] += 0.3 * mel[:-dl, 0]
    wet[2 * dl:, 0] += 0.15 * mel[:-2 * dl, 1]
    wet[2 * dl:, 0] += 0.12 * mel[:-2 * dl, 0] * 0  # 자리 표시(대칭 유지)
    dry = wet + drm + bas_b + pad_b * 0.9 + fxb
    # 잔향: 어둡게 감쇠하는 노이즈 임펄스 응답과 FFT 컨볼루션
    n_ir = int(1.4 * SR)
    ti = np.arange(n_ir) / SR
    irs = []
    for _ in range(2):
        ir = smooth(rng.standard_normal(n_ir), 5) * np.exp(-ti * 3.6)
        ir[: int(0.012 * SR)] *= np.linspace(0, 1, int(0.012 * SR))
        irs.append(ir / np.sqrt(np.sum(ir ** 2)) * 0.55)
    L = N + n_ir
    sz = 1 << (L - 1).bit_length()
    send = rev_send.copy()
    send[:, 0] += 0.0
    wetr = np.stack([np.fft.irfft(np.fft.rfft(send[:, c], sz) * np.fft.rfft(irs[c], sz), sz)[:N] for c in (0, 1)], 1)
    x = dry + wetr * 0.55
    x += music_bus() * MUS_GAIN
    # 끝 페이드(36.5~38) + 시작 0.01초 페이드
    env = np.ones(N)
    m = t >= 36.5
    env[m] = 0.5 * (1 + np.cos(np.pi * (t[m] - 36.5) / 1.5))
    env[: int(0.01 * SR)] *= np.linspace(0, 1, int(0.01 * SR))
    x = x * env[:, None]
    x = np.tanh(x * 0.9) / np.tanh(0.9)  # 부드러운 리미팅
    return x


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    # 외부 배경음악 위에 효과음만 얹을 때 쓴다(2026-10-07, 유튜브 오디오 보관함 곡 사용).
    ap.add_argument("--sfx-only", action="store_true")
    # 시계 틱·도장만 남긴 최소 효과음. --sfx-only와 함께 쓴다.
    ap.add_argument("--minimal", action="store_true")
    args = ap.parse_args()
    out = args.out
    events_minimal() if args.minimal else events()
    if not args.sfx_only:
        music()
        pads()
    x = master()
    x *= 10 ** (-1 / 20) / np.max(np.abs(x))  # 최대 피크 -1dBFS
    pcm = np.round(x * 32767).astype("<i2")
    with wave.open(out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


if __name__ == "__main__":
    main()
