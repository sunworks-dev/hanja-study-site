import { TraceSession, resample } from './stroke-scorer.mjs';

const board = document.querySelector('.writing-workspace');
const canvas = document.querySelector('#writing-canvas');
const context = canvas.getContext('2d');
const status = document.querySelector('#writing-status');
const progress = document.querySelector('#writing-progress');
const nextButton = document.querySelector('#stroke-button');
const playButton = document.querySelector('#writing-play');
const clearButton = document.querySelector('#clear-button');
const speed = document.querySelector('#writing-speed');
const modes = [...document.querySelectorAll('[data-writing-mode]')];
const characters = [...document.querySelectorAll('[data-writing-char]')];
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
const size = canvas.width;
const colors = { ink: '#233f35', hint: '#be411f', outline: '#e9ebdf', assisted: '#899184' };
let glyph, paths, medians, session;
let mode = 'guide';
let character = '明';
let frame = 0, playing = false, shown = 0, partial = 0;
let pointer = null, points = [], userStrokes = [];
let loadVersion = 0;
const cache = new Map();

function announce(message) { status.textContent = message; }
function updateControls() {
  const ready = Boolean(glyph);
  const watching = mode === 'watch';
  board.dataset.mode = mode;
  modes.forEach((b) => { b.disabled = !ready; b.setAttribute('aria-pressed', String(b.dataset.writingMode === mode)); });
  nextButton.hidden = playButton.hidden = speed.parentElement.hidden = !watching;
  nextButton.disabled = !ready || Boolean(frame);
  playButton.disabled = clearButton.disabled = !ready;
  playButton.textContent = playing ? '잠깐 멈추기' : '이어서 보기';
  playButton.setAttribute('aria-pressed', String(playing));
  nextButton.textContent = ready && shown >= medians.length ? '처음 획 보기' : '다음 획 보기';
  const count = ready ? medians.length : 0;
  progress.textContent = !ready ? '준비 중' : watching ? `${shown} / ${count}획 살펴봄` : `${session.index} / ${count}획 진행`;
  canvas.setAttribute('aria-label', `${glyph?.reading ?? '한자'} 연습장. ${watching ? '아래 버튼으로 획순을 살펴보세요.' : `${mode === 'guide' ? '시작점에서 선을 따라' : '힌트 없이'} 마우스나 손가락으로 한 획씩 써 보세요. 키보드로는 획순 보기 버튼을 이용하세요.`}`);
}

function stopAnimation() {
  cancelAnimationFrame(frame);
  frame = 0;
  playing = false;
}
function cancelPointer() {
  const previous = pointer;
  pointer = null;
  points = [];
  if (previous !== null && canvas.hasPointerCapture(previous)) canvas.releasePointerCapture(previous);
}
function reset() {
  stopAnimation(); cancelPointer();
  shown = 0; partial = 0; userStrokes = [];
  session = new TraceSession(medians, size);
  updateControls(); render();
  announce(mode === 'watch' ? '버튼을 눌러 한 획씩 살펴보세요.' : mode === 'guide' ? '숫자가 있는 시작점에서 화살표까지 그어 보세요.' : '글자 모양을 떠올려 한 획씩 써 보세요. 막히면 따라 쓰기로 돌아가도 괜찮아요.');
}

