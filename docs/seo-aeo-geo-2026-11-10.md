# 어흥!한자 검색·답변·AI 인용 기반 개선

2026-11-10 로컬 구현 및 검증 완료. 커밋·배포·색인 제출은 하지 않았다. 검색 순위, 설치율, AI 추천·인용 개선은 아직 측정하지 않았다.

## 진단과 변경

| 영역 | 변경 전 | 변경 후 |
| --- | --- | --- |
| SEO | 정적 HTML, canonical, 사이트맵, 정상 404 보유. H1은 브랜드·급수 없이 감성 문구만 표시 | 기존 디자인 안에서 H1에 어흥!한자·8급~1급·한자 공부 앱 표시. 제목·설명에 급수 정보와 시험 일정 반영 |
| AEO | 홈 FAQ 11개, 이용·기능 중심 | 8급 독학·2급 준비·기출 자료·시험 일정 질문 4개 추가. 화면에서 추출한 동일 문구로 FAQPage 생성 |
| GEO | 급수 안내 15페이지, 출처·확인일, llms 파일 보유 | 홈에 공식 데이터 기반 주요 7개 급수 비교표, 안내 페이지에서 설치 안내 연결, WebPage와 앱·회사 엔티티 연결 |
| LLMO | 공식 표기 어흥!한자와 회사 @id 있음 | 공식 브랜드 유지, llms.txt·llms-full.txt에 화면 FAQ 동기화 |
| 네이버 | Yeti 허용, sitemap·IndexNow 키 존재 | 크롤링 정책 유지. 소유 확인·수집 실적은 미조회 |
| 콘텐츠 | 급수별 배정한자·시험 일정 페이지 운영 중 | 중복 페이지를 만들지 않고 홈과 기존 안내를 연결. 다음 콘텐츠는 실제 유입 검색어 확인 후 결정 |

`public/index.html`은 메타·H1·FAQ 원본이다. 홈 비교표는 `scripts/build-pages.py`가 `data/kccpt-official.json`에서 생성한다. JSON-LD와 llms의 FAQ도 홈에서 추출한다. 생성 파일을 직접 수정하지 않는다. `GUIDE_UPDATED`는 설치 안내의 실제 수정일이며 공식 자료 확인일 `checked`와 구분한다. 새 문구를 포함해 Jua·SUIT 서브셋을 재생성하고 홈의 글꼴·CSS 캐시 버전을 갱신했다.

앱 퀴즈를 공식 기출문제로 소개하지 않는다. 기출 원문은 한국어문회로 안내한다. 근거 없는 최고 추천·단기 합격·효과 수치나 키워드 반복은 넣지 않았다. 브랜드 독점권·상표권 검토는 이번 작업에 포함하지 않았다.

## 근거

- [한국어문회 급수 배정](https://www.hanja.re.kr/kccpt/exam/levelConfirm.do), [합격 기준](https://www.hanja.re.kr/kccpt/exam/successRule.do): 2026-11-10 원문 대조. 새 비교표의 배정한자 수·문항 수 일치. 다른 원자료 항목까지 재확인한 것은 아니므로 기존 전체 데이터 확인일 2026-10-17은 유지했다.
- [Google AI 기능 안내](https://developers.google.com/search/docs/appearance/ai-features): 기본 SEO, 공개 텍스트, 내부 링크, 가시 콘텐츠와 일치하는 구조화 데이터가 기준. 별도 AI 파일·특수 스키마는 필수 요건이 아니다. llms 파일은 보조 안내로 취급한다.
- [Google 문서 변경 이력](https://developers.google.com/search/updates): 2026-05-08 기록은 2026-05-07부터 FAQ 리치 결과가 표시되지 않는다고 명시한다. FAQPage 구현은 검색 결과의 접이식 FAQ 노출을 약속하지 않는다.
- 제품의 출시 상태는 현재 홈·생성 스크립트와 회사 저장소의 최신 PRODUCT/AGENTS 확인값을 사용했다. 한자 `docs/PRODUCT.md`의 출시 전 문구는 과거 기록으로 남아 있다.

## 검증

- 변경 전 운영 사이트: 홈·robots.txt·sitemap.xml·llms.txt HTTP 200, 임의 없는 URL HTTP 404. 홈 meta/header noindex 없음. robots에서 검색 및 AI 크롤러 허용. 원문 증거 `/tmp/sunworks-seo-before/`.
- 변경 후 사이트맵 22개 HTML: canonical·title·description·H1·색인 허용·JSON-LD 파싱 확인.
- 전체 FAQ 62개 답변과 화면 HTML 일치. 홈 FAQ 15개가 llms에도 포함됨. 급수 비교표 숫자는 JSON 원본과 일치.
- `python3 scripts/build-pages.py` 성공. 동일 입력 재실행 시 생성 결과 해시 동일.
- `curl http://127.0.0.1:4322/` 원문에 새 내용·FAQ·JSON-LD 존재. `git diff --check` 통과.
- ego-lite TaskSpace 3에서 홈을 390px·1440px로 확인. 가로 넘침 없음. 모바일 FAQ 열기와 2급 페이지 설치 안내 배치 확인. 화면 기록 `docs/review/seo-hanja-*.png`는 로컬 검증 파일로 Git에서 제외된다.
- 설치 안내는 기존 `/#download`와 실제 스토어 링크로 연결된다. 앱 설치·결제 자체는 실행하지 않았다. 기존 미추적 파일 `docs/review/https-recovery-2026-10-04.json`은 수정하지 않았다.

## 측정과 남은 작업

배포일 +14일에 재측정한다. 2026-11-10 배포 시 목표일은 **2026-11-24**다. 자동 예약은 하지 않았다.

1. 배포 후 홈·급수 페이지·사이트맵 HTTP 응답과 noindex를 다시 확인하고 Google Search Console, Bing Webmaster Tools, 네이버 서치어드바이저의 소유 확인·사이트맵 제출 상태를 확인한다. 미배포 URL에 대한 IndexNow 제출은 하지 않았다.
2. 최근 28일의 노출·클릭·CTR·색인 URL 수를 내려받아 기준선으로 보관한다. 계정 지표·서버 봇 로그는 이번에 조회하지 않았다. 미조회는 0이 아니다.
3. 같은 조건으로 ‘초등학생 한자 8급 독학 앱’, ‘한자능력검정시험 2급 공부법’, ‘8급 배정한자’, ‘한국어문회 시험 일정’, ‘어흥!한자’ 질문의 ChatGPT 검색·Gemini·Perplexity·네이버 AI 출처 URL과 답변 날짜를 기록한다. 현재 인용 여부는 미측정이다.
4. 기존 PostHog에서 홈/급수 안내 유입과 스토어 링크 클릭을 비교한다. 스토어 클릭은 설치 완료가 아니다. 설치 전환율은 App Store Connect·Play Console 유입 지표와 함께 판단한다. 새 추적 SDK나 개인정보 수집 항목은 추가하지 않았다.
5. 집계 지연을 고려해 마지막 2~3일은 제외하고 비교한다. 날짜가 다른 시험 일정은 원문 변경 여부를 먼저 확인한다.
