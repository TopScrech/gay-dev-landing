// Regenerates the placeholder art in public/images/fallback
// Run with: bun scripts/fallbacks.ts
import { mkdirSync, writeFileSync } from 'node:fs'
import { buildScene, figure, palettes, sceneToSvg, type PaletteName } from '../src/lib/landscape'

const out = new URL('../public/images/fallback/', import.meta.url)
mkdirSync(out, { recursive: true })
const write = (name: string, svg: string) => writeFileSync(new URL(name, out), svg)
const order: PaletteName[] = ['dusk', 'bog', 'hex', 'ember']

order.forEach((name, i) => {
  const palette = palettes[name]
  write(`shot-${i + 1}.svg`, sceneToSvg(buildScene({ width: 1600, height: 900, seed: 11 + i * 7, palette, moonX: [0.72, 0.3, 0.55, 0.8][i] })))
  write(`cover-${i + 1}.svg`, sceneToSvg(buildScene({ width: 1500, height: 1000, seed: 91 + i * 5, palette, moonX: [0.3, 0.7, 0.5, 0.25][i] })))

  const h = 1000
  const portrait = buildScene({ width: 800, height: h, seed: 40 + i * 3, palette, moonX: 0.28 })
  write(`portrait-${i + 1}.svg`, sceneToSvg(portrait, figure(400, h * 0.97, h * 0.34, palette.layers[3], palette.wisp)))
})

const group = buildScene({ width: 2100, height: 900, seed: 77, palette: palettes.dusk, moonX: 0.5 })
const hunters = [0.18, 0.34, 0.5, 0.66, 0.82]
  .map((x, i) => figure(2100 * x, 900 * 0.97, 900 * (0.28 + (i % 2) * 0.03), palettes.dusk.layers[3], palettes.dusk.wisp))
  .join('')
write('group.svg', sceneToSvg(group, hunters))
write('key-art.svg', sceneToSvg(buildScene({ width: 1600, height: 900, seed: 3, palette: palettes.dusk })))
console.log('fallbacks written')