function transform() {
  const scale = size / 1024 * glyph.fit.scale;
  context.translate(size / 2 - glyph.fit.center[0] * scale, size / 2 + glyph.fit.center[1] * scale);
  context.scale(scale, -scale);
}
function fillStroke(index, color, fraction = 1) {
  context.save(); transform();
  if (fraction < 1) {
    context.clip(paths[index]);
    const samples = resample(glyph.medians[index], 100);
    context.beginPath(); context.moveTo(...samples[0]);
    samples.slice(1, Math.max(2, Math.ceil(fraction * 100))).forEach((p) => context.lineTo(...p));
    context.strokeStyle = color; context.lineWidth = 200;
    context.lineCap = context.lineJoin = 'round'; context.stroke();
  } else { context.fillStyle = color; context.fill(paths[index]); }
  context.restore();
}
function line(path, color, width, dashed = false) {
  if (!path.length) return;
  context.save(); context.beginPath(); context.moveTo(...path[0]);
  path.slice(1).forEach((p) => context.lineTo(...p));
  context.strokeStyle = color; context.lineWidth = width;
  context.lineCap = context.lineJoin = 'round';
  if (dashed) context.setLineDash([10, 9]);
  context.stroke(); context.restore();
}
function render() {
  context.clearRect(0, 0, size, size);
  if (!glyph) return;
  if (mode !== 'blind') paths.forEach((_, i) => fillStroke(i, colors.outline));
  if (mode === 'watch') {
    for (let i = 0; i < shown; i++) fillStroke(i, colors.ink);
    if (partial > 0 && shown < paths.length) fillStroke(shown, colors.ink, partial);
  } else {
    session.results.forEach((result, i) => fillStroke(i, result.passed ? colors.ink : colors.assisted));
    if (mode === 'guide' && !session.done) {
      const median = medians[session.index];
      line(median, colors.hint, 4, true);
      const start = median[0], end = median.at(-1), before = median.at(-2);
      const angle = Math.atan2(end[1] - before[1], end[0] - before[0]);
      line([[end[0] - 17 * Math.cos(angle - .5), end[1] - 17 * Math.sin(angle - .5)], end,
        [end[0] - 17 * Math.cos(angle + .5), end[1] - 17 * Math.sin(angle + .5)]], colors.hint, 5);
      context.beginPath(); context.arc(...start, 19, 0, Math.PI * 2);
      context.fillStyle = colors.hint; context.fill();
      context.fillStyle = '#fffef9'; context.font = 'bold 24px sans-serif';
      context.textAlign = 'center'; context.textBaseline = 'middle';
      context.fillText(String(session.index + 1), ...start);
    }
    userStrokes.forEach((path) => line(path, colors.ink, 5));
    line(points, colors.ink, 9);
  }
}

function showNext(continuous = false) {
  if (!glyph || mode !== 'watch') return;
  cancelAnimationFrame(frame);
  if (shown >= medians.length) { shown = 0; partial = 0; }
  playing = continuous;
  const start = performance.now();
  const from = partial;
  function paint(now) {
    partial = reducedMotion.matches ? 1 : Math.min(1, from + (now - start) / (800 / Number(speed.value)));
    render();
    if (partial < 1) frame = requestAnimationFrame(paint);
    else {
      shown++; partial = 0; frame = 0;
      announce(`${shown} / ${medians.length}획. ${glyph.descriptions[shown - 1]}${shown === medians.length ? ' 획순을 모두 살펴봤어요. 따라 쓰기도 해 볼까요?' : ''}`);
      render();
      if (playing && shown < medians.length && !reducedMotion.matches) showNext(true);
      else { playing = false; updateControls(); }
    }
  }
  frame = requestAnimationFrame(paint);
  updateControls();
}

function pointFor(event) {
  const rect = canvas.getBoundingClientRect();
  return [(event.clientX - rect.left) * size / rect.width, (event.clientY - rect.top) * size / rect.height];
}
function finishStroke() {
  const input = points;
  cancelPointer();
  const result = session.submit(input);
  if (!result) { render(); return; }
  if (result.advanced && mode === 'guide') userStrokes.push(input);
  if (session.done) {
    const helped = medians.length - session.passed;
    announce(`${glyph.reading} 완성! ${session.allPassed ? `${session.passed}획 모두 스스로 썼어요.` : `${session.passed}획은 스스로, ${helped}획은 도움을 받아 썼어요.`} 획 정확도 ${Math.round(session.accuracy * 100)}%. ${mode === 'guide' ? '이번엔 혼자 쓰기에 도전해 볼까요?' : '다시 쓰기로 한 번 더 연습할 수 있어요.'}`);
  } else if (result.advanced) {
    announce(`${result.assisted ? '이 획은 함께 완성했어요.' : '잘 그었어요!'} 이제 ${session.index + 1}번째 획이에요.`);
  } else {
    announce(`${!result.directionOk ? '시작점에서 끝점 방향으로 그어 보세요.' : !result.startPointOk ? '획의 시작 위치를 다시 살펴보세요.' : '획의 모양을 따라 끝까지 그어 보세요.'} ${session.attempts} / 3번 시도했어요.`);
  }
  updateControls(); render();
}

