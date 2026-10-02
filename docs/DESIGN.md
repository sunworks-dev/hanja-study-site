---
name: "어흥!한자 소개 사이트"
description: "문방구 학습 놀이터의 온기로 한자를 연결하고, 쓰고, 떠올리는 웹 체험"
colors:
  paper: "#fff9ed"
  ink: "#233f35"
  muted: "#57655a"
  orange: "#be411f"
  mint: "#dfead5"
  line: "#d5d6c7"
  white: "#fffef9"
  yellow: "#f7d681"
typography:
  display:
    fontFamily: "Jua, SUIT, sans-serif"
    fontSize: "clamp(62px, 6.3vw, 88px)"
    fontWeight: 400
    lineHeight: 1.12
    letterSpacing: "-0.025em"
  headline:
    fontFamily: "Jua, SUIT, sans-serif"
    fontSize: "clamp(34px, 4vw, 54px)"
    fontWeight: 400
    lineHeight: 1.25
    letterSpacing: "-0.025em"
  title:
    fontFamily: "Jua, SUIT, sans-serif"
    fontSize: "clamp(25px, 3vw, 36px)"
    fontWeight: 400
    lineHeight: 1.25
    letterSpacing: "-0.02em"
  body:
    fontFamily: "SUIT, Apple SD Gothic Neo, Malgun Gothic, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.75
  action:
    fontFamily: "SUIT, Apple SD Gothic Neo, Malgun Gothic, sans-serif"
    fontSize: "17px"
    fontWeight: 800
    lineHeight: 1.4
  note:
    fontFamily: "SUIT, Apple SD Gothic Neo, Malgun Gothic, sans-serif"
    fontSize: "12px"
    fontWeight: 400
  hanja-piece:
    fontFamily: "Songti SC, Noto Serif CJK KR, Batang, serif"
    fontSize: "106px"
    fontWeight: 400
    lineHeight: 1.2
rounded:
  text-control: "6px"
  compact-control: "9px"
  answer: "10px"
  action: "12px"
  character-card: "13px"
  vocabulary: "14px"
  workspace: "16px"
spacing:
  small: "8px"
  control: "12px"
  inset: "16px"
  content: "24px"
  group: "32px"
  columns: "48px"
  section-mobile: "68px"
  section-tablet: "76px"
  section: "112px"
components:
  button-primary:
    backgroundColor: "{colors.orange}"
    textColor: "{colors.white}"
    typography: "{typography.action}"
    rounded: "{rounded.action}"
    padding: "14px 25px"
  button-primary-hover:
    backgroundColor: "#a33416"
  button-ink:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.white}"
    typography: "{typography.action}"
    rounded: "{rounded.action}"
    padding: "14px 25px"
  button-ink-hover:
    backgroundColor: "#355647"
  text-button:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.text-control}"
    padding: "8px 5px"
  answer-option:
    backgroundColor: "{colors.white}"
    textColor: "{colors.ink}"
    rounded: "{rounded.answer}"
  answer-option-hover:
    backgroundColor: "{colors.yellow}"
  answer-option-pressed:
    backgroundColor: "#f1ceaf"
  navigation:
    textColor: "{colors.ink}"
    padding: "12px 0"
  character-card:
    backgroundColor: "{colors.white}"
    rounded: "{rounded.character-card}"
    padding: "7px 5px 14px"
    width: "132px"
  writing-workspace:
    backgroundColor: "{colors.white}"
    rounded: "{rounded.workspace}"
    padding: "26px"
  vocabulary-page:
    backgroundColor: "#fae4ab"
    rounded: "{rounded.vocabulary}"
---

# Design System: 어흥!한자

## Overview

**Creative North Star: "문방구 학습 놀이터"**

학교 앞 문방구의 큰 글자 포스터, 학습 도장, 실제 앱 캐릭터의 온기를 가져온다. 넉넉한 크림색 바탕 위에 둥근 한국어 제목과 명확한 한자 획을 놓고, 직접 눌러 보는 체험으로 친근함을 전달한다. 본문과 근거는 차분한 먹빛 초록으로 읽힌다.

**Key Characteristics:**
- 크림·먹빛 초록을 바탕으로 주홍 행동과 노란 강조를 구분한다.
- Jua 제목, SUIT 설명, 명조 계열 한자의 역할을 나눈다.
- 학습 도구에는 둥근 면을, 설명 구간에는 여백과 구분선을 사용한다.
- 캐릭터는 실제 앱 자산을 재사용하고 체험·설명을 보조한다.

근거: [최종 CSS](../public/styles.css), [HTML](../public/index.html), [동작](../public/app.js), [제품](PRODUCT.md), [홈 방향](surfaces/home.md). 코드 우선 구현의 현재 상태를 기록한다. 승인된 별도 시안·QUALITY BAR 산출물은 없다. Phi 검증 캡처에는 브라우저 주입 파란 테마가 섞였으므로 색상 기준은 소스 CSS다.

