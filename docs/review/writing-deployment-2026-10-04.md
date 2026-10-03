# 손글씨 체험 배포·HTTPS 복구 점검 · 2026-10-04

## 배포·기능

- 구현 커밋 `4d503d3a0ce07de572aa6cd5561f083d8b3e4860` (`feat: 앱 손글씨 체험 적용`)을 `main`에 푸시했다.
- [최초 배포](https://github.com/sunworks-dev/hanja-study-site/actions/runs/37156315844) 성공. Pages 재구성 뒤 [재배포](https://github.com/sunworks-dev/hanja-study-site/actions/runs/37157539364)도 성공.
- Phi Agent Space `hanja-composition-release`에서 프로덕션 HTTP 페이지의 새 明/木, 따라 쓰기/혼자 쓰기/획순 보기 조작 확인. 실제 포인터로 木 4획을 모두 직접 써서 100% 완료했다.
- 60개 Dart 실행 결과와 JS 채점 일치, 도움 판정, 탭 제외, 재시작, 앱 좌표를 검증하는 Node 테스트 5개 통과.
- 공개 HTML/CSS/JS/MJS의 `http://` 리소스 참조 없음. 기존 법적 고지·앱 연결 유지.

## HTTPS 진단·수행

- 기존 `docs/legal-review-2026-10-03.md`와 과거 감시 로그를 보면 2026-10-02부터 발급 미완료였다.
- 권위 DNS `ns1.ksdom.kr`·`ns2.ksdom.kr`, 공개 리졸버 1.1.1.1·8.8.8.8 모두 `hanja-app.sunw.kr CNAME sunworks-dev.github.io.` 확인. GitHub IPv4/IPv6 외 충돌 주소와 CAA 제한을 발견하지 못했다.
- GitHub Pages DNS health 결과: `dns_resolves:true`, `is_valid:true`, `is_https_eligible:true`, `is_served_by_pages:true`, `caa_error:null`.
- HTTP는 200. TLS는 서버가 `*.github.io` 인증서를 제공해 호스트명이 일치하지 않는다. `curl`은 인증 검증을 켠 상태에서 오류 60. 검증 우회로 성공 처리하지 않는다.
- 2026-10-04 06:46~06:47 KST: 공식 문서의 도메인 제거·동일 값 복원 절차로 재요청. 07:10까지 `https_certificate.state:new` 상태 유지.
- 이전 재요청도 실패한 기록을 확인해 07:10 KST에 Pages 설정을 보관하고 이 저장소의 Pages 설정만 제거·동일 `workflow`, `main`, `/`, 맞춤 도메인으로 재생성했다. 저장소·소스·DNS는 삭제하지 않았다. 07:11 KST 재배포 및 HTTP 200 확인.
- 발급이 `approved`로 바뀌면 `https_enforced:true` 적용 후 실제 TLS 검증을 수행하도록 이 작업의 감시 프로세스를 실행했다. 발급 완료는 아직 확인하지 못했다.

## 지원 요청 초안 — 미발송

**Subject:** GitHub Pages TLS certificate stays in new despite valid DNS and recreated Pages configuration

Repository: https://github.com/sunworks-dev/hanja-study-site
Custom domain: hanja-app.sunw.kr

The domain has served HTTP successfully since October 2, 2026, but HTTPS still serves the default *.github.io certificate and fails hostname verification. The Pages API reports https_certificate.state=new and https_enforced=false.

The completed DNS health check reports dns_resolves=true, is_valid=true, is_https_eligible=true, is_served_by_pages=true and caa_error=null. Authoritative and public resolvers agree on the CNAME to sunworks-dev.github.io with the expected Pages addresses. There are no conflicting address records or CAA restrictions.

Removing and re-adding the domain on October 3 did not advance issuance. On October 3 at 22:10 UTC, we backed up and recreated this repository's Pages configuration with the same workflow source and custom domain, then successfully deployed commit 4d503d3. The certificate is still new. Please investigate the certificate provisioning job and manually re-trigger or complete issuance. Please preserve the current domain and repository deployment configuration.

## 공식 근거

- [GitHub HTTPS·발급 재요청](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https)
- [GitHub 맞춤 도메인 문제 해결](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/troubleshooting-custom-domains-and-github-pages)
- [Pages 설정·DNS health REST API](https://docs.github.com/en/rest/pages/pages)
