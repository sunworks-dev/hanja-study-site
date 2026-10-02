# hanja-study-site

`hanja-study-app` 출시 안내와 제품 소개를 위한 웹사이트 저장소입니다.

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