사이드카는 문서 위치 규칙에 따라 [DESIGN.md.json](DESIGN.md.json)에 둔다. 일반 Impeccable 경로인 `.impeccable/design.json`과 다르므로 도구 연결 시 경로 지정이 필요하다. 사이드카의 생성 색조 램프는 미리보기용이며 사이트 토큰이 아니다.

## Colors

### Primary

- **주홍 (`orange`)**: 주 행동, 제목 일부, 연결할 한자, 손글씨 잉크, 포커스 표시.

### Secondary

- **연한 잎색 (`mint`)**: 첫 체험 무대와 마지막 시작 구간.
- **학습 노랑 (`yellow`)**: 선택 영역, 답 보기 호버, 기억 원리 도형과 달력 그림.

### Neutral

- **크림 종이 (`paper`)**: 페이지·고정 헤더 바탕, 어두운 구간의 제목.
- **먹빛 초록 (`ink`)**: 기본 글자, 보조 행동, 기억 설계 구간 바탕, 획순 시연.
- **설명 초록 (`muted`)**: 보충 설명·출처·상태 문구.
- **종이 흰색 (`white`)**: 한자 조각·연습장·답 보기와 진한 버튼의 글자.
- **종이 경계 (`line`)**: 헤더·리본·후기·FAQ의 얇은 구분선.

낱말 종이와 제작자 편지의 별도 따뜻한 면색은 해당 컴포넌트의 지역 값이다. 이를 새로운 전역 색상군으로 확대하지 않는다.

**The Source Palette Rule.** 색상 수정과 비교는 CSS 토큰을 기준으로 한다. 브라우저가 주입한 미리보기 테마를 브랜드 색으로 옮기지 않는다.

## Typography

Jua는 제목·브랜드·캐릭터의 짧은 말에 사용한다. SUIT는 본문·버튼·탭·출처를 담당한다. 로컬 WOFF2는 `font-display: swap`으로 로드하며 Jua는 400, SUIT는 100–900 가변 굵기다. 한자는 운영체제의 Songti SC·Noto Serif CJK KR·Batang·serif 조합을 사용하므로 기기별 자형 차이가 있다.

기본 계층은 frontmatter의 display/headline/title/body/action/note다. 모바일 본문은 16px, 주요 설명은 문맥에 따라 14–16px, 작은 출처는 대부분 12px다. 첫 제목은 기본 유동 크기에서 1100px 이하 68px, 560px 이하 57px, 360px 이하 52px로 줄어든다. 560px 이하 일반 h2는 35px이며 개별 구간의 크기 조정이 있다.

**The Script Roles Rule.** 한국어 안내는 Jua·SUIT, 학습할 한자는 명조 계열을 유지한다. 본문은 `word-break: keep-all`, 제목은 균형 줄바꿈을 사용한다. 폰트가 서브셋이므로 문구를 늘릴 때 새 글자의 포함 여부를 확인한다.

## Layout

- 기본 내용 폭은 최대 1256px, 좌우 안쪽 여백은 36px. 헤더는 최대 1360px, 40px 여백이며 88px 높이로 고정된다. 앵커 이동 여유는 110px.
- 첫 화면은 설명과 체험이 1:1.12, 학습·어휘는 1:1, 기억 원리는 3열, 친구들은 4열이다. 설명 구간은 반복 카드보다 넓은 면·선·여백으로 나뉜다.
- 1100px 이하: 첫 화면 1:1, 주요 열 간격과 캐릭터 크기 축소.
- 800px 이하: 좌우 여백 24px, 구간 여백 76px, 헤더 72px. 메뉴 링크를 숨기고 브랜드·웹 시작 버튼을 유지한다. 첫 화면·FAQ는 1열이며 첫 체험은 최대 530px.
- 560px 이하: 좌우 여백 22px, 구간 여백 68px. 학습·어휘·편지·후기는 1열, 친구는 2열. 어휘 설명을 카드 위에 둔다. 쓰기 설명은 `minmax(0, 1fr) 112px`, 이야기 도입은 2열 그리드에 제목 전체 폭을 사용한다. 두 캐릭터는 정상 흐름에 있어 글자와 겹치지 않는다.
- 360px 이하: 좌우 여백 18px와 작은 첫 제목. 파일 끝의 560px 규칙이 앞선 절대 위치 캐릭터 규칙을 덮어쓰는 순서를 보존한다.
- 1600px 이상: 첫 화면 세로 여백과 체험 무대 높이를 늘린다. 인쇄 시 헤더·체험·주 버튼을 숨기고 흰 바탕·검정 본문으로 전환한다.

