# 앱 손글씨 체험 반영·검증 · 2026-10-03

## 변경

| 이전 | 변경 |
|---|---|
| 木 글꼴 위 낙서 | 앱의 明·木 SVG 윤곽·중심선·글자 맞춤 좌표 |
| 채점 없음 | 앱의 방향·Fréchet 기준, 3회 재시도, 도움/직접 성공 구분 |
| 한 획 보기·지우기 | 3모드, 한 획/연속 재생, 일시정지, 3단계 속도, 다시 쓰기 |
| 조합 뒤 별도 木 체험 | 조합한 明을 바로 따라 쓰는 링크 |
| 일반 안내 | 획 진행, 원인별 피드백, 정확도, 기록 미저장, 출처·라이선스 |

## 실행 검증

- `fvm flutter test /tmp/hanja-writing-parity_test.dart test/handwriting/stroke_scorer_test.dart --reporter expanded`: 11 통과(임시 추출 검사 1 + 기존 scorer 10).
- `node --test tests/writing.test.mjs`: 5 통과. 明·木 12획 × 정확/역방향/작은 오차/큰 오차/불완전 = 60개 사례의 거리·정확도·판정이 실제 Dart 값과 일치(허용 오차 1e-8). 좌표 변환도 대조.
- Phi Agent Space `hanja-site-learning-review`에서 데스크톱 및 320×844·390×844 확인. 사용자 Space 미사용.
- 마우스로 木 4획 완성(100%), 역방향 재시도 안내 확인. 明 1획을 3회 역방향으로 입력 후 나머지를 완성하여 ‘7획 스스로·1획 도움, 88%’ 확인.
- 320px에서 가로 넘침 없음, 터치 1획 성공. 터치 취소는 획 진행에 반영되지 않음.
- 혼자 쓰기 초기화, 획순 1획 재생, 연속 재생/일시정지/다시 쓰기, 모션 감소+Space 키로 2획 진행 확인.
- 네트워크 차단 시 로드 실패 문구와 글자 버튼 재시도 복구 확인. 실패 주입 중 발생한 오류와 정상 로드 오류를 구분했다.
- 최종 정상 로드에서 콘솔 오류·경고 0, 실패 네트워크 요청 0. 조합 정답에서 明 따라 쓰기 연결·기존 어휘 탭 전환 확인.
- DESIGN.md 기존 clamp 차원 표현 3개를 최대값+반응형 설명으로 정규화해 lint 오류를 해결했다(CSS 시각 변화 없음).
- 실제 iOS Safari·Android·VoiceOver/TalkBack 검증은 미실시. 공개 사이트 배포는 하지 않음.

## 재현

기존 앱 scorer가 바뀌면 앱의 `flutter_app/`에서:

```sh
HANJA_SITE_EXPORT_DIR=/tmp/hanja-writing-export fvm flutter test /absolute/path/to/hanja-study-site/scripts/export-app-writing_test.dart
```

출력 디렉터리는 미리 생성한다. `glyph-fits.json`의 값을 해당 공개 JSON의 `fit`에 적용하고, 원본 앱의 `strokes`·`medians`·`radStrokes`를 동기화한다. `tests/app-scorer-fixtures.json`을 갱신한 뒤 Node 검사를 수행한다. 훈음은 앱 seed, 획 설명은 실제 획 모양과 대조한다. 글꼴은 `scripts/subset-fonts.py`로 재생성한다.

## 배포 전 상태

소개 사이트 원본 HTTPS 접속은 `net::ERR_CERT_COMMON_NAME_INVALID`, HTTP는 정상으로 확인했다. 도메인 인증서 설정은 변경하지 않았다. 출처 데이터는 [Make Me a Hanzi](https://github.com/skishore/makemeahanzi)의 그래픽 데이터이며 앱에 포함된 ARPHICPL 전문을 복사했다.
