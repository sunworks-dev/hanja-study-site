# hanja-study-site

`hanja-study-app` 출시 안내와 제품 소개를 위한 웹사이트 저장소입니다.

## 사이트 주소

Sunworks에서 새로 만드는 서비스와 소개 사이트는 `sunw.kr`의 하위 도메인을 사용합니다.

| 대상 | 주소 | 상태 |
| --- | --- | --- |
| 한자 앱 소개 사이트 | `https://hanja-app.sunw.kr` | 구축 및 도메인 연결 예정 |
| 기존 한자 웹 앱 | [bryannamd.github.io/hanja-web](https://bryannamd.github.io/hanja-web/) | 현재 배포 유지 |

소개 사이트의 **웹에서 시작하기** 링크는 기존 한자 웹 앱으로 연결합니다.
웹 앱 빌드 결과물은 계속 [`bryannamd/hanja-web`](https://github.com/bryannamd/hanja-web)에 배포합니다.

## 예정 콘텐츠

- 앱 소개와 주요 기능
- 설치·이용 링크와 시작 안내
- 자주 묻는 질문과 지원 안내

## 현재 상태

저장소 초기 설정 단계입니다. 사이트 구현, 기술 스택, 배포 방식은 후속 개발에서 결정합니다.

## 시작하기

```sh
git clone https://github.com/bryannamd/hanja-study-site.git
cd hanja-study-site
```

개발 서버와 빌드 명령은 기술 스택을 정한 뒤 추가합니다.

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
