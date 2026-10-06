// Phi 에이전트 Space에서 film.html을 프레임 단위로 찍는다.
// 실행: FILM_O=landscape FILM_OUT=<폴더> node ~/.claude/skills/phi-browser/scripts/runner.mjs < scripts/product-film/capture.js
// 먼저 저장소 루트에서 python3 -m http.server 4323 을 켠다.
const fs = require('fs')
const out = process.env.FILM_OUT
const orientation = process.env.FILM_O || 'landscape'
const [width, height] = orientation === 'portrait' ? [1080, 1920] : [1920, 1080]
await enterContext({ kind: 'agent', name: 'hanja-film-render' })
await cdp('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: false })
await goto('http://localhost:4323/scripts/product-film/film.html?o=' + orientation + '&v=' + Date.now())
await waitForFunction('window.filmReady === true', { timeout: 40 })
const { DURATION, FPS } = await js('window.FILM')
const total = DURATION * FPS
const started = Date.now()
for (let frame = 0; frame < total; frame++) {
  await js('seek(' + frame / FPS + ')')
  const shot = await cdp('Page.captureScreenshot', { format: 'jpeg', quality: 93, clip: { x: 0, y: 0, width, height, scale: 1 } })
  fs.writeFileSync(out + '/' + String(frame).padStart(5, '0') + '.jpg', Buffer.from(shot.data, 'base64'))
  if (frame % 150 === 0) await ping(600)
}
cliLog({ orientation, frames: total, seconds: Math.round((Date.now() - started) / 1000) })
