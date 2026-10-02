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

const canvas = document.querySelector("#writing-canvas");
const context = canvas.getContext("2d", { willReadFrequently: true });
const writingStatus = document.querySelector("#writing-status");
const strokeButton = document.querySelector("#stroke-button");
const clearButton = document.querySelector("#clear-button");
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
let drawing = false;
let activePointer = null;
let drawingFrame = 0;
let strokeIndex = 0;
let previousPoint;
let strokeMode = false;
const strokes = [
  [
    [138, 214],
    [452, 214],
  ],
  [
    [302, 103],
    [302, 507],
  ],
  [
    [285, 220],
    [258, 285],
    [210, 350],
    [146, 408],
    [102, 436],
  ],
  [
    [320, 233],
    [356, 294],
    [405, 358],
    [463, 414],
    [502, 436],
  ],
];
const strokeDescriptions = [
  "첫째 획: 왼쪽에서 오른쪽으로 가로획.",
  "둘째 획: 위에서 아래로 세로획.",
  "셋째 획: 가운데에서 왼쪽 아래로 삐침.",
  "넷째 획: 가운데에서 오른쪽 아래로 파임. 나무 목 완성!",
];
function resetStrokeButton() {
  strokeButton.lastChild.textContent = "획순 보기";
}
function stopStrokeAnimation() {
  cancelAnimationFrame(drawingFrame);
  drawingFrame = 0;
  strokeButton.disabled = false;
}
function clearWriting(announce = true) {
  stopStrokeAnimation();
  if (activePointer !== null && canvas.hasPointerCapture(activePointer))
    canvas.releasePointerCapture(activePointer);
  activePointer = null;
  drawing = false;
  context.clearRect(0, 0, canvas.width, canvas.height);
  strokeIndex = 0;
  strokeMode = false;
  resetStrokeButton();
  if (announce)
    writingStatus.textContent = "깨끗해졌어요. 천천히, 다시 써 볼까요?";
}
function pointFor(event) {
  const box = canvas.getBoundingClientRect();
  return [
    ((event.clientX - box.left) * canvas.width) / box.width,
    ((event.clientY - box.top) * canvas.height) / box.height,
  ];
}
function ink(color = "#be411f", width = 11) {
  context.strokeStyle = color;
  context.fillStyle = color;
  context.lineWidth = width;
  context.lineCap = "round";
  context.lineJoin = "round";
}
if (context) {
  canvas.addEventListener("pointerdown", (event) => {
    if (!event.isPrimary || event.button !== 0) return;
    if (strokeMode) clearWriting(false);
    stopStrokeAnimation();
    activePointer = event.pointerId;
    canvas.setPointerCapture(activePointer);
    drawing = true;
    previousPoint = pointFor(event);
    ink();
    context.beginPath();
    context.arc(...previousPoint, 5.5, 0, Math.PI * 2);
    context.fill();
    writingStatus.textContent = "좋아요. 손끝으로 글자의 모양을 익혀 보세요.";
  });
  canvas.addEventListener("pointermove", (event) => {
    if (!drawing || event.pointerId !== activePointer) return;
    const point = pointFor(event);
    ink();
    context.beginPath();
    context.moveTo(...previousPoint);
    context.lineTo(...point);
    context.stroke();
    previousPoint = point;
  });
  function finishPointer(event) {
    if (event.pointerId !== activePointer) return;
    drawing = false;
    if (canvas.hasPointerCapture(activePointer))
      canvas.releasePointerCapture(activePointer);
    activePointer = null;
  }
  canvas.addEventListener("pointerup", finishPointer);
  canvas.addEventListener("pointercancel", finishPointer);
  canvas.addEventListener("lostpointercapture", () => {
    drawing = false;
    activePointer = null;
  });
  clearButton.addEventListener("click", () => clearWriting());
  strokeButton.addEventListener("click", () => {
    if (!strokeMode || strokeIndex === 4) {
      clearWriting(false);
      strokeMode = true;
    }
    const points = strokes[strokeIndex];
    const base = context.getImageData(0, 0, canvas.width, canvas.height);
    const started = performance.now();
    strokeButton.disabled = true;
    function paint(now) {
      const progress = reducedMotion.matches
        ? 1
        : Math.min((now - started) / 420, 1);
      context.putImageData(base, 0, 0);
      ink("#233f35", 12);
      context.beginPath();
      context.moveTo(...points[0]);
      const pathProgress = progress * (points.length - 1);
      for (let index = 1; index < points.length; index++) {
        const fraction = Math.max(0, Math.min(1, pathProgress - index + 1));
        if (fraction === 0) break;
        context.lineTo(
          points[index - 1][0] +
            (points[index][0] - points[index - 1][0]) * fraction,
          points[index - 1][1] +
            (points[index][1] - points[index - 1][1]) * fraction,
        );
      }
      context.stroke();
      if (progress < 1) drawingFrame = requestAnimationFrame(paint);
      else {
        writingStatus.textContent = strokeDescriptions[strokeIndex];
        strokeIndex += 1;
        strokeButton.disabled = false;
        strokeButton.lastChild.textContent =
          strokeIndex === 4
            ? "획순 다시 보기"
            : `다음 획 (${strokeIndex + 1}/4)`;
        drawingFrame = 0;
      }
    }
    drawingFrame = requestAnimationFrame(paint);
  });
} else {
  canvas.hidden = true;
  strokeButton.disabled = true;
  clearButton.disabled = true;
  writingStatus.textContent =
    "이 브라우저에서는 손글씨 체험을 열 수 없어요. 웹앱에서 다른 학습을 만나 보세요.";
}
