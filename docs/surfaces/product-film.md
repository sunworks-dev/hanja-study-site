---
surface: product-film
mode: persuade
target: public/assets/video/hanja-motion-landscape.mp4
---

# 2026-10-06 제품 필름 재제작 (현재 판)

사용자가 사이트의 컨셉과 핵심 내용을 대본으로 삼아 훨씬 세련된 소개 영상으로 다시 만들 것을 요청했다. 아래 2026-10-03 판을 대체한다.

THESIS: “한 번 맞혔다고, 익혔다고 하지 않아요.” 네 칸을 익히고 12시간 뒤 다시 떠올려야 도장이 찍히는 과정을 38초에 보여 준다.
OWN-WORLD: 사이트의 문방구 학습 놀이터와 익힘 도장판을 그대로 옮긴다. 크림·먹빛 초록·주홍·노랑, Jua 제목, 주홍 도장, 노란 테이프, 새 앱 아이콘.
STORY(초): 0–2 “외웠다!” → 2–4 “…내일도 기억날까?” → 4–6 아이콘과 이름, 핵심 문장 → 6–12 네 가지로 익히기(실제 퀴즈·획순 녹화) → 12–14 오늘은 빈칸 → 14–18 12시간 시계와 도장 네 번 → 18–20 “익힘.” → 20–24 30일 달력, 다시 확인, 다시 도장 → 24–28 연결 고리(모양·그림·낱말·이야기) → 28–32 옛이야기 녹화와 이야기 11편 → 32–34 도감과 친구들 → 34–38 아이콘·이름·주소.
FORM: 가로 1920×1080, 세로 1080×1920, 30fps, 38초. 120 BPM이라 2초마다 장면이 바뀌고 도장은 박자에 맞춰 찍힌다. 세로는 따로 배치한다.
사실 경계: 휴대폰 안의 화면은 실제 앱 녹화를 고치지 않고 쓴다. 도장판·시계·달력·연결 그림은 원리 설명용 그림이며 앱 화면으로 보이게 만들지 않는다. 12시간·23일·30일은 앱 `lib/srs/hanja_mastery.dart` 기준이다.

## 만드는 방법 (2026-10-06 판)

- 장면 원본은 `scripts/product-film/film.html` 하나다. 모든 움직임을 `seek(초)`가 계산하므로 같은 프레임을 언제든 똑같이 다시 그린다. `?t=16.6`으로 한 장면을, `?play=1`로 미리보기를 본다.
- 음악·효과음은 `scripts/product-film/audio.py --out film.wav`가 수식으로 합성한다(numpy만 사용, 외부 음원 없음).
- 촬영: 저장소 루트에서 `python3 -m http.server 4323`을 켜고 `FILM_O=landscape FILM_OUT=<폴더> node ~/.claude/skills/phi-browser/scripts/runner.mjs < scripts/product-film/capture.js`. 세로는 `FILM_O=portrait`. 각 1,140장.
- 인코딩: `ffmpeg -framerate 30 -i <폴더>/%05d.jpg -i film.wav -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -af loudnorm=I=-16:TP=-1.5:LRA=9 -c:a aac -b:a 160k -t 38 -movflags +faststart <출력>.mp4`.
- 필요한 로컬 자료(git 제외): `.tmp/product-film-captures/`의 녹화 4종·Jua 원본과 `fonts/`(앱 `flutter_app/assets/fonts`의 Pretendard Medium·Bold, NotoSerifKR SemiBold 복사본).
- `scripts/build-product-film.py`는 2026-10-03 판을 만든 이전 스크립트다. 현재 영상에는 쓰지 않는다.

# 2026-10-03 제품 필름 재제작 (이전 판)

사용자는 이전 고정 레이아웃 시연 영상을 거절하고, 감각적인 앱 광고 수준의 모션 그래픽을 명확히 요청했다. 단순 자막/배경 교체가 아니라 시간축의 연출을 교체한다. 기존 사이트·제품 사실·캐릭터·크림/초록/주홍/Jua 정체성은 보존한다.

THESIS: 한 글자가 실제 학습 화면과 낱말, 이야기, 도감으로 확장되는 32초 제품 광고.
OWN-WORLD: 문방구 학습 놀이터의 큰 활자와 실제 캐릭터를 현대적인 제품 모션으로 확장. 인터페이스 안의 결과는 만들지 않는다.
STORY: 0–4초 키네틱 한글 오프닝, 4–7초 입체 기기 등장, 7–10초 실제 회상 퀴즈, 10–13초 한자에서 낱말로, 13–17초 획순 확대, 17–21초 이야기, 21–25초 도감, 25–28초 캐릭터 앙상블, 28–32초 브랜드·웹 체험.
FIRST VIEWPORT: 크기를 가득 쓰는 한글이 박자에 맞춰 마스크로 드러나고 한자·캐릭터가 다음 장면을 연다. 이전의 좌측 설명/우측 고정 폰 템플릿은 반복하지 않는다.
FORM: 사용자 지정 모션 그래픽 재제작. 실제 앱 녹화와 캡처, 입체 투영·오브젝트의 연속 이동·클로즈업·타이포 마스크·컷 전환·독자적인 120 BPM 음악과 효과음을 사용. 가로1920×1080/세로1080×1920,30fps. 모바일은 별도 구도로 제작. 재생은 사용자가 시작한다.
FINISH: 두 화면비의 대표 프레임·전환·실제 재생을 확인하고, 사용자 거절 사유를 기준으로 독립 검수. 소스·영상·표지·장면 자막·사이트 타임코드를 함께 갱신한다.

## 모션 계획

- 초점: 한 글자가 낱말과 앱 학습 화면으로 확장되는 크기·거리·회전의 연결.
- 연속성: 실제 화면은 기기 안에서 유지. 일부는 카메라가 확대하지만 앱 버튼·숙련 수치·정답 표시를 합성하지 않음.
- 피드백: 촬영된 선택/정답/획순을 보존하며 영상 외부의 글자와 장면 전환이 음악에 맞춰 반응.
- 예산: 모든 합성은 사전 렌더링 MP4. 사이트는 H.264 영상 한 개만 사용자 입력 후 읽음. 실시간 WebGL/추가 프레임워크 없음.
- 참고: [Ordinary Folk 제작 과정](https://www.ordinaryfolk.co/process)의 메시지·디자인·움직임·사운드를 함께 설계하는 제작 순서를 참고. 타사 영상·음악·그림은 재사용하지 않음.


## 재편집 자료

- 원본 캡처는 로컬 `.tmp/product-film-captures/`에 보존한다(약52MB, git 제외). `recall`, `strokes`, `story`, `collection`의 JPG 시간축과 `frames.json`, 실제 화면 PNG, Jua 원본을 포함한다.
- 렌더: `/tmp/hanja-site-fonts-review/bin/python scripts/build-product-film.py .tmp/product-film-captures --out /tmp/hanja-motion`.
- Python 의존성: Pillow, NumPy, OpenCV headless. 인코더: ffmpeg. 나머지 서체는 형제 앱의 `flutter_app/assets/fonts`를 참조한다.
- 공개 산출물은 `public/assets/video/hanja-motion-{landscape,portrait}.mp4`, 같은 폴더의 표지·자막·출처 sidecar.
- 별도 생성 이미지·외부 음악 없이 기존 캐릭터/실제 웹 녹화를 사용. 기기 프레임과 낱말 연결 그래픽은 소개용 연출이며 앱 UI 내부는 합성하지 않는다.
