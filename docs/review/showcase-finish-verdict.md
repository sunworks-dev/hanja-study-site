## verdict

동일 경로의 최신 필수 캡처 9개 모두 유효. 이번 판정은 최초 검수의 material fix 1–4만 대상으로 한다.

1. **resolved — 모바일 기능 탐색:** 최신 `showcase-mobile-features.png`에서 선택된 ‘성장이 눈앞에’ 탭과 실제 도감 화면이 같은 뷰포트에 보인다. 전체 모바일 캡처도 탭 → 화면 → 설명 순서를 확인시킨다. 긴 설명·목록·CTA가 화면 앞을 막지 않는다.
2. **resolved — 문서 지속성:** `docs/DESIGN.md`, `docs/DESIGN.md.json`, `docs/surfaces/home.md`가 최종 히어로·영상·기능 탭·모바일 배치·가격·SVG 체계를 기록한다. 기존 팔레트·seed·schemaVersion 2를 보존했고 YAML/JSON, 컴포넌트 참조, 8개 정식 섹션 순서 검증을 통과했다. 에이전트 슬롯 제한으로 같은 검수자가 문서화 역할만 순차 수행했으며 UI 작성에는 참여하지 않았다.
3. **resolved — 글리프 아이콘:** 최신 전체 캡처의 링크·FAQ가 기존 문맥과 정렬을 유지한다. 수정 소스에서 외부 링크와 FAQ 6개의 인라인 SVG, 모바일 후기의 글리프 제거를 확인했다. 학습식의 더하기는 유지된다.
4. **resolved — 모바일 문장 공백:** `showcase-mobile-hero.png`와 `showcase-320.png`에서 ‘복습해요. 아이의’가 정상적으로 띄워진다.

## remaining

clear — 수정 배치가 만든 회귀는 제공된 캡처에서 발견되지 않았다. 이 ship 판정은 검수한 네 수정 사항의 해소 범위에 한정한다.

disposition: ship
