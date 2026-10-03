---
name: "어흥!한자 소개 사이트"
description: "문방구 학습 놀이터의 온기로 실제 앱과 한자 학습을 만나는 제품 쇼케이스"
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
    fontSize: "clamp(60px, 6vw, 84px)"
    fontWeight: 400
    lineHeight: 1.12
    letterSpacing: "-0.03em"
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
  showcase-tab:
    backgroundColor: "transparent"
    textColor: "{colors.muted}"
    padding: "13px 0"
  showcase-tab-selected:
    backgroundColor: "transparent"
    textColor: "{colors.orange}"
    padding: "13px 0"
  film-chapter:
    backgroundColor: "transparent"
    textColor: "{colors.paper}"
    padding: "14px 0 8px"
  film-chapter-current:
    backgroundColor: "transparent"
    textColor: "{colors.yellow}"
    padding: "14px 0 8px"
  start-step:
    textColor: "{colors.ink}"
    padding: "22px 0 0"
  deep-summary:
    textColor: "{colors.ink}"
    padding: "26px 0"
---

# Design System: 어흥!한자

## 정책 문서 확장 · 2026-10-03

운영정보·개인정보 안내·이용약관·취소 및 환불은 기존 색상·Jua·SUIT를 재사용하는 읽기 문서다. `public/legal.css`에서 최대 72ch의 16px/1.85 본문, 38–58px 제목, 29px 소제목(모바일 27px), 13px 날짜·사업자 정보, 14px 탐색·출처를 지역 크기로 쓴다. 이 크기는 법적 안내의 가독성을 위한 의도적 확장이며 홍보 첫 화면의 타이포그래피를 바꾸지 않는다. 800px 이하에서 문서 탐색을 본문 위로 옮기고, 560px 이하에서는 운영 정보의 이름·값을 세로로 읽는다. 모든 주요 탐색 타깃은 44px 이상이다. 푸터는 정책 링크와 운영·문의·호스팅 정보를 나눠 보여준다. 법적 내용의 근거와 미확인 항목은 [법적 고지 점검](legal-review-2026-10-03.md)에서 관리한다.

## Overview

**Creative North Star: "문방구 학습 놀이터"**

학교 앞 문방구의 큰 글자 포스터, 학습 도장, 실제 앱 캐릭터의 온기를 가져온다. 넉넉한 크림색 바탕 위에 둥근 한국어 제목과 명확한 한자 획을 놓고, 실제 앱 화면·시연 영상·직접 눌러 보는 체험으로 친근함을 전달한다. 본문과 근거는 차분한 먹빛 초록으로 읽힌다.

**Key Characteristics:**
- 크림·먹빛 초록을 바탕으로 주홍 행동과 노란 강조를 구분한다.
- Jua 제목, SUIT 설명, 명조 계열 한자의 역할을 나눈다.
- 학습 도구에는 둥근 면을, 설명 구간에는 여백과 구분선을 사용한다.
- 캐릭터는 실제 앱 자산을 재사용하고 체험·설명을 보조한다.
- 앱 화면과 시연을 충분한 크기로 보여 주며, 선택한 기능과 그 화면을 가깝게 둔다.

근거: [기본 CSS](../public/styles.css), [쇼케이스 CSS](../public/showcase.css), [HTML](../public/index.html), [기존 체험 동작](../public/app.js), [영상·기능 탐색 동작](../public/showcase.js), [제품](PRODUCT.md), [홈 방향](surfaces/home.md), [제품 필름](surfaces/product-film.md), [내용·순서 점검](review/site-content-audit-2026-10-03.md). 2026-10-03 모션 필름 재제작과 내용·순서 교정 후 코드 우선 구현의 현재 상태를 기록한다. 기존 방향 seed `0436a9ef`의 5번 세계를 유지한다. 승인된 별도 시안·QUALITY BAR 산출물은 없다. Phi 검증 캡처에는 브라우저 주입 파란 테마가 섞였으므로 색상 기준은 소스 CSS다.

사이드카는 문서 위치 규칙에 따라 [DESIGN.md.json](DESIGN.md.json)에 둔다. 일반 Impeccable 경로인 `.impeccable/design.json`과 다르므로 도구 연결 시 경로 지정이 필요하다. 사이드카의 생성 색조 램프는 미리보기용이며 사이트 토큰이 아니다.

## Colors

### Primary

- **주홍 (`orange`)**: 주 행동, 제목 일부, 연결할 한자, 손글씨 잉크, 포커스 표시.

### Secondary

