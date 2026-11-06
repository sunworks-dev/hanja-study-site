"use strict";

// 모바일 하단 고정 안내: 히어로를 지난 뒤에만 보이고, 가격 카드·마지막 안내가 보이면 숨긴다.
(() => {
  const bar = document.querySelector("#sticky-cta");
  const hero = document.querySelector(".product-hero");
  if (!bar || !hero || !("IntersectionObserver" in window)) return;
  try {
    if (sessionStorage.getItem("sticky-cta-closed") === "1") return;
  } catch (error) {
    // 저장소를 못 써도 안내는 그대로 보여 준다.
  }
  document.documentElement.classList.add("has-sticky");
  let heroPassed = false;
  const covered = new Set();
  const update = () => bar.classList.toggle("is-visible", heroPassed && covered.size === 0);
  const heroObserver = new IntersectionObserver(([entry]) => {
    heroPassed = !entry.isIntersecting && entry.boundingClientRect.bottom < 0;
    update();
  });
  const coverObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => (entry.isIntersecting ? covered.add(entry.target) : covered.delete(entry.target)));
    update();
  });
  heroObserver.observe(hero);
  document.querySelectorAll(".price-offer, .closing-section").forEach((el) => coverObserver.observe(el));
  document.querySelector("#sticky-cta-close").addEventListener("click", () => {
    heroObserver.disconnect();
    coverObserver.disconnect();
    bar.classList.remove("is-visible");
    document.documentElement.classList.remove("has-sticky");
    try {
      sessionStorage.setItem("sticky-cta-closed", "1");
    } catch (error) {
      // 이번 방문에서만 닫힌 채로 둔다.
    }
  });
})();

const productFilm = document.querySelector("#product-film");
const filmPlayer = document.querySelector("#film-player");
const filmStatus = document.querySelector("#film-status");
const filmChapters = [...document.querySelectorAll("[data-film-time]")];
const portraitFilm = window.matchMedia("(max-width: 560px)");
let pendingFilmTime = null;
let filmStarted = false;
// The cover is the only play control until playback starts; native controls stay in HTML as the no-JS fallback.
productFilm.controls = false;

function chooseFilm() {
  // Never swap a loaded film during playback or restart a user's position.
  if (filmStarted) return;
  const orientation = portraitFilm.matches ? "portrait" : "landscape";
  productFilm.querySelector("source").src = `assets/video/hanja-motion-${orientation}.mp4?v=20261007c`;
  productFilm.poster = `assets/video/poster-motion-${orientation}.webp?v=20261007c`;
}
chooseFilm();
portraitFilm.addEventListener("change", chooseFilm);

async function playFilm(time) {
  filmStatus.textContent = "";
  pendingFilmTime = time;
  if (!filmStarted) {
    filmStarted = true;
    productFilm.load();
  }
  if (productFilm.readyState >= 1 && time !== undefined) {
    productFilm.currentTime = time;
    pendingFilmTime = null;
  }
  filmPlayer.classList.add("is-started");
  productFilm.controls = true;
  try {
    await productFilm.play();
  } catch {
    filmPlayer.classList.remove("is-started");
    productFilm.controls = false;
    filmStatus.textContent = "영상을 재생하지 못했어요. 재생 버튼을 다시 눌러 주세요.";
  }
}
productFilm.addEventListener("loadedmetadata", () => {
  if (pendingFilmTime !== null && pendingFilmTime !== undefined) {
    productFilm.currentTime = pendingFilmTime;
    pendingFilmTime = null;
  }
});
document.querySelector("#film-play").addEventListener("click", () => playFilm());
filmChapters.forEach((button) => button.addEventListener("click", () => playFilm(Number(button.dataset.filmTime))));
productFilm.addEventListener("play", () => {
  filmPlayer.classList.add("is-started");
  productFilm.controls = true;
});
productFilm.addEventListener("timeupdate", () => {
  const time = productFilm.currentTime;
  filmChapters.forEach((button, index) => {
    const active = time >= Number(button.dataset.filmTime) && time < Number(button.dataset.filmEnd);
    button.classList.toggle("is-current", active);
  });
});
productFilm.addEventListener("error", () => {
  filmPlayer.classList.remove("is-started");
  productFilm.controls = false;
  filmStatus.textContent = "영상 연결을 확인하지 못했어요. 잠시 후 다시 재생해 주세요.";
});
// Playback is user initiated. Pause it when the document or player is out of view.
document.addEventListener("visibilitychange", () => {
  if (document.hidden) productFilm.pause();
});
if ("IntersectionObserver" in window) {
  new IntersectionObserver(([entry]) => {
    if (!entry.isIntersecting) productFilm.pause();
  }, { threshold: 0 }).observe(productFilm);
}

