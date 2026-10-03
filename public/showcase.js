"use strict";

const showcaseContent = {
  learn: {
    image: "study", alt: "학교 교의 획순·연상·연결 어휘 학습 화면",
    heading: ["校 하나를 배웠는데,", "학교가 새롭게 보여요."],
    description: "획순으로 모양을 익히고, 연상으로 뜻을 연결해요. 학교·대학교·중학교처럼 같은 한자를 쓰는 단어를 함께 만나니, 한 글자의 배움이 우리말로 넓어집니다.",
    benefits: ["획순·훈음·부수·연상 설명을 한곳에서", "단어와 예문으로 넓히는 이해", "정답을 보기 전, 직접 떠올리는 연습"],
  },
  story: {
    image: "story", alt: "흥부와 놀부 이야기의 빈칸에 농촌을 맞힌 실제 앱 화면",
    heading: ["한자를 맞혔더니,", "이야기가 이어져요."],
    description: "흥부와 놀부, 해와 달이 된 오누이. 익숙한 옛이야기 속 빈칸을 채우며 한자를 문맥으로 만나요. 다음 마당을 여는 재미가 한 번 더 읽을 이유가 됩니다.",
    benefits: ["흥부와 놀부·심청 등 이야기 11편", "문장 속에서 생각하는 한자어의 뜻", "마당별 진도를 저장해 이어서 학습"],
  },
  collection: {
    image: "collection", alt: "8급의 읽기·훈음·쓰기·부수 학습 현황과 한자 도감 화면",
    heading: ["얼마나 했는지보다,", "무엇을 익혔는지."],
    description: "읽기·뜻·쓰기·부수를 따로 살펴요. 한 번 본 글자와 여러 번 떠올린 글자를 구분하고, 한자 도감에서 배운 흔적을 확인합니다. 약한 유형은 골라 연습할 수 있어요.",
    benefits: ["네 가지 방향으로 확인하는 숙련 상태", "급수별 도감과 학습 기록", "모의시험·오답 복습·유형별 연습"],
  },
  home: {
    image: "home", alt: "새 한자와 복습 분량, 이어서 풀기를 안내하는 앱 홈 화면",
    heading: ["오늘 뭘 할지,", "고민은 줄여 주세요."],
    description: "새로 만날 한자와 다시 볼 한자를 오늘의 학습으로 모아 줍니다. FSRS가 답변 기록에 맞춰 복습 간격을 조절하고, 잠깐 멈춘 공부는 이어서 시작할 수 있어요.",
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

function chooseFilm() {
  // Never swap a loaded film during playback or restart a user's position.
  if (filmStarted) return;
  const orientation = portraitFilm.matches ? "portrait" : "landscape";
  productFilm.querySelector("source").src = `assets/video/hanja-film-${orientation}.mp4`;
  productFilm.poster = `assets/video/poster-${orientation}.webp`;
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
  try {
    await productFilm.play();
  } catch {
    filmPlayer.classList.remove("is-started");
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
productFilm.addEventListener("play", () => filmPlayer.classList.add("is-started"));
productFilm.addEventListener("timeupdate", () => {
  const time = productFilm.currentTime;
  filmChapters.forEach((button, index) => {
    const active = time >= Number(button.dataset.filmTime) && time < Number(filmChapters[index + 1]?.dataset.filmTime || 32);
    button.classList.toggle("is-current", active);
  });
});
productFilm.addEventListener("error", () => {
  filmPlayer.classList.remove("is-started");
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