- **연한 잎색 (`mint`)**: 앱 화면 뒤의 면, 연결 체험 무대, 마지막 시작 구간.
- **학습 노랑 (`yellow`)**: 선택 영역, 답 보기 호버, 기억 원리 도형, 현재 영상 장면, 가격 안내 면.

### Neutral

- **크림 종이 (`paper`)**: 페이지·고정 헤더 바탕, 어두운 구간의 제목.
- **먹빛 초록 (`ink`)**: 기본 글자, 보조 행동, 영상·기억 설계 구간 바탕, 실제 화면 테두리, 획순 시연.
- **설명 초록 (`muted`)**: 보충 설명·출처·상태 문구.
- **종이 흰색 (`white`)**: 한자 조각·연습장·답 보기와 진한 버튼의 글자.
- **종이 경계 (`line`)**: 헤더·리본·후기·FAQ의 얇은 구분선.

낱말 종이와 제작자 편지의 별도 따뜻한 면색은 해당 컴포넌트의 지역 값이다. 영상 안쪽 면 `#172c25`, 영상 설명 `#d1decd`, 장면 구분선 `#708a78`, 장면 시간 `#bbceb8`, 영상 안내 `#c2d3be`, 노란 가격 면의 작은 안내 `#4b5137` 역시 해당 배경에서 쓰는 지역 값이다. 주홍 호버 `#a33416`은 기존 버튼과 재생 버튼이 공유한다. 지역 값을 새로운 전역 색상군으로 확대하지 않는다.

**The Source Palette Rule.** 색상 수정과 비교는 CSS 토큰을 기준으로 한다. 브라우저가 주입한 미리보기 테마를 브랜드 색으로 옮기지 않는다.

## Typography

Jua는 제목·브랜드·캐릭터의 짧은 말에 사용한다. SUIT는 본문·버튼·탭·출처를 담당한다. 로컬 WOFF2는 `font-display: swap`으로 로드하며 Jua는 400, SUIT는 100–900 가변 굵기다. 한자는 운영체제의 Songti SC·Noto Serif CJK KR·Batang·serif 조합을 사용하므로 기기별 자형 차이가 있다.

기본 계층은 frontmatter의 display/headline/title/body/action/note다. 모바일 본문은 16px, 주요 설명은 문맥에 따라 14–16px, 작은 출처는 대부분 12px다. 제품 첫 제목은 801–1100px에서 62px, 561–800px에서 `clamp(55px, 10vw, 76px)`, 560px 이하 54px, 360px 이하 48px다. 작은 화면 첫 제목의 행간은 1.13이다. 560px 이하 일반 h2는 35px이며 영상 제목과 기능 제목은 32px다.

쇼케이스의 지역 조정: 영상 제목은 `clamp(33px, 3.5vw, 48px)`, 기능 제목은 `clamp(30px, 3.2vw, 43px)`와 행간 1.3, 기능 설명은 43ch 이내와 행간 1.9를 쓴다. 기능 탭은 15px/700, 선택 상태 900이며 태블릿 13px·모바일 14px로 조정한다. 가격 숫자는 SUIT 900, `clamp(58px, 5.5vw, 76px)`, 모바일 63px다. 시간·가격 숫자에는 tabular numerals를 사용한다. 모바일 영상·출시 보조 안내의 11px은 해당 구간의 현행 지역 크기이며 기본 본문 계층으로 확대하지 않는다.

**The Script Roles Rule.** 한국어 안내는 Jua·SUIT, 학습할 한자는 명조 계열을 유지한다. 본문은 `word-break: keep-all`, 제목은 균형 줄바꿈을 사용한다. 폰트가 서브셋이므로 문구를 늘릴 때 새 글자의 포함 여부를 확인한다.

## Layout

