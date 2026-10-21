import { TraceSession, resample } from './stroke-scorer.mjs';

const board = document.querySelector('.writing-workspace');
const canvas = document.querySelector('#writing-canvas');
const context = canvas.getContext('2d');
const status = document.querySelector('#writing-status');
const progress = document.querySelector('#writing-progress');
const playButton = document.querySelector('#writing-play');
const clearButton = document.querySelector('#clear-button');
const result = document.querySelector('#writing-result');
const modes = [...document.querySelectorAll('[data-writing-mode]')];
const characters = [...document.querySelectorAll('[data-writing-char]')];
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
const size = canvas.width;
const strokeMs = 800;
const colors = { ink: '#233f35', missed: '#be411f', outline: '#e9ebdf' };
let glyph, paths, medians, session;
let mode = 'write';
let character = '明';
let frame = 0, playing = false, shown = 0, partial = 0;
let pointer = null, points = [];
let loadVersion = 0;
const cache = new Map();

function announce(message) { status.textContent = message; }
function updateControls() {
  const ready = Boolean(glyph);
  const watching = mode === 'watch';
  board.dataset.mode = mode;
  modes.forEach((b) => { b.disabled = !ready; b.setAttribute('aria-pressed', String(b.dataset.writingMode === mode)); });
  playButton.hidden = !watching;
  // The result card has its own retry button.
  clearButton.hidden = watching || Boolean(ready && session.done);
  playButton.disabled = clearButton.disabled = !ready;
  const finished = ready && shown >= medians.length;
  playButton.querySelector('span').textContent = playing ? '멈춤' : finished ? '다시 재생' : shown || partial ? '이어서 재생' : '획순 재생';
  playButton.dataset.playing = String(playing);
  const count = ready ? medians.length : 0;
  progress.textContent = !ready ? '준비 중' : watching ? `${shown} / ${count}획` : `${session.index} / ${count}획 진행`;
  canvas.setAttribute('aria-label', `${glyph?.reading ?? '한자'} 연습장. ${watching ? '재생 버튼을 누르면 획순이 차례로 나타나요.' : '획순 안내 없이 마우스나 손가락으로 한 획씩 써 보세요. 맞게 쓴 획은 화면에 나타나요. 키보드로는 획순 보기의 재생 버튼을 이용하세요.'}`);
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
  shown = 0; partial = 0;
  session = new TraceSession(medians, size);
  result.hidden = true;
  updateControls(); render();
  announce(mode === 'watch' ? '재생 버튼을 누르면 획순이 차례로 나타나요.' : '획순 안내 없이 한 획씩 써 보세요. 맞게 쓴 획은 화면에 나타나요.');
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
function line(path, color, width) {
  if (!path.length) return;
  context.save(); context.beginPath(); context.moveTo(...path[0]);
  path.slice(1).forEach((p) => context.lineTo(...p));
  context.strokeStyle = color; context.lineWidth = width;
  context.lineCap = context.lineJoin = 'round';
  context.stroke(); context.restore();
}
function render() {
  context.clearRect(0, 0, size, size);
  if (!glyph) return;
  // Like the app's practice screen: a faint whole-glyph silhouette, no order or path hints.
  paths.forEach((_, i) => fillStroke(i, colors.outline));
  if (mode === 'watch') {
    for (let i = 0; i < shown; i++) fillStroke(i, colors.ink);
    // Reduced motion: each stroke appears whole instead of being drawn.
    if (partial > 0 && shown < paths.length && !reducedMotion.matches) fillStroke(shown, colors.ink, partial);
  } else {
    session.results.forEach((r, i) => fillStroke(i, r.passed ? colors.ink : colors.missed));
    line(points, colors.ink, 9);
  }
}

function play() {
  if (!glyph || mode !== 'watch') return;
  if (shown >= medians.length) { shown = 0; partial = 0; }
  playing = true;
  let last = performance.now();
  function paint(now) {
    partial += (now - last) / strokeMs;
    last = now;
    if (partial >= 1) {
      shown++; partial = 0;
      updateControls();
      announce(`${shown} / ${medians.length}획. ${glyph.descriptions[shown - 1]}${shown === medians.length ? ' 획순을 모두 봤어요. 직접 쓰기도 해 볼까요?' : ''}`);
    }
    render();
    if (shown < medians.length) frame = requestAnimationFrame(paint);
    else { frame = 0; playing = false; updateControls(); }
  }
  frame = requestAnimationFrame(paint);
  updateControls();
}

function reason(score) {
  return !score.directionOk ? '방향이 반대였어요' : !score.startPointOk ? '시작 위치가 달랐어요' : '모양이 조금 어긋났어요';
}
function showResult() {
  const total = medians.length;
  const missed = session.results.flatMap((r, i) => (r.passed ? [] : [`${i + 1}번째 획: ${reason(r)}`]));
  result.querySelector('[data-result="score"]').textContent = `${session.passed} / ${total}획`;
  result.querySelector('[data-result="summary"]').textContent = session.allPassed
    ? '모든 획을 획순대로 맞게 썼어요!'
    : `${missed.length}획은 세 번 안에 맞히지 못해 주황색으로 보여 드렸어요.`;
  result.querySelector('[data-result="accuracy"]').textContent = `획 정확도 ${Math.round(session.accuracy * 100)}%`;
  const list = result.querySelector('[data-result="missed"]');
  list.replaceChildren(...missed.map((text) => Object.assign(document.createElement('li'), { textContent: text })));
  list.parentElement.hidden = !missed.length;
  result.hidden = false;
  announce(`${glyph.reading} 완성! 전체 ${total}획 중 ${session.passed}획을 맞게 썼어요. 획 정확도 ${Math.round(session.accuracy * 100)}%.`);
}

function pointFor(event) {
  const rect = canvas.getBoundingClientRect();
  return [(event.clientX - rect.left) * size / rect.width, (event.clientY - rect.top) * size / rect.height];
}
function finishStroke() {
  const input = points;
  cancelPointer();
  const scored = session.submit(input);
  if (!scored) { render(); return; }
  if (session.done) showResult();
  else if (scored.advanced) {
    announce(`${scored.assisted ? '세 번 안에 맞히지 못해 이 획을 보여 드렸어요.' : '맞았어요!'} 이제 ${session.index + 1}번째 획이에요.`);
  } else {
    announce(`${!scored.directionOk ? '획을 쓰는 방향을 다시 떠올려 보세요.' : !scored.startPointOk ? '획의 시작 위치를 다시 살펴보세요.' : '획의 모양을 다시 떠올려 보세요.'} ${session.attempts} / 3번 시도했어요.`);
  }
  updateControls(); render();
}

async function loadCharacter(value) {
  const version = ++loadVersion;
  character = value; stopAnimation(); cancelPointer();
  glyph = null; context.clearRect(0, 0, size, size);
  result.hidden = true;
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
    mode = 'write';
    await loadCharacter('明');
    canvas.focus({ preventScroll: true });
  }));
  characters.forEach((b) => b.addEventListener('click', () => loadCharacter(b.dataset.writingChar)));
  modes.forEach((b) => b.addEventListener('click', () => { mode = b.dataset.writingMode; reset(); }));
  clearButton.addEventListener('click', reset);
  result.querySelector('[data-result="retry"]').addEventListener('click', () => { reset(); canvas.focus({ preventScroll: true }); });
  playButton.addEventListener('click', () => {
    if (playing) { stopAnimation(); updateControls(); announce('잠깐 멈췄어요. 다시 누르면 이어서 재생해요.'); }
    else play();
  });
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
  loadCharacter(character);
} else {
  board.querySelectorAll('button').forEach((b) => { b.disabled = true; });
  announce('이 브라우저에서는 손글씨 체험을 열 수 없어요. 웹앱에서 다른 학습을 만나 보세요.');
}
