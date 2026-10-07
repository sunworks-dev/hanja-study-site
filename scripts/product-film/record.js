// Phi 에이전트 Space에서 웹 베타 화면을 약 10fps로 녹화한다(430×860, 2배 해상도 → 860×1720 JPG + frames.json).
// 실행: REC_NAME=recall REC_SECONDS=7.5 REC_ACTIONS='[{"at":2.4,"x":116,"y":608}]' REC_OUT=<폴더> node ~/.claude/skills/phi-browser/scripts/runner.mjs < scripts/product-film/record.js
const fs = require('fs')
const name = process.env.REC_NAME, seconds = +process.env.REC_SECONDS, out = process.env.REC_OUT + '/' + name
const actions = JSON.parse(process.env.REC_ACTIONS || '[]')
fs.mkdirSync(out, { recursive: true })
await enterContext({ kind: 'agent', name: 'hanja-app-capture' })
const frames = []
const t0 = Date.now()
let next = 0
while (true) {
  const t = (Date.now() - t0) / 1000
  if (t > seconds) break
  if (next < actions.length && t >= actions[next].at) {
    const a = actions[next++]
    await click(a.x, a.y)
  }
  const shot = await cdp('Page.captureScreenshot', { format: 'jpeg', quality: 92 })
  const file = out + '/' + String(frames.length).padStart(4, '0') + '.jpg'
  fs.writeFileSync(file, Buffer.from(shot.data, 'base64'))
  frames.push({ file, t: +t.toFixed(3) })
  await wait(0.045)
}
fs.writeFileSync(out + '/frames.json', JSON.stringify(frames))
cliLog({ name, frames: frames.length, last: frames[frames.length - 1].t })