- 기본 내용 폭은 최대 1256px, 좌우 안쪽 여백은 36px. 헤더는 최대 1360px, 40px 여백이며 88px 높이로 고정된다. 앵커 이동 여유는 110px.
- 첫 제품 화면은 설명과 실제 앱 화면이 1:1.04, 간격 30px, 위아래 여백 60px/76px다. 기능 화면과 설명은 .9:1.1, 가격 설명과 안내 면은 1.1:1이며 두 구간의 열 간격은 80px다. 기존 연결 체험은 1:1.12, 학습·어휘는 1:1, 기억 원리는 3열, 친구들은 4열이다. 설명 구간은 반복 카드보다 넓은 면·선·여백으로 나뉜다.
- 801–1100px: 제품 화면 열 간격 10px, 앱 화면 폭 205px로 축소. 기능·가격 열 간격은 40px다.
- 시작 단계는 3열, 열 간격 36px, 위아래 여백 48px/34px다. 각 단계는 윗선과 22px 안쪽 여백으로 나누고 번호·제목·설명을 둔다. 상세 펼치기는 구간 전체 폭의 경계선과 좌우 정렬한 제목·SVG 표시를 사용한다.
- 800px 이하: 좌우 여백 24px, 구간 여백 76px, 헤더 72px. 메뉴 링크를 숨기고 브랜드·웹 시작 버튼을 유지한다. 제품 첫 화면·연결 체험·가격·FAQ는 1열이며 기능 쇼케이스는 아직 2열이다. 가격 안내 면은 최대 530px다. 시작 단계 간격은 20px이며 시작 버튼·기록 안내는 세로로 쌓는다.
- 560px 이하: 좌우 여백 22px, 구간 여백 68px. 기능 쇼케이스는 탭 → 실제 화면 → 설명·목록 → 웹 체험 링크 → 데이터 안내의 1열이다. 설명 래퍼의 `display: contents`와 화면의 2번째 grid row로 이 순서를 만든다. 영상은 세로 9:16, 최대 폭 410px, 장면 선택은 2열이다. 시작 단계는 1열이며 각 항목 안에서 44px 번호 열과 설명 열을 나눈다. 학습·어휘·편지·후기는 1열, 친구는 2열. 어휘 설명을 카드 위에 둔다. 쓰기 설명은 `minmax(0, 1fr) 112px`, 이야기 도입은 2열 그리드에 제목 전체 폭을 사용한다. 두 캐릭터는 정상 흐름에 있어 글자와 겹치지 않는다.
- 360px 이하: 좌우 여백 18px와 작은 첫 제목. 파일 끝의 560px 규칙이 앞선 절대 위치 캐릭터 규칙을 덮어쓰는 순서를 보존한다.
- 1600px 이상: 기존 연결 체험의 세로 여백과 체험 무대 높이를 늘린다. 제품 첫 화면에는 이 규칙을 적용하지 않는다. 인쇄 시 헤더·체험·영상·주 버튼을 숨기고 흰 바탕·검정 본문으로 전환한다.

홈은 제품 첫 화면·영상·기능 탐색·가격·시작 3단계·연결 체험·쓰기와 어휘·제작자 이야기·선택해서 펼치는 상세·FAQ·마지막 웹 체험과 푸터 순서다. 상세 안에 기억 설계·친구·시험과 익명 후기 두 묶음을 둔다. 이 순서는 현재 홈의 기록이며 전역 화면 규칙이 아니다. 설득 전략과 이후 순서 변경은 [홈 문서](surfaces/home.md)에 둔다.

## Elevation & Depth

기본은 평평한 종이 면과 1px 경계다. 한자 조각에는 낮고 부드러운 그림자, 주홍 버튼에는 호버 그림자가 있다. 앱 화면 프레임은 두 겹의 부드러운 그림자로 종이 무대와 구분한다. 첫 화면의 호랑에는 `drop-shadow(0 8px 8px rgb(35 63 53 / 12%))`만 더한다. 정확한 그림자 값은 사이드카에 기록한다. 문방구 도장과 살짝 기운 종이가 특징이며 유리 효과나 광택은 없다.

## Shapes

버튼·연습장·낱말 종이는 frontmatter의 둥근 모서리 범위 안에 있다. 기존 연결 체험은 윗부분이 완만한 아치이고 아래는 작은 둥근 모서리다. 한자 조각은 좌우 7도, 낱말 종이는 기본 -2도 기울며 모바일에서 -1.4도다. 제품 화면 두 장은 각각 -7도/+5도, 1:2 비율을 유지하며 먹빛 테두리 3px·반경 17px, 560px 이하 4px·14px로 감싼다. 안쪽 이미지 반경은 13px다. 영상·기능 화면 배경·가격 면과 기능 탐색의 화면 이미지 반경은 16px다. 이 프레임 수치는 해당 컴포넌트의 지역 조정이다. 동그라미는 도장·회상 표시·복습 간격 점과 제품 화면 뒤의 잎색 면에 사용한다.

## Components

