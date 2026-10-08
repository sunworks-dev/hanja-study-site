# hanja-study-site

`hanja-study-app` 출시 안내와 제품 소개를 위한 웹사이트 저장소입니다.

## 사이트 주소

Sunworks에서 새로 만드는 서비스와 소개 사이트는 `sunw.kr`의 하위 도메인을 사용합니다.

| 대상                | 주소                                                                    | 상태                  |
| ------------------- | ----------------------------------------------------------------------- | --------------------- |
| 한자 앱 소개 사이트 | [hanja.sunw.kr](https://hanja.sunw.kr/)         | 공식 소개·학습 맛보기 |
| 한자 웹 앱          | [hanja-app.sunw.kr](https://hanja-app.sunw.kr/) | 웹 베타(앱 저장소 배포) |

소개 사이트의 **웹에서 시작하기** 링크는 기존 한자 웹 앱으로 연결합니다.
웹 앱 빌드 결과물은 계속 [`bryannamd/hanja-web`](https://github.com/bryannamd/hanja-web)에 배포합니다.

## 콘텐츠

- 日·月 연결, 뜻 맞히기, 손글씨·획순, 어휘 전환 체험
- 읽기·뜻·쓰기·부수 익힘 도장판(12시간 뒤 다시 맞히기, 30일 유지)
- FSRS 복습 원리를 망각곡선 그림과 실제 자신감 선택 화면으로 설명
- FSRS 복습 원리, 캐릭터, 성취 기록, 모바일 시험 알림
- 중2 아들과 함께 만든 이야기와 계속 개선하는 약속
- 실제 App Store 낮은 평가의 출처 있는 요약
- 웹 베타 시작 링크, 출시 준비·가격 정책 안내, FAQ

## 현재 상태

`sunworks-dev` 조직의 공개 저장소입니다. 프레임워크나 외부 런타임 없이 HTML·CSS·JavaScript로 구성했습니다. 배포 파일은 `public/`이며, 앱의 기존 그림과 직접 호스팅하는 글꼴을 사용합니다. 소개 체험은 브라우저 메모리 안에서만 동작하며 앱 학습 기록을 변경하지 않습니다.

## 시작하기

```sh
git clone https://github.com/sunworks-dev/hanja-study-site.git
cd hanja-study-site
python3 -m http.server 4322 --directory public
```

로컬 확인 주소는 `http://localhost:4322`입니다. 별도 빌드나 패키지 설치가 필요하지 않습니다.

문구·구조는 `public/index.html`, 시각 규칙은 `public/styles.css`, 체험 동작은 `public/app.js`에서 편집합니다. 새 문구를 넣으면 글꼴 서브셋도 다시 만들어 주세요. 현재 서브셋에 없는 문자는 시스템 대체 글꼴로 표시됩니다.

```sh
python3 -m venv /tmp/hanja-fonts
/tmp/hanja-fonts/bin/pip install fonttools brotli
/tmp/hanja-fonts/bin/python scripts/subset-fonts.py
```

글꼴 재생성은 콘텐츠를 바꿀 때만 필요하며, 일반 실행·배포에는 Python 패키지가 필요하지 않습니다.

## 소개 영상

`scripts/product-film/`에 장면 원본(`film.html`), 음악 합성(`audio.py`), 앱 화면 녹화(`record.js`), 프레임 촬영(`capture.js`)이 있습니다. 절차는 [영상 기획 문서](docs/surfaces/product-film.md)에 적었습니다.

## 근거와 검수

- [제품 기준](docs/PRODUCT.md), [콘텐츠 출처](docs/content-sources.md), [첫 화면 방향](docs/surfaces/home.md)
- [디자인 규칙](docs/DESIGN.md), [실행 검증](docs/review/verification.md), [독립 검수](docs/review/finish-review.md)
- 각 WebP의 `.json`에는 기존 자산의 출처를 기록했습니다.
- Jua·SUIT의 SIL OFL 라이선스는 `public/assets/fonts/`에 함께 배포합니다.
- UI 확인은 Phi 에이전트 스페이스에서 수행합니다.

## 배포와 도메인

- `main`에 푸시하면 GitHub Actions가 `public/`을 GitHub Pages로 배포합니다.
- 커스텀 도메인은 저장소의 GitHub Pages 설정에서 관리합니다. `public/CNAME`은 도메인 기록용이며, Actions 배포에서는 이 파일만 바꿔도 설정이 변경되지는 않습니다.
- 아이티이지 DNS: `sunw.kr`의 `hanja`(소개 사이트)와 `hanja-app`(웹 앱) CNAME은 모두 `sunworks-dev.github.io`를 가리킵니다. 2026-10-08에 소개 사이트를 `hanja-app`에서 `hanja`로 옮겼습니다.
- 한자 웹 앱은 앱 저장소(`hanja-study-app`)가 `sunworks-dev/hanja-web`으로 배포합니다. 옛 주소 `bryannamd.github.io/hanja-web/`은 마지막 빌드로 남아 있습니다.
- 앱 아이콘은 앱의 최신 `flutter_app/web/icons/Icon-512.png`를 WebP로 변환한 자산입니다.

## 작업 규칙

- 기본 브랜치는 `main`입니다.
- 공개 가능한 사이트 코드와 자산만 저장합니다.
- 환경 변수는 Git에서 제외합니다. 필요한 변수 이름은 실제 값을 넣지 않은 `.env.example`로 공유합니다.
- 계획·설계·연구·보고·인계 문서는 `docs/` 아래에 작성합니다.
- 변경 사항과 검증 결과는 Pull Request에 기록합니다.

## 기본 설정 파일

- `.editorconfig`: 들여쓰기, 문자 인코딩, 줄바꿈 규칙
- `.gitattributes`: Git 줄바꿈 규칙
- `.gitignore`: 환경 변수, 의존성, 빌드 결과물, 로컬 설정 제외
- `.github/pull_request_template.md`: 변경 내용과 검증 기록 양식

## 손글씨 체험 검증

앱에서 가져온 明·木 획순과 같은 채점 기준을 사용합니다. 입력·재생은 `public/writing-demo.mjs`, 순수 채점은 `public/stroke-scorer.mjs`입니다.

```sh
node --test tests/writing.test.mjs
```

앱과의 대조 결과·fixture 재생성은 [손글씨 검증 기록](docs/review/writing-demo-2026-10-03.md), 포팅 결정은 [ADR](docs/decisions/adr-app-writing-demo-2026-10-03.md)에 있습니다.
