# 구현 검증 · 2026-10-02

## 환경

Phi 공식 runner, `hanja-site-build` Agent Space. 로컬 정적 서버에서 확인. 일반 사용자 탭과 다른 브라우저는 사용하지 않았다.

## 확인 결과

- 1440 / 1428(실제 창) / 768 / 390 / 320px: 가로 스크롤 넘침 없음, 모든 이미지 로딩 완료.
- Jua와 SUIT 글꼴 로딩 완료. 최종 새 탭에서 console warning/error 0, 실패한 네트워크 요청 0.
- 연상 체험: 연결 → 오답 안내 → 정답 → 다음 체험 포커스 → 초기화, 실제 클릭 검증.
- 손글씨: 포인터로 그린 뒤 캔버스 픽셀 존재 확인, 4획 모두 그려짐(16,368 alpha 픽셀), 지우기 후 빈 캔버스 확인.
- 어휘 탭: 클릭 후 ArrowRight로 ‘문명’ 이동, 선택 상태·문구·포커스 일치.
- 가격 FAQ: 실제 클릭으로 열림·닫힘 확인.
- 모션 감소 설정: media query true, 전환 0초, 스크롤 auto 확인.
- HTML의 중복 ID·잘못된 내부 앵커·없는 로컬 파일·누락된 이미지 alt 없음. JS 문법 검사·git diff --check 통과.
- 배포 이미지 10개 모두 출처 메타데이터 보유. 폰트 라이선스 포함. 전체 공개 파일 약 580KB(디스크 블록 크기 제외).

## 검증 범위와 환경 제한

- Phi가 `style#phi-agent-page-theme`를 삽입해 제목·링크를 파란색으로 덮어쓴다. 캡처는 이 환경 그대로이며, 원본 색상 캡처로 표현하지 않는다. 검수 탭에 한정한 비활성화 요청이 자동 승인 검토에서 ‘페이지 변형 금지’로 거절되었다. 사용자에게 제한된 허용을 요청했으며 아직 응답 대기 중이다. 브라우저 설정이나 DOM 스타일을 우회 변경하지 않았다.
- 원본 CSS의 대비 계산: 본문 10.92:1, 보조 본문 5.86:1, 주 CTA 5.24:1, 녹색 배경 글자 9.20:1, 짙은 배경 본문 8.33:1, 어휘 카드 보조 글자 5.81:1. 브라우저 색상 덮어쓰기 상태의 전체 대비 통과를 주장하지 않는다.
- Impeccable 정적 detector는 파서 모듈 부재로 regex 모드였다. 보고된 항목은 0이나 계산된 색상·커스텀 속성 분석은 포함되지 않는다. `detector.json` 참조.
- 화면 크기 모의 설정에서 일부 자동 스크롤/클릭 좌표가 불안정했다. 최종 기능 검증은 실제 창 크기에서 수행했다. 실제 iOS/Android 기기의 터치 테스트를 수행했다는 주장은 하지 않는다.
- GitHub Pages의 custom domain DNS health는 valid/HTTPS eligible, CAA 오류 없음. 인증서 상태 `new`여서 HTTPS는 아직 발급 대기 중이다. 기능 검증과 별개의 배포 환경 상태다.

## 캡처

`desktop.png`, `mobile.png`, `width-768.png`, `width-320.png`, `user-1428.png`는 전체 페이지, `hero-1440.png`·`hero-390.png`는 첫 화면이다. 별도 `demo-success.png`·`writing-complete.png`는 동작 확인용이다. PNG는 로컬 검수 자료이며 Git에서 제외한다.

## 독립 검수 수정

첫 독립 검수 `fix`: 320px에서 쓰기·제작자 이야기의 그림이 문구를 가림. 560px 이하에서 쓰기 설명은 텍스트/그림 그리드, 이야기 그림은 제목 다음 행으로 배치했다. 동일 5개 폭 재촬영, scrollY=0·이미지 로딩 완료·가로 넘침 없음 확인. 320px의 쓰기 문구 오른쪽 165px, 그림 왼쪽 179px(14px 분리); 이야기 제목 하단 6138.5px, 그림 상단 6156.5px(18px 분리). 독립 검수의 최종 수정 판정은 `resolved`, disposition은 `ship`. [검수 기록](finish-review.md) 참조.

## 운영 배포 확인 · 20:46 KST

- 구현 커밋 `857fd9a`의 [GitHub Pages 배포](https://github.com/sunworks-dev/hanja-study-site/actions/runs/37002685093) 성공.
- `http://hanja-app.sunw.kr/`에서 공개 파일 31개 모두 HTTP 200, 로컬 파일과 SHA-256 일치.
- 동일 Phi Agent Space의 새 운영 탭에서 제목·첫 화면·기존 웹앱으로 연결되는 CTA 3개·글꼴 로딩 확인. 1428px에서 가로 넘침 없음, console warning/error 0, 실패 요청 0. `production.png`에 해당 화면 기록.
- HTTPS는 인증서 `new`, 강제 HTTPS `false`로 발급 대기. HTTP 확인을 TLS 검증으로 취급하지 않았다.