- **행동 버튼:** 주홍은 웹 체험 시작, 먹빛은 헤더·체험 내부 동작. 기본 최소 높이 58px, 작은 헤더 버튼은 46px이며 모바일은 44px. 호버 2px 들림과 눌림 `scale(0.96)`를 사용한다. 주 진입 버튼의 문구는 ‘웹에서 체험하기’로 통일한다. 텍스트 동작은 배경 없이 44px 최소 높이를 둔다.
- **헤더 탐색:** 데스크톱은 ‘앱 둘러보기’·‘가격·이용 안내’·‘시작 방법’을 해당 앵커로 연결한다. 800px 이하에서는 메뉴 링크를 숨기고 브랜드·웹 체험 버튼을 유지한다.
- **제품 첫 설명:** 한자·어휘 학습 앱이라는 제품 종류와 초보부터 급수 준비까지의 대상을 큰 제목 아래에 둔다. 주 행동 가까이에 설치·가입 없는 웹 체험과 스토어 준비 상태를 적고, 예정 가격은 가격 구간 앵커로 연결한다.
- **제품 화면 무대:** 실제 퀴즈와 획순·어휘 화면 두 장을 1:2 비율로 보여 준다. 화면에 포함된 앱 자체 색과 문구를 사이트 팔레트로 재작성하지 않는다. 호랑은 화면 하단을 보조하며 설명을 대체하지 않는다.
- **제품 영상:** 먹빛 면 안의 32초 실제 앱 모션 필름. 키네틱 글자 마스크·원근감 있는 기기·실제 앱 녹화와 화면·기존 캐릭터를 120 BPM 자체 합성 음악·효과음에 맞춰 사전 렌더링한다. 가로 1920×1080·세로 1080×1920, 30fps이며 앱 내부 표시 결과는 합성하지 않는다. 560px 이하에서는 첫 재생 전 세로 버전을 고르며, 재생을 시작한 뒤 크기를 바꿔도 소스와 위치를 유지한다. 표지 위의 재생 버튼이나 네 장면 버튼으로 시작하고 자동 재생하지 않는다. 장면 버튼은 00:07·00:13·00:17·00:21과 설명을 함께 표시하며 실제 이동 시각은 7.25·13.25·17.25·21.25초다. 현재 장면 표시의 끝은 각각 10·17·21·25초이며 노랑 글자와 선으로 표시한다. 기본 video 컨트롤, 한국어 장면 설명 트랙, 연결 오류 안내, 화면 밖·백그라운드 일시 정지를 제공한다.
- **기능 탐색:** 4개 탭이 실제 화면·제목·설명·목록을 함께 바꾼다. 탭은 투명 바탕과 얇은 밑선, 선택 시 주홍·굵은 글자다. `aria-selected`, roving tabindex, 좌우 방향키·Home·End를 지원한다. ‘화면 크게 보기’는 선택한 기능의 실제 이미지 URL과 대체 설명을 함께 갱신하며 새 탭으로 연다. 모바일에서는 탭 다음에 실제 화면·확대 링크를 두고 상세 설명을 뒤로 보낸다.
- **가격 안내:** 노란 면에 29,900원 숫자·일회 구매·3일 체험 조건·웹 체험 버튼을 묶는다. 제목과 숫자만으로 판매 상태를 암시하지 않도록 출시 예정 가격과 스토어 결제 준비 중 안내를 같은 면에 유지한다. 데스크톱 안쪽 여백 44px/38px/36px, 모바일 30px/24px다. 가격과 판매 조건의 원자료는 PRODUCT.md다.
- **시작 안내:** 번호 01·02·03, 급수 선택·하루 분량·오늘의 학습을 순서 있는 목록으로 보여 준다. 큰 카드 대신 얇은 윗선을 사용한다. 아래에는 웹 체험과 기기·브라우저별 기록 보관 안내를 함께 두고 FAQ의 기록 답변으로 연결한다.
- **연결 체험:** `connect → recall → success`의 세 상태. 日·月을 합쳐 明의 뜻을 고르고, 오답은 힌트·선택 표시, 정답은 다음 학습 링크를 제공한다. 상태 변경 시 다음 조작 대상으로 포커스를 옮기며 다시 시작할 수 있다. 설명용 체험이고 기록을 저장하지 않는다.
- **손글씨 연습장:** 정사각형 십자 안내선과 연한 木 위의 600×600 캔버스. 포인터로 쓰기, 지우기, 네 획을 한 번씩 보여 주는 버튼이 있다. 채점은 하지 않는다. 획순 버튼이 키보드 대안이며 상태 문구가 각 획을 설명한다. 캔버스를 쓸 수 없으면 안내하고 도구를 비활성화한다.
- **어휘 종이:** 설명·명확·문명 탭, 큰 한자, 짧은 풀이와 강조한 예문. 탭은 선택 밑줄·`aria-selected`·순환 포커스를 사용하며 좌우 방향키·Home·End를 지원한다. 입력 필드·필터 칩은 없다.
- **설명 펼치기:** 학습 설계·친구·시험과 타 앱 익명 후기는 두 개의 네이티브 `details/summary`로 묶고 처음에는 접는다. 큰 제목·작은 설명·오른쪽 SVG 더하기가 한 행을 이루며 열면 표시가 45도 회전한다. 내부 연구 근거와 FAQ 8개도 네이티브 펼치기를 쓴다. 해시 이동은 대상과 모든 조상 `details`를 열어 보여 주며 같은 해시를 다시 클릭해도 작동한다. 타 앱 후기의 A/B/C 익명, 작성자 비공개·원문 링크 제거는 해당 콘텐츠의 기존 처리이며 자사 고객 후기로 바꾸지 않는다.
- **기록·개인정보 안내:** 시작 구간의 짧은 안내와 FAQ의 자세한 답변을 연결한다. 개인정보 처리방침은 FAQ·푸터의 공식 링크로 제공한다.
- **아이콘:** 동작·외부 링크·FAQ는 currentColor 기반 인라인 SVG, 1.8px stroke, 둥근 끝·모서리를 공유한다. 일반 아이콘은 24px, 텍스트 링크는 16–20px다. FAQ의 SVG 더하기는 기존 열림 상태 회전을 따른다. 학습식 日+月의 더하기는 한자 조합 의미를 전달하는 문자이며 조작 아이콘과 구분한다.
- **접근성:** 본문 바로 가기, 명명된 탐색·구간, 이미지 대체 텍스트, 장식의 `aria-hidden`, 상태 안내를 사용한다. 포커스는 주홍 3px 외곽선과 5px 간격이며 캔버스만 잘림 방지를 위해 -4px 안쪽 간격이다.
- **모션:** 페이지 UI는 입력에 반응하고, 모션 필름은 사용자 재생 후 영상 시간축을 따른다. 버튼·상세 묶음 표시 회전 180ms, 근거·FAQ 표시 회전 200ms, 답 보기 150ms, 캐릭터 호버 300ms, 결합 550–600ms, 획순 한 획 420ms. `prefers-reduced-motion: reduce`에서는 CSS 전환·호버 이동·부드러운 스크롤을 없애고 획순을 즉시 표시한다. 사전 렌더링 영상 자체의 동작은 바꾸지 않으며 정지 표지와 재생 선택을 유지한다.
- **자산:** `public/assets/`의 호랑 환영·쓰기·독서·축하 WebP, 또또·구름이·왜왜·앗차, 앱 아이콘과 실제 개발 화면을 재사용한다. `assets/screens/`에는 실제 웹 앱 5종, `assets/video/`에는 `hanja-motion-{landscape,portrait}.mp4`, `poster-motion-{landscape,portrait}.webp`, `hanja-motion-ko.vtt`와 출처 sidecar를 둔다. 사진·신규 생성 삽화는 없다. 배포 이미지·영상에는 인접 출처 sidecar가 있고, 글꼴과 OFL 문서는 `assets/fonts/`에 있다. 첫 화면 두 앱 이미지는 우선 로드하고 아래 이미지는 지연 로드한다. 영상은 `preload="none"`이다. 변경된 CSS·JS·폰트 URL의 `?v=20261003-motion`은 이전 배포 캐시와 새 영상 주소의 혼용을 막는 배포 식별자이며 디자인 토큰이 아니다.

