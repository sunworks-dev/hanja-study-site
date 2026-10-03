# 법적 고지·HTTPS 점검 · 2026-10-03

## 범위와 판단

사용자가 제공한 이미지의 사업자정보·개인정보 처리방침·통신판매업·고객문의·호스팅사·이용약관·취소 및 환불 항목을 공식 자료와 대조했다. 사이트는 앱 소개·웹 베타 연결을 제공하며, 현재 코드에 주문·결제·가입·문의 폼이 없다. 이를 근거로 법률상 모든 의무가 면제된다고 판단하지 않는다. 이미지의 ‘누락은 곧 중죄’라는 표현 역시 법률 판단으로 채택하지 않는다.

| 항목 | 공식 기준 | 반영 및 남은 확인 |
| --- | --- | --- |
| 사업자 신원 | 전자상거래법 제10조, 시행규칙 제7조: 대상 사이버몰 초기 화면에 신원, 약관 등 표시·사업자정보 공개페이지 연결 | 확인된 브랜드·연락 주소·호스팅 추가. 법적 상호, 대표자, 주소, 전화, 사업자등록번호는 사용자 입력 대기. 가짜 값이나 등록 완료 표시 없음 |
| 통신판매업 | 제12조 신고, 제13조 표시·광고 시 신고번호·신고기관 등 | 신고 여부·면제 해당 여부는 자료가 없어 판단 보류. ‘무료 베타니까 자동 면제’라고 쓰지 않음 |
| 개인정보 | 개인정보 보호법 제30조, 개인정보위 2026 작성지침 | 소개 사이트 처리 현황과 앱의 기존 방침을 분리. 문의 메일 운영·보관·위탁·국외 처리 및 보호 담당자 미확인. 완성된 처리방침이라고 표시하지 않음 |
| 고객문의 | 전자상거래법 제10·13조, 개인정보 보호법 제30조 | 기존 owner 확정 주소 support@sunworks.kr 유지. MX 레코드가 없어 실제 수신 확인 필요 |
| 호스팅사 | 시행령 제11조의4 | GitHub, Inc. (GitHub Pages) 표시, GitHub의 IP 보안 로그와 해외 처리 안내 출처 연결 |
| 이용약관 | 제10·13조 | 소개 사이트 열람·체험 범위 약관. 유료 앱 계약 또는 기존 앱의 약관을 대신하지 않음 |
| 취소·환불 | 제13·17·18조 | 현재 결제 없음과 판매 준비 상태, 청약철회·디지털콘텐츠 예외의 조건·하자·미성년자·환급 법정 기준을 구분. 일괄 환불 거절 조항 없음 |

이 작업만으로 법률 준수 완료를 보증하지 않는다. 실제 판매·개인정보 처리 절차와 공개 문구가 같아야 한다. 사업자 정보를 받으면 초기 화면 푸터에도 표시하고 신고 정보 확인 링크를 추가한다. 통신판매업 신고 면제는 사업자등록·신원 표시·개인정보 의무 전체의 면제가 아니다.

## 확인한 공식 출처

모두 2026-10-03 확인. 미래 시행 조항을 현재 의무로 적용하지 않았다. 법령명만 검색한 오래된 조문·연혁은 현행 근거로 사용하지 않았다.

