// Port of hanja-study-app/lib/handwriting/stroke_scorer.dart.
// Keep tolerance, resampling, direction and accuracy in sync with the app.
const distance = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1]);

export function resample(points, count = 32) {
  const lengths = [0];
  for (let i = 1; i < points.length; i++) {
    lengths.push(lengths[i - 1] + distance(points[i - 1], points[i]));
  }
  const total = lengths.at(-1);
  if (total === 0) return Array.from({ length: count }, () => points[0]);
  const out = [points[0]];
  let j = 1;
  for (let k = 1; k < count - 1; k++) {
    const target = (total / (count - 1)) * k;
    while (j < points.length - 1 && lengths[j] < target) j++;
    const segment = lengths[j] - lengths[j - 1];
    const t = segment === 0 ? 0 : (target - lengths[j - 1]) / segment;
    out.push(points[j - 1].map((v, axis) => v + (points[j][axis] - v) * t));
  }
  out.push(points.at(-1));
  return out;
}

export function scoreStroke(user, expected, canvasSize) {
  if (user.length < 2 || expected.length < 2 || canvasSize <= 0) {
    return { frechet: Infinity, directionOk: false, startPointOk: false, passed: false, accuracy: 0 };
  }
  const u = resample(user);
  const e = resample(expected);
  const grid = u.map(() => Array(e.length).fill(0));
  for (let i = 0; i < u.length; i++) {
    for (let j = 0; j < e.length; j++) {
      const d = distance(u[i], e[j]);
      grid[i][j] = i === 0 && j === 0 ? d
        : i === 0 ? Math.max(grid[i][j - 1], d)
        : j === 0 ? Math.max(grid[i - 1][j], d)
        : Math.max(Math.min(grid[i - 1][j], grid[i - 1][j - 1], grid[i][j - 1]), d);
    }
  }
  const frechet = grid.at(-1).at(-1);
  const start = distance(u[0], e[0]);
  const directionOk = start <= distance(u[0], e.at(-1));
  const maxAllowed = canvasSize * 0.22;
  return {
    frechet, directionOk, startPointOk: start <= maxAllowed,
    passed: directionOk && frechet <= maxAllowed,
    accuracy: Math.max(0, Math.min(1, 1 - frechet / maxAllowed)),
  };
}

// The same three-attempt flow as StrokeTraceCanvas. Assisted strokes count
// in the accuracy average, but never become independently passed strokes.
export class TraceSession {
  constructor(medians, size = 600) {
    this.medians = medians;
    this.size = size;
    this.index = 0;
    this.attempts = 0;
    this.results = [];
  }
  get done() { return this.index >= this.medians.length; }
  get passed() { return this.results.filter((r) => r.passed).length; }
  get allPassed() { return this.medians.length > 0 && this.passed === this.medians.length; }
  get accuracy() {
    return this.results.length ? this.results.reduce((sum, r) => sum + r.accuracy, 0) / this.results.length : 0;
  }
  submit(points) {
    if (this.done || points.length < 2) return null;
    const score = scoreStroke(points, this.medians[this.index], this.size);
    this.attempts++;
    const advanced = score.passed || this.attempts >= 3;
    if (advanced) {
      this.results.push(score);
      this.index++;
      this.attempts = 0;
    }
    return { ...score, advanced, assisted: advanced && !score.passed };
  }
}