// 익힘 도장판: 시간 단계 버튼이 칸 상태와 안내 문장을 바꾼다.
const stampCard = document.querySelector(".stamp-card");
const masteryButtons = [...document.querySelectorAll("[data-mastery]")];
const masteryStatus = {
  today: "오늘 맞혔어요. 칸은 12시간 뒤에 켤 수 있어요.",
  lit: "네 칸이 모두 켜졌어요.",
  fade: "다시 확인할 때예요. 30일이 지나면 칸이 꺼져요.",
};
function showMastery(state) {
  stampCard.dataset.state = state;
  masteryButtons.forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.mastery === state)));
  document.querySelector("#mastery-status").textContent = masteryStatus[state];
}
let masteryTouched = false;
masteryButtons.forEach((button) => button.addEventListener("click", () => {
  masteryTouched = true;
  // 직접 누른 뒤부터만 화면 낭독기에 상태 변화를 알린다.
  document.querySelector("#mastery-status").setAttribute("role", "status");
  showMastery(button.dataset.mastery);
}));
// 처음 화면에 들어올 때 한 번만 도장이 찍히는 장면을 보여 준다.
if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  showMastery("today");
  const stampObserver = new IntersectionObserver(([entry]) => {
    if (!entry.isIntersecting) return;
    stampObserver.disconnect();
    setTimeout(() => { if (!masteryTouched) showMastery("lit"); }, 700);
  }, { threshold: 0.6 });
  stampObserver.observe(stampCard);
}

// Preserve links into collapsed learning details and individual FAQ answers.
function revealLinkedDetail() {
  if (!location.hash) return;
  let target;
  try { target = document.getElementById(decodeURIComponent(location.hash.slice(1))); } catch { return; }
  if (!target) return;
  let opened = false;
  for (let element = target; element; element = element.parentElement) {
    if (element.tagName === "DETAILS" && !element.open) { element.open = true; opened = true; }
  }
  if (opened) requestAnimationFrame(() => target.scrollIntoView({ block: "start", behavior: "instant" }));
}
window.addEventListener("hashchange", revealLinkedDetail);
document.addEventListener("click", (event) => {
  const link = event.target.closest('a[href^="#"]');
  if (link && link.hash === location.hash) revealLinkedDetail();
});
revealLinkedDetail();

// 의견 폼: 필드를 한 통의 메일 본문으로 묶어 메일 앱을 연다. JS 없이도 폼 자체가 mailto로 보낸다.
const feedbackForm = document.querySelector("#feedback-form");
feedbackForm?.addEventListener("submit", (event) => {
  event.preventDefault();
  const data = new FormData(feedbackForm);
  const kind = data.get("kind");
  const lines = [
    `[종류] ${kind}`,
    `[기기] ${data.get("device") || "(미기재)"}`,
    `[답장 주소] ${data.get("reply") || "(보내는 주소로)"}`,
    "",
    data.get("body"),
    "",
    `— 보낸 곳: ${location.origin}${location.pathname}`,
  ];
  const subject = `[어흥!한자] ${kind}`;
  const status = document.querySelector("#feedback-status");
  status.setAttribute("role", "status");
  status.textContent = "메일 앱을 여는 중이에요. 열리지 않으면 support@sunworks.kr로 직접 보내 주세요.";
  location.href = `mailto:support@sunworks.kr?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join("\n"))}`;
});