홈의 구간 순서와 설득 전략은 [홈 문서](surfaces/home.md)에 둔다.

## Elevation & Depth

기본은 평평한 종이 면과 1px 경계다. 한자 조각에는 낮고 부드러운 그림자, 주홍 버튼에는 호버 그림자가 있다. 정확한 그림자 값은 사이드카에 기록한다. 문방구 도장과 살짝 기운 종이가 특징이며 유리 효과나 광택은 없다.

## Shapes

버튼·연습장·낱말 종이는 frontmatter의 둥근 모서리 범위 안에 있다. 첫 체험은 윗부분이 완만한 아치이고 아래는 작은 둥근 모서리다. 한자 조각은 좌우 7도, 낱말 종이는 기본 -2도 기울며 모바일에서 -1.4도다. 동그라미는 도장·회상 표시·복습 간격 점에 사용한다.

## Components

- **행동 버튼:** 주홍은 웹 체험 시작, 먹빛은 헤더·체험 내부 동작. 기본 최소 높이 58px, 작은 헤더 버튼은 46px이며 모바일은 44px. 호버 이동과 눌림 축소를 사용한다. 텍스트 동작은 배경 없이 44px 최소 높이를 둔다.
- **연결 체험:** `connect → recall → success`의 세 상태. 日·月을 합쳐 明의 뜻을 고르고, 오답은 힌트·선택 표시, 정답은 다음 학습 링크를 제공한다. 상태 변경 시 다음 조작 대상으로 포커스를 옮기며 다시 시작할 수 있다. 설명용 체험이고 기록을 저장하지 않는다.
- **손글씨 연습장:** 정사각형 십자 안내선과 연한 木 위의 600×600 캔버스. 포인터로 쓰기, 지우기, 네 획을 한 번씩 보여 주는 버튼이 있다. 채점은 하지 않는다. 획순 버튼이 키보드 대안이며 상태 문구가 각 획을 설명한다. 캔버스를 쓸 수 없으면 안내하고 도구를 비활성화한다.
- **어휘 종이:** 설명·명확·문명 탭, 큰 한자, 짧은 풀이와 강조한 예문. 탭은 선택 밑줄·`aria-selected`·순환 포커스를 사용하며 좌우 방향키·Home·End를 지원한다. 입력 필드·필터 칩은 없다.
- **설명 펼치기:** 근거와 FAQ는 네이티브 `details/summary`. 키보드로 열고 닫으며 보이는 제목과 출처를 유지한다.
- **접근성:** 본문 바로 가기, 명명된 탐색·구간, 이미지 대체 텍스트, 장식의 `aria-hidden`, 상태 안내를 사용한다. 포커스는 주홍 3px 외곽선과 5px 간격이며 캔버스만 잘림 방지를 위해 -4px 안쪽 간격이다.
- **모션:** 입력에 반응하는 동작만 있다. 버튼 180ms, 답 보기 150ms, 캐릭터 호버 300ms, 결합 550–600ms, 획순 한 획 420ms. `prefers-reduced-motion: reduce`에서는 CSS 전환·호버 이동·부드러운 스크롤을 없애고 획순을 즉시 표시한다.
- **자산:** `public/assets/`의 호랑 환영·쓰기·독서·축하 WebP, 또또·구름이·왜왜·앗차, 앱 아이콘과 실제 개발 화면을 재사용한다. 사진·신규 생성 삽화는 없다. 이미지마다 인접 `.webp.json`에 출처가 있고, 글꼴과 OFL 문서는 `assets/fonts/`에 있다. 영웅 이미지는 우선 로드하고 아래 이미지는 지연 로드한다. 조작 아이콘은 주로 인라인 SVG다.

## Do's and Don'ts

### Do:

- **Do** 소스의 색·서체 역할과 실제 앱 자산을 재사용한다.
- **Do** 320px 화면에서 설명과 캐릭터의 분리, 세 체험 상태, 키보드 포커스를 확인한다.
- **Do** 상태 전환·탭·획순의 키보드 동작과 모션 감소 처리를 유지한다.

### Don't:

- **Don't** 브라우저 주입 색이나 미리보기용 색조 램프를 사이트 토큰으로 채택한다.
- **Don't** 작은 화면의 쓰기·이야기 캐릭터를 텍스트 위의 절대 위치로 되돌린다.
- **Don't** 사용하지 않는 토큰이나 일회성 장식을 공통 규칙으로 늘린다.

규칙으로 승격하지 않은 항목: 사용되지 않는 `--orange-bright`, 본문 링크의 화살표 문자·FAQ의 `+`·모바일 후기의 `↳` 같은 글리프 아이콘. 후자는 현재 구현의 예외이며 새 컴포넌트가 복제할 아이콘 규칙으로 삼지 않는다.
