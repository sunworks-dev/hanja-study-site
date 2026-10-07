"use strict";

const showcaseContent = {
  learn: {
    image: "study", alt: "학교 교의 조각 모아 보기·획순·뜻풀이 학습 화면",
    heading: ["校 하나를 배웠는데,", "학교가 새롭게 보여요."],
    description: "校는 나무 木과 사귈 交가 만난 글자예요. 조각을 모아 뜻과 소리를 짐작하고, 획순으로 모양을 익혀요. 학교·대학교·중학교처럼 같은 한자를 쓰는 단어로 배움이 우리말까지 넓어집니다.",
    benefits: ["조각 모아 보기·획순·훈음·부수를 한곳에서", "뜻을 떠올리기 쉬운 그림과 단어·예문", "정답을 보기 전, 직접 떠올리는 연습"],
  },
  story: {
    image: "story", alt: "흥부와 놀부 이야기의 빈칸에 농촌을 맞힌 실제 앱 화면",
    heading: ["한자를 맞혔더니,", "이야기가 이어져요."],
    description: "흥부와 놀부, 해와 달이 된 오누이. 익숙한 옛이야기 속 빈칸을 채우며 한자를 문맥으로 만나요. 한자어를 글 속에서 많이 읽을수록 기억의 연결 고리가 늘어나요. 국어 문해력까지 함께 자라도록 만들었습니다.",
    benefits: ["흥부전·심청전·홍길동전 등 고전을 바탕으로 한 이야기 11편", "문장 속에서 생각하는 한자어의 뜻", "마당별 진도를 저장해 이어서 학습"],
  },
  collection: {
    image: "collection", alt: "8급의 유형별 익힘 정도와 색이 켜진 校·敎·九 카드가 있는 한자 도감 화면",
    heading: ["얼마나 했는지보다,", "무엇을 익혔는지."],
    description: "읽기·뜻·쓰기·부수를 따로 살펴요. 12시간 넘게 지난 뒤 다시 맞혀야 칸이 켜지니, 한 번 본 글자와 정말 익힌 글자가 구분돼요. 만난 한자가 도감에 하나씩 모이는 재미도 있어요.",
    benefits: ["12시간 뒤 다시 맞혀야 켜지는 네 개의 칸", "30일 안에 다시 확인해 오래 남기는 기억", "급수별 도감·모의시험·유형별 연습"],
  },
  home: {
    image: "home", alt: "연속 학습 일수, 오늘의 새 한자와 복습 분량, 시험 일정을 보여 주는 앱 홈 화면",
    heading: ["오늘 뭘 할지,", "고민은 줄여 주세요."],
    description: "새로 만날 한자와 다시 볼 한자를 오늘의 학습으로 모아 줍니다. 답변 기록에 맞춰 다시 볼 시점을 조절하고, 잠깐 멈춘 공부는 이어서 시작할 수 있어요.",
    benefits: ["내 기록에 맞춰 조절되는 복습 간격", "직접 정하는 하루 신규 학습량", "풀던 학습을 이어 가는 세션 저장"],
  },
};

const showcaseTabs = [...document.querySelectorAll("[data-showcase]")];
const showcaseImage = document.querySelector("#showcase-image");
function showFeature(tab, focus = false) {
  const item = showcaseContent[tab.dataset.showcase];
  showcaseTabs.forEach((button) => {
    const selected = button === tab;
    button.setAttribute("aria-selected", String(selected));
    button.tabIndex = selected ? 0 : -1;
  });
  showcaseImage.src = `assets/screens/${item.image}.webp`;
  showcaseImage.alt = item.alt;
  const enlarge = document.querySelector("#showcase-enlarge");
  enlarge.href = showcaseImage.src;
  enlarge.setAttribute("aria-label", `${item.alt} 크게 보기, 새 탭`);
  const title = document.querySelector("#showcase-heading");
  title.replaceChildren(document.createTextNode(item.heading[0]), document.createElement("br"), document.createTextNode(item.heading[1]));
  document.querySelector("#showcase-description").textContent = item.description;
  document.querySelector("#showcase-benefits").replaceChildren(...item.benefits.map((text) => {
    const li = document.createElement("li");
    li.textContent = text;
    return li;
  }));
  document.querySelector("#showcase-panel").setAttribute("aria-labelledby", tab.id);
  if (focus) tab.focus();
}
showcaseTabs.forEach((tab, index) => {
  tab.addEventListener("click", () => showFeature(tab));
  tab.addEventListener("keydown", (event) => {
    let next;
    if (event.key === "ArrowRight") next = (index + 1) % showcaseTabs.length;
    if (event.key === "ArrowLeft") next = (index - 1 + showcaseTabs.length) % showcaseTabs.length;
    if (event.key === "Home") next = 0;
    if (event.key === "End") next = showcaseTabs.length - 1;
    if (next !== undefined) {
      event.preventDefault();
      showFeature(showcaseTabs[next], true);
    }
  });
});

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
feedbackForm.addEventListener("submit", (event) => {
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