## Do's and Don'ts

### Do:

- **Do** 소스의 색·서체 역할과 실제 앱 자산을 재사용한다.
- **Do** 320px 화면에서 설명과 캐릭터의 분리, 세 체험 상태, 키보드 포커스를 확인한다.
- **Do** 상태 전환·탭·획순의 키보드 동작과 모션 감소 처리를 유지한다.
- **Do** 모바일 기능 탭과 실제 화면을 붙여 두고 영상은 사용자 입력으로 재생한다.

### Don't:

- **Don't** 브라우저 주입 색이나 미리보기용 색조 램프를 사이트 토큰으로 채택한다.
- **Don't** 작은 화면의 쓰기·이야기 캐릭터를 텍스트 위의 절대 위치로 되돌린다.
- **Don't** 사용하지 않는 토큰이나 일회성 장식을 공통 규칙으로 늘린다.
- **Don't** 링크·펼치기 조작을 글리프 아이콘으로 되돌리거나 앱 화면의 표시 결과를 재작성한다.

규칙으로 승격하지 않은 항목: 사용되지 않는 `--orange-bright`, 브라우저 주입 파란 테마, 단일 구간의 글자 크기·배경색·앱 프레임 반경. 지역 조정은 해당 구간의 기록이며 공통 토큰이 아니다. 대부분의 조작 아이콘은 SVG로 교체되었으나 체험의 다음 학습 링크에는 문자 화살표가 남아 있다. 이 지역 예외를 재사용할 아이콘 규칙으로 삼지 않는다.
