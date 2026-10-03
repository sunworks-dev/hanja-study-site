"use strict";

const demo = document.querySelector("#hero-demo");
const connectButton = document.querySelector("#connect-button");
const feedback = document.querySelector("#demo-feedback");
const panels = ["connect", "recall", "success"];

function setDemoStep(step) {
  demo.dataset.step = step;
  panels.forEach((name) => {
    document.querySelector(`#${name}-panel`).hidden = name !== step;
  });
  document.querySelector("#demo-step").textContent =
    `${panels.indexOf(step) + 1} / 3`;
  document
    .querySelector(".hanja-combined")
    .setAttribute("aria-hidden", step === "connect" ? "true" : "false");
}

connectButton.addEventListener("click", () => {
  setDemoStep("recall");
  feedback.textContent = "";
  document
    .querySelector('[data-answer="bright"]')
    .focus({ preventScroll: true });
});

document.querySelectorAll("[data-answer]").forEach((button) => {
  button.addEventListener("click", () => {
    if (button.dataset.answer === "bright") {
      setDemoStep("success");
      feedback.textContent = "밝을 명, 한 글자와 친해졌어요!";
      document.querySelector("#success-panel a").focus({ preventScroll: true });
    } else {
      document
        .querySelectorAll("[data-answer]")
        .forEach((answer) => answer.removeAttribute("aria-pressed"));
      button.setAttribute("aria-pressed", "true");
      feedback.textContent =
        button.dataset.answer === "rest"
          ? "괜찮아요! 해와 달이 빛나는 모습을 떠올려 볼까요?"
          : "숲은 나무를 떠올려요. 해와 달은 어떤 빛을 낼까요?";
    }
  });
});

document.querySelector("#demo-reset").addEventListener("click", () => {
  setDemoStep("connect");
  feedback.textContent = "";
  document
    .querySelectorAll("[data-answer]")
    .forEach((button) => button.removeAttribute("aria-pressed"));
  connectButton.focus({ preventScroll: true });
});

const words = [
  {
    word: "설명",
    hanja: ["說", "明"],
    accent: 1,
    definition: "어떤 내용을 잘 알 수 있도록 밝혀 말하는 것.",
    before: "친구에게 문제 풀이를 ",
    after: "했어요.",
  },
  {
    word: "명확",
    hanja: ["明", "確"],
    accent: 0,
    definition: "뜻이나 내용이 분명하고 확실한 것.",
    before: "자기 생각을 ",
    after: "하게 말했어요.",
  },
  {
    word: "문명",
    hanja: ["文", "明"],
    accent: 1,
    definition: "사람들이 함께 발전시켜 온 생활과 문화.",
    before: "역사 시간에 고대 ",
    after: "의 발달을 배웠어요.",
  },
];
const wordTabs = [...document.querySelectorAll("[data-word]")];
function selectWord(index, moveFocus = false) {
  const word = words[index];
  wordTabs.forEach((tab, i) => {
    tab.setAttribute("aria-selected", String(i === index));
    tab.tabIndex = i === index ? 0 : -1;
  });
  const characters = word.hanja.map((character, i) => {
    if (i !== word.accent) return document.createTextNode(character);
    const accent = document.createElement("span");
    accent.textContent = character;
    return accent;
  });
  document.querySelector("#word-hanja").replaceChildren(...characters);
  document.querySelector("#word-title").textContent = word.word;
  document.querySelector("#word-definition").textContent = word.definition;
  const emphasis = document.createElement("strong");
  emphasis.textContent = word.word;
  document
    .querySelector("#word-example")
    .replaceChildren(
      document.createTextNode(word.before),
      emphasis,
      document.createTextNode(word.after),
    );
  document
    .querySelector("#word-panel")
    .setAttribute("aria-labelledby", wordTabs[index].id);
  if (moveFocus) wordTabs[index].focus({ preventScroll: true });
}
wordTabs.forEach((tab, index) => {
  tab.addEventListener("click", () => selectWord(index));
  tab.addEventListener("keydown", (event) => {
    let next;
    if (event.key === "ArrowRight") next = (index + 1) % words.length;
    if (event.key === "ArrowLeft")
      next = (index + words.length - 1) % words.length;
    if (event.key === "Home") next = 0;
    if (event.key === "End") next = words.length - 1;
    if (next !== undefined) {
      event.preventDefault();
      selectWord(next, true);
    }
  });
});
