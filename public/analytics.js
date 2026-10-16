// 방문 통계(PostHog). 쿠키·브라우저 저장소를 쓰지 않는 cookieless 모드로만 켠다.
// 개인정보 처리방침의 "소개 사이트 방문 통계" 절과 함께 고친다.
// 프로젝트에서 "Cookieless server hash mode"를 켜야 이벤트가 버려지지 않는다.
(function () {
  // 공개용 프로젝트 토큰(브라우저에 그대로 노출되는 값). EU 지역 프로젝트.
  var TOKEN = 'phc_ADcEwVKa4sBi6pnihazp8TQjcGgQiNyTWSTZPWzqFAY4';

  // prettier-ignore
  !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],Object.defineProperty(u,"toString",{configurable:!0,enumerable:!0,writable:!0,value:function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e}}),Object.defineProperty(u.people,"toString",{configurable:!0,enumerable:!0,writable:!0,value:function(){return u.toString(1)+".people (stub)"}}),o="init capture register register_once register_for_session unregister unregister_for_session getFeatureFlag getFeatureFlagResult isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey getNextSurveyStep identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty createPersonProfile opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing debug".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);

  window.posthog.init(TOKEN, {
    api_host: 'https://eu.i.posthog.com',
    defaults: '2026-08-30',
    cookieless_mode: 'always',
    // 개인 프로필을 만들지 않는다(identify는 무시된다).
    person_profiles: 'never',
    // 화면 녹화·설문은 쓰지 않는다(쿠키 없는 모드에서도 꺼진다).
    disable_session_recording: true,
    disable_surveys: true,
  });
})();
