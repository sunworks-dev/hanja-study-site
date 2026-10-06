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
    for tgt, k in ((bus, 1.0), (rev_send, send)):
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
ARP = [0, 1, 2, 1, 3, 2, 1, 2]


def hit_chord(t, vel=1.0, ms=(72, 76, 79, 84, 88), pan_w=0.5):
    for k, m in enumerate(ms):  # 살짝 펼쳐서 반짝임
        put(mel, t + k * 0.012, pluck(mf(m), 1.4, 1.2), 0.9 * vel, (k - 2) * pan_w * 0.5, 0.5)


# ---------- 리듬 구간 ----------
# (시작, 끝, 킥, 셰이커, 베이스, 아르페지오, 리드) / 킥: 'beat'|'bar'|'half' / 셰이커: 8|16
SECS = [
    (4.0, 6.0, "beat", 8, True, None, False),
    (6.0, 14.0, "beat", 8, True, 8, True),
    (14.0, 15.0, "beat", 8, True, 4, False),
    (15.0, 16.0, "bar", 0, False, None, False),
    (18.0, 20.0, "beat", 16, True, 8, True),
    (20.0, 22.5, "beat", 8, True, 8, True),
    (22.5, 23.0, None, 8, False, None, False),
    (23.0, 28.0, "beat", 8, True, 8, False),
    (28.0, 32.0, "bar", 8, True, 4, True),
    (32.0, 34.0, "beat", 16, True, 8, False),
    (34.0, 36.0, "half", 0, True, None, False),
]


def rhythm():
    for a, b, kk, sh, bs, ar, ld in SECS:
        t = a
        while t < b - 1e-9:
            c = chord(t)
            bi = round((t % 2) / BEAT)  # 마디 안 박 번호 0~3
            if kk == "beat" or (kk == "bar" and bi == 0) or (kk == "half" and bi % 2 == 0):
                vel = 0.55 if kk == "bar" else 0.9
                put(drm, t, kick(vel))
                kicks.append(t)
            if bs:  # 서브 베이스: 1박 길게 + 3·4박 사이 8분 푸시
                put(bas, t, bass(mf(c["root"] + (12 if bi == 3 else 0)), 0.42), 0.8)
                if bi in (1, 3) and kk == "beat":
                    put(bas, t + 0.25, bass(mf(c["root"] + 12), 0.2), 0.45)
            if sh:
                steps = 4 if sh == 16 else 2
                for s in range(steps):
                    if sh == 8 and s == 0:  # 8분 셰이커는 뒷박 위주
                        put(drm, t, shaker(0.35), 1, 0.3)
                    else:
                        put(drm, t + s * BEAT / steps, shaker(0.9 if s % 2 else 0.5), 1, -0.3 if s % 2 else 0.3)
            if ar:
                per = 2 if ar == 8 else 1
                for s in range(per):
                    idx = ARP[(bi * per + s) % 8]
                    tm = t + s * BEAT / per
                    put(mel, tm, pluck(mf(c["arp"][idx]), 0.7, 0.9, kal=True), 0.6,
                        0.45 if (bi * per + s) % 2 else -0.45, 0.45)
            if ld and bi == 0:  # 마디당 한 음 리드(주제 조각)
                for s, m in enumerate(c["lead"][:2]):
                    put(mel, t + s * 0.75 + (0.5 if s else 0), pluck(mf(m - 12 + 12), 1.0, 1.0), 0.55, 0.15, 0.55)
            t += BEAT


PADLEV = [(0, 2, 0.5), (2, 4, 0.55), (4, 14, 0.5), (14, 15.5, 0.4), (18, 34, 0.6), (34, 36.5, 0.7)]


def pads():
    for a, b, lv in PADLEV:
        t = a
        while t < b - 1e-9:
            put(pad, t, padv(chord(t)["pad"], 2.4), lv, 0, 0.35)
            t += 2.0


# ---------- 장면별 이벤트 ----------
def events():
    # 0.0 팡파르
    put(drm, 0, kick(1.3)); kicks.append(0.0)
    put(bas, 0, np.sin(2 * np.pi * 36 * tt(1.4)) * np.exp(-tt(1.4) * 2.2), 1.0)
    put(fxb, 0, crash(1.4, 1.0), 1, 0, 0.4)
    hit_chord(0.0, 1.0)
    for tm, m, d in ((0.5, 76, .5), (0.75, 79, .5), (1.0, 84, 1.0), (1.5, 88, 1.0)):
        put(mel, tm, pluck(mf(m), d + 0.4, 1.3), 0.8, 0.2, 0.5)
    put(bas, 1.0, bass(mf(36), 0.9), 0.8)
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
    for tm, m, d in ((34.5, 79, .4), (35.0, 76, .4), (35.5, 74, .4), (36.0, 72, 2.0)):
        put(mel, tm, pluck(mf(m + 12), d + 0.8, 1.1), 0.7, 0.0, 0.7)
    put(pad, 36.0, padv([48, 55, 60, 64, 67], 2.0), 0.7, 0, 0.5)
    put(pad, 34.0, padv([48, 55, 60, 64, 67, 72], 2.4), 0.5, 0, 0.5)


# ---------- 마스터 ----------
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
    out = ap.parse_args().out
    events()
    rhythm()
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