- [전자상거래법 제10조](https://law.go.kr/LSW/lsLinkCommonInfo.do?chrClsCd=010202&lsJoLnkSeq=1029561875): 2026-07-21 시행, 법률 제21312호.
- [전자상거래법 제12·13조](https://law.go.kr/lsLawLinkInfo.do?chrClsCd=010202&lsJoLnkSeq=1013449467): 신고·신원·거래조건·미성년자 계약.
- [시행령 제11조의4](https://law.go.kr/lsLinkCommonInfo.do?chrClsCd=010202&lspttninfSeq=63473): 2026-07-21 시행, 대통령령 제36507호. 과거 제11조의3과 혼동하지 않음.
- [전자상거래법 시행규칙 제7조](https://www.law.go.kr/LSW/lsLawLinkInfo.do?chrClsCd=010202&lsJoLnkSeq=900616963): 2026-07-21 시행, 총리령 제2136호. 초기 화면 표시와 사업자정보 공개페이지 연결.
- [전자상거래법 제17조](https://www.law.go.kr/LSW/lsSideInfoP.do?docCls=jo&joBrNo=00&joNo=0017&lsiSeq=282793&urlMode=lsScJoRltInfoR): 청약철회 기간과 디지털콘텐츠 제한 전 필요한 조치.
- [전자상거래법 제18조](https://www.law.go.kr/LSW/lsSideInfoP.do?docCls=jo&joBrNo=00&joNo=0018&lsiSeq=282793&urlMode=lsScJoRltInfoR): 환급 시점·기한과 결제취소·지연 의무.
- [개인정보 보호법 제30조](https://www.law.go.kr/lsLinkCommonInfo.do?lsJoLnkSeq=1029331583): 2026-09-11 시행, 법률 제21445호. 처리 목적·보유 기간·파기·권리·연락처 및 해당 시 위탁 등.
- [개인정보위 2026 작성지침 개정 안내](https://pipc.go.kr/np/cop/bbs/selectBoardArticle.do?bbsId=BS074&nttId=12021): 외부 전송 없는 단말 내부 처리에도 처리 사실과 삭제 기준 안내 권장.
- [GitHub Pages 데이터 수집](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages#data-collection): 방문자 IP를 보안 목적으로 기록·보관.
- [GitHub 개인정보 처리방침](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement): 2026-04-27 시행. 미국 등 해외 처리, 보관 원칙, 권리 행사.
- 앱 정본: `../../apps/hanja-study-app/docs/PRIVACY_POLICY.md` 및 [공개 앱 처리방침](https://bryannamd.github.io/hanja-web/privacy.html). 소개 사이트에서 앱의 방침을 복제·변경하지 않음.

## 사이트 코드 조사

`public/index.html`, `app.js`, `showcase.js`에서 폼·업로드·분석 SDK·추적 코드·쿠키·localStorage·sessionStorage·IndexedDB 사용 없음 확인. 영상·자막·이미지·글꼴은 사이트 파일이다. 외부 링크 이동과 호스팅사의 접속정보 처리는 별도다. 문의 이메일 발신 주소와 본문도 개인정보가 될 수 있으므로 ‘모든 개인정보 수집 없음’으로 일반화하지 않았다.

## 사용자 입력 대기

1. 실제 사업자등록·통신판매업 신고 상태, 공개할 상호·대표자·주소·문의 전화·등록번호·신고번호.
2. 수신 가능한 문의 이메일, 메일 서비스, 보관·삭제 기준 및 개인정보 보호 담당자.

문의 메일 위탁·국외 처리·보관기간은 운영자 확인 없이 임의로 만들어 게시하지 않는다. `privacy.html`은 확인된 기술적 처리 현황이며 문의의 완결된 개인정보 처리방침이 아니다.

## HTTPS 및 메일 진단

- 시작 시 GitHub Pages 인증서 `state: new`, `https_enforced: false`. 2026-10-02부터 발급 미완료.
- CNAME `hanja-app.sunw.kr → sunworks-dev.github.io` 정상. CNAME 대상의 CAA에 `letsencrypt.org` 허용, sunw.kr 상위 CAA 제한 없음.
- HTTP 200. HTTPS는 curl 60, 인증서의 대상 도메인 불일치. 인증 검증을 우회하지 않음.
- 2026-10-03 22:50 KST: [GitHub 공식 절차](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https#troubleshooting-certificate-provisioning-certificate-not-yet-created-error)에 따라 CNAME을 API로 제거하고 즉시 같은 값으로 복원해 발급 재요청. 복원 확인, 반복 초기화하지 않음.
- GitHub DNS health API는 202와 `{}` 반환. 이번 조회에서 `valid` 응답을 받았다고 주장하지 않음. [GitHub Status](https://www.githubstatus.com/api/v2/status.json)는 전체 정상으로 표시.
- Phi 전용 Agent Space `hanja-site-legal-https`에서 Pages 설정 UI 확인 시 로그인되지 않은 상태. 인증된 `gh` API로 설정 작업 수행. 일반 사용자 탭·쿠키·인증 토큰을 브라우저로 옮기지 않음.
- `sunworks.kr` MX: Cloudflare 1.1.1.1·Google 8.8.8.8 모두 NOERROR, MX 응답 0. 수신 가능한 메일 서비스 확인 전 임의 DNS 변경·테스트 메일 발송 없음.

## 구현·검증 상태

운영정보·문의, 소개 사이트 개인정보 안내, 소개 사이트 이용약관, 취소·환불 안내의 정적 페이지와 공통 푸터를 작성했다. 기존 앱 소개·영상·체험은 보존한다. 폰트 서브셋 입력을 모든 공개 HTML/CSS/JS/VTT로 넓혀 새 안내 문구도 포함한다. 최종 검증·배포 결과는 이 문서에 이어 기록한다.

- Phi `hanja-site-legal-https` Agent Space에서 정책 4페이지 × 1440/768/390/320px, 총 16개 조합 확인. 가로 넘침·깨진 이미지·40px 미만 주요 탐색 타깃 없음. 본문 16px.
- 홈페이지 푸터에서 개인정보 안내를 실제 클릭하고 약관·환불·운영정보로 이동 완료. 실제 창 1428px와 모바일 390px 푸터 확인. console warning/error 0, 실패 요청 0.
- HTML 6페이지의 내부 파일·앵커·중복 ID·이미지 alt와 sitemap XML 파싱 통과. 기존 두 JS 문법 검사와 git diff --check 통과.
- Jua/SUIT 서브셋 재생성. 새로운 문구 포함, 각각 112,156/122,472 bytes.
- 디자인 detector 1회 실행. 파서 부재로 regex 모드; 폰트 단계 관련 advisory 13건이며 오류 없음. 읽기 페이지의 의도적 지역 타이포그래피로 기록하며 계산된 색상·대비 통과를 주장하지 않음. `docs/review/legal-detector.json` 참조.
- Phi가 여전히 원본 제목·링크 색상에 자체 테마를 덧씌움. 임의 스타일 변경 없이 해당 환경에서 검증. 캡처는 `docs/review/legal-*.png` (Git 제외).
- 권한 DNS `ns1.ksdom.kr`, `ns2.ksdom.kr` 모두 동일 CNAME 응답. 공개 A/AAAA도 GitHub 공식 IP 4개씩으로 일치.

## GitHub 지원 요청 초안 · 아직 전송하지 않음

외부 지원팀에 메시지를 보내라는 지시는 없으므로 아래 내용을 자동 발송하지 않는다. 재요청 후에도 발급이 진행되지 않으면 사용할 수 있는 진단 초안이다.

**Subject:** GitHub Pages TLS certificate provisioning remains in `new` for hanja-app.sunw.kr

Repository: https://github.com/sunworks-dev/hanja-study-site (public, GitHub Actions deployment)

The custom domain `hanja-app.sunw.kr` has been serving HTTP successfully since October 2, 2026, but HTTPS fails with a certificate hostname mismatch. The Pages API reports `https_certificate.state: new` and `https_enforced: false`.

Both authoritative nameservers (`ns1.ksdom.kr`, `ns2.ksdom.kr`) return `hanja-app.sunw.kr CNAME sunworks-dev.github.io`. The resolved A/AAAA addresses are GitHub Pages' published addresses. CAA permits `letsencrypt.org`; the parent domain has no restrictive CAA records.

Following GitHub's documented procedure, I removed and restored the same custom domain once on October 3, 2026 at 13:50 UTC. The domain was restored successfully, but the certificate remained `new` in subsequent checks. The DNS health endpoint returns HTTP 202 with an empty object, so I cannot obtain a current completed health result. Please check whether the certificate provisioning/DNS verification job is stalled and advise on recovery. No private keys or custom certificates are configured.