async function loadCharacter(value) {
  const version = ++loadVersion;
  character = value; stopAnimation(); cancelPointer();
  glyph = null; context.clearRect(0, 0, size, size);
  characters.forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.writingChar === value)));
  board.setAttribute('aria-busy', 'true'); updateControls();
  announce('획순을 준비하고 있어요.');
  try {
    let data = cache.get(value);
    if (!data) {
      const response = await fetch(`assets/hanzi/${encodeURIComponent(value)}.json`);
      if (!response.ok) throw new Error('stroke data unavailable');
      data = await response.json();
      if (!data.strokes?.length || data.strokes.length !== data.medians?.length || data.medians.some((m) => m.length < 2) || !data.fit) throw new Error('invalid stroke data');
      cache.set(value, data);
    }
    if (version !== loadVersion) return;
    paths = data.strokes.map((path) => new Path2D(path));
    glyph = data;
    const scale = size / 1024 * data.fit.scale;
    medians = data.medians.map((m) => m.map(([x, y]) => [size / 2 + (x - data.fit.center[0]) * scale, size / 2 - (y - data.fit.center[1]) * scale]));
    document.querySelector('#writing-character').textContent = value;
    document.querySelector('#writing-reading').textContent = data.reading;
    reset();
  } catch {
    if (version !== loadVersion) return;
    glyph = null; updateControls();
    announce('획순을 불러오지 못했어요. 글자 버튼을 눌러 다시 시도해 주세요.');
  } finally { if (version === loadVersion) board.setAttribute('aria-busy', 'false'); }
}

if (context && typeof Path2D === 'function') {
  document.querySelectorAll('a[href="#writing-demo"]').forEach((link) => link.addEventListener('click', async () => {
    mode = 'guide';
    await loadCharacter('明');
    canvas.focus({ preventScroll: true });
  }));
  characters.forEach((b) => b.addEventListener('click', () => loadCharacter(b.dataset.writingChar)));
  modes.forEach((b) => b.addEventListener('click', () => { mode = b.dataset.writingMode; reset(); }));
  clearButton.addEventListener('click', reset);
  nextButton.addEventListener('click', () => showNext());
  playButton.addEventListener('click', () => {
    if (playing) { stopAnimation(); updateControls(); announce('잠깐 멈췄어요. 이어서 볼 수 있어요.'); }
    else showNext(true);
  });
  speed.addEventListener('change', () => { if (frame) showNext(playing); });
  canvas.addEventListener('pointerdown', (event) => {
    if (!glyph || mode === 'watch' || session.done || !event.isPrimary || event.button !== 0 || pointer !== null) return;
    pointer = event.pointerId; points = [pointFor(event)];
    canvas.setPointerCapture(pointer); render();
  });
  canvas.addEventListener('pointermove', (event) => {
    if (pointer !== event.pointerId) return;
    const samples = event.getCoalescedEvents?.() ?? [];
    (samples.length ? samples : [event]).forEach((sample) => points.push(pointFor(sample)));
    render();
  });
  canvas.addEventListener('pointerup', (event) => {
    if (pointer !== event.pointerId) return;
    const end = pointFor(event);
    // A tap is not a stroke and must not consume an attempt.
    if (!points.some((p) => Math.hypot(p[0] - points[0][0], p[1] - points[0][1]) > 2)
      && Math.hypot(end[0] - points[0][0], end[1] - points[0][1]) <= 2) { cancelPointer(); render(); return; }
    points.push(end); finishStroke();
  });
  for (const name of ['pointercancel', 'lostpointercapture']) canvas.addEventListener(name, (event) => {
    if (pointer !== event.pointerId) return;
    cancelPointer(); render();
  });
  function suspend() { cancelPointer(); stopAnimation(); if (glyph) { updateControls(); render(); } }
  document.addEventListener('visibilitychange', () => { if (document.hidden) suspend(); });
  window.addEventListener('blur', suspend);
  new IntersectionObserver(([entry]) => { if (!entry.isIntersecting) suspend(); }).observe(canvas);
  reducedMotion.addEventListener('change', () => {
    if (reducedMotion.matches && frame) { stopAnimation(); partial = 0; shown++; updateControls(); render(); announce('움직임을 줄여 현재 획을 바로 보여 드렸어요. 다음 획 보기로 이어 가세요.'); }
  });
  loadCharacter(character);
} else {
  board.querySelectorAll('button, select').forEach((b) => { b.disabled = true; });
  announce('이 브라우저에서는 손글씨 체험을 열 수 없어요. 웹앱에서 다른 학습을 만나 보세요.');
}
