# 제품 영상·사이트 개편 검증 · 2026-10-03

## 산출물

- 영상: 가로 1920×1080 / 세로 1080×1920, 각각 32.000초,30fps,H.264+AAC. 파일 7,852,876 / 7,558,585 bytes. 기존 영상·표지·자막을 교체하고 새 파일 이름으로 캐시 혼동 방지. GitHub Pages의 기존 JS 응답 max-age=600을 확인해, 변경된 JS/CSS/글꼴 URL에도 버전 쿼리를 붙여 이전 플레이어가 오래된 영상 주소를 고르지 않도록 했다.
- 독자적으로 합성한 120 BPM 음악·효과음. 인코딩된 음량 mean -16.6dB,max -1.3dB,클리핑 없음.
- 실촬영 앱 화면은 기기 안에 그대로 유지, 편집 속도 안내 포함. 7/13/17/21초 장면 이동과 한국어 설명 자막 제공.

## Phi Agent Space QA

Space `hanja-product-film`, kind `agent`, ID `3C4C9B8E-FBB8-4E43-9CC4-6BBFBADD15A3`. 사용자 탭·다른 브라우저 사용 없음. 자체 검수 2회 묶음, 수정은 사이에 반영. 일부 파란색은 Phi의 주입 테마이며 사이트 CSS 색상과 구분.

- 1440×1000,820×1000,390×844,320×740 점검. 가로 넘침 없음. 전체/주요 구간 캡처를 직접 열어 유효성 확인.
- 최종 순서: 제품·대상 → 영상 → 기능 → 가격 → 시작 방법 → 직접 체험 → 쓰기·어휘 → 제작자 이야기 → 접힌 상세 설계·익명 후기 → FAQ → 마무리.
- 4개 기능 탭: 클릭·방향키 이동·선택 상태·포커스·캡처 확대 링크 일치.
- 가격 예정·일회 구매·체험·스토어 준비 중 표시, 개인정보 링크 및 기기별 기록 안내.
- 접기/펼치기 및 `#memory` 직접 진입 시 부모 details 자동 열림, `#faq-records` 진입 시 해당 답 열림.
- 데스크톱/모바일 각각 다른 영상 소스 재생 확인. 모바일 duration32,currentTime 증가,17.25초 장면 이동 확인. 화면 밖 이동 시 일시 정지. 감소 모션 설정에서 자동 재생 없고 preload none.
- 기존 연결 체험 성공 상태, 획순 시연 시작·상태 안내, 어휘 탭 ‘문명’ 변경 확인.
- 콘솔 오류·경고0, 실패/4xx/5xx 네트워크0.

## 정적 검증

- `node --check public/app.js public/showcase.js` 각각 통과.
- HTML 중복 ID0, 깨진 내부 앵커0, 누락 자산0. `git diff --check` 통과.
- self-hosted 글꼴 subset 재생성.
- asset provenance scan:17rasters,0missing.
- Impeccable detector는 이번 변경에서1회 실행. parser 모듈 부재로 regex fallback이며 computed contrast/selector 계산은 하지 못함. 239개 모두 advisory: 기존 DESIGN 타입 단계·색상·반경 기록과의 불일치. 전체 자동 검수 통과라는 의미가 아님. 검수자에게 원본 JSON 전달.

## 독립 검수·배포

- 새 독립 검수자 `/root/motion_site_finish_review`: 필수 캡처15개 유효, 내용 순서·모바일·새영상의 시각 근거 적합. 유일한 material fix는 DESIGN 문서 동기화. 음악 청취·실시간 영상 감상은 독립 검수 범위 밖.
- 기능 보완 검증: 같은 해시로 재방문해도 FAQ가 다시 열림. 실제 화면 크게 보기를 눌러 Agent Space 새 탭의 원본 WebP 로드 확인.
- 독립 documenter의 문서 동기화 후 동일 검수자가 유일한 수정 항목 resolved, remaining clear, disposition ship으로 판정. 이 후속 판정 범위는 문서 동기화에 한정.
- 배포 커밋 `9496882be914806aa5cd5cdf87aaf06cdb51e896`. [GitHub Actions run37104552390](https://github.com/sunworks-dev/hanja-study-site/actions/runs/37104552390) success.
- 공개 HTTP 사이트의 HTML/CSS2종/쇼케이스JS/자막이 로컬 배포본과 byte 단위로 일치. 가로·세로 MP4 모두 Range 요청206, 파일 전체 크기 일치.
- 공개 사이트 Phi 모바일 재생:1080×1920,duration32,currentTime1.819558,playingtrue. 장면 이동 정상, 콘솔 오류·경고0, 실패 네트워크0. `motion-production.png`, `motion-production-film.png` 확인.
- 작업 Agent Space는 `complete()`로 정리함.
- 별도 잔여 사항: GitHub Pages HTTPS certificate state `new`, `https_enforced:false`. 맞춤 도메인의 인증서 발급은 완료되지 않았으며 HTTPS 복구를 주장하지 않음.
