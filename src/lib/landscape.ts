// Procedural marsh scenery. Used live by <Scene> and to generate the
// fallback images in public/images/fallback (see scripts/fallbacks.ts)

export type Palette = {
  sky: [string, string, string]
  glow: string
  moon: string
  layers: [string, string, string, string]
  wisp: string
}

const wisp = 'oklch(0.88 0.17 128)'

export const palettes = {
  dusk: {
    sky: ['oklch(0.17 0.04 300)', 'oklch(0.3 0.08 330)', 'oklch(0.6 0.14 42)'],
    glow: 'oklch(0.72 0.15 50)',
    moon: 'oklch(0.88 0.08 75)',
    layers: ['oklch(0.42 0.1 350)', 'oklch(0.31 0.075 325)', 'oklch(0.225 0.05 310)', 'oklch(0.16 0.035 305)'],
    wisp,
  },
  bog: {
    sky: ['oklch(0.16 0.03 250)', 'oklch(0.28 0.05 205)', 'oklch(0.52 0.08 165)'],
    glow: 'oklch(0.72 0.12 150)',
    moon: 'oklch(0.9 0.06 140)',
    layers: ['oklch(0.38 0.06 185)', 'oklch(0.29 0.05 200)', 'oklch(0.21 0.04 230)', 'oklch(0.155 0.03 260)'],
    wisp,
  },
  hex: {
    sky: ['oklch(0.15 0.04 290)', 'oklch(0.27 0.09 300)', 'oklch(0.5 0.13 320)'],
    glow: 'oklch(0.66 0.16 330)',
    moon: 'oklch(0.87 0.08 320)',
    layers: ['oklch(0.37 0.1 305)', 'oklch(0.27 0.08 300)', 'oklch(0.2 0.05 295)', 'oklch(0.15 0.035 295)'],
    wisp,
  },
  ember: {
    sky: ['oklch(0.15 0.03 30)', 'oklch(0.28 0.08 25)', 'oklch(0.6 0.15 45)'],
    glow: 'oklch(0.76 0.15 58)',
    moon: 'oklch(0.9 0.1 80)',
    layers: ['oklch(0.39 0.1 25)', 'oklch(0.28 0.07 18)', 'oklch(0.2 0.045 10)', 'oklch(0.15 0.03 350)'],
    wisp,
  },
} satisfies Record<string, Palette>

export type PaletteName = keyof typeof palettes

export function rng(seed: number) {
  return () => {
    seed = (seed + 0x6d2b79f5) | 0
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed)
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}

const f = (n: number) => Math.round(n * 10) / 10

type RidgeSpec = {
  base: number
  amp: number
  trees?: { count: number; min: number; max: number }
  reeds?: { count: number; min: number; max: number }
}

function ridge(width: number, height: number, spec: RidgeSpec, r: () => number) {
  const phase = [r() * 6.28, r() * 6.28, r() * 6.28]
  const k = [1.2, 2.7, 6.1].map((n) => (n / width) * Math.PI * 2)
  const y = (x: number) =>
    spec.base - spec.amp * (0.55 * Math.sin(x * k[0] + phase[0]) + 0.3 * Math.sin(x * k[1] + phase[1]) + 0.15 * Math.sin(x * k[2] + phase[2]))

  let d = `M0 ${height} L0 ${f(y(0))}`
  for (let x = 16; x <= width; x += 16) d += ` L${x} ${f(y(x))}`
  d += ` L${width} ${height}Z`

  if (spec.trees) {
    const { count, min, max } = spec.trees
    for (let i = 0; i < count; i++) {
      const x = r() * width
      const h = min + r() * (max - min)
      d += pine(x, y(x) + h * 0.06, h, (r() - 0.5) * h * 0.3, r)
    }
  }

  if (spec.reeds) {
    const { count, min, max } = spec.reeds
    for (let i = 0; i < count; i++) {
      const x = r() * width
      const h = min + r() * (max - min)
      const base = y(x) + 2
      const lean = (r() - 0.5) * h * 0.5
      d += ` M${f(x - 1.6)} ${f(base)} Q${f(x + lean * 0.3)} ${f(base - h * 0.6)} ${f(x + lean)} ${f(base - h)} Q${f(x + lean * 0.3 + 1)} ${f(base - h * 0.5)} ${f(x + 1.6)} ${f(base)}Z`
    }
  }

  return { d, y }
}

// A crooked pine: stacked tiers whose tips drift with `lean`
function pine(x: number, ground: number, h: number, lean: number, r: () => number) {
  const w = h * (0.26 + r() * 0.1)
  const tiers = 3 + Math.floor(r() * 2)
  let d = ` M${f(x - h * 0.025)} ${f(ground)} L${f(x + lean * 0.3)} ${f(ground - h * 0.5)} L${f(x + h * 0.025)} ${f(ground)}Z`
  for (let t = 0; t < tiers; t++) {
    const p0 = 0.18 + (t / tiers) * 0.62
    const p1 = Math.min(1, p0 + 0.42)
    const bw = w * (1 - t / (tiers + 0.6))
    const by = ground - h * p0
    const tx = x + lean * p1
    const ty = ground - h * p1
    const sag = h * 0.03
    d += ` M${f(x + lean * p0 - bw)} ${f(by)} Q${f(x + lean * p0)} ${f(by - sag)} ${f(x + lean * p0 + bw)} ${f(by + sag * 0.6)} L${f(tx)} ${f(ty)}Z`
  }
  return d
}

// `fog` is a mist band (y, height, color) that sits in the valley in front of the ridge
export type Layer = { d: string; fill: string; depth: number; fog?: { y: number; h: number; color: string } }

export type SceneData = {
  width: number
  height: number
  palette: Palette
  stars: { x: number; y: number; r: number; o: number }[]
  moon: { x: number; y: number; r: number }
  // A spot inside the third ridge where something can lurk
  lurk: { x: number; y: number }
  layers: Layer[]
}

export function buildScene(opts: { width: number; height: number; seed: number; palette: Palette; moonX?: number }): SceneData {
  const { width: w, height: h, palette } = opts
  const r = rng(opts.seed)
  const specs: RidgeSpec[] = [
    { base: h * 0.64, amp: h * 0.06 },
    { base: h * 0.71, amp: h * 0.045, trees: { count: Math.round(w / 34), min: h * 0.05, max: h * 0.11 } },
    { base: h * 0.81, amp: h * 0.04, trees: { count: Math.round(w / 70), min: h * 0.12, max: h * 0.24 } },
    { base: h * 0.93, amp: h * 0.02, reeds: { count: Math.round(w / 7), min: h * 0.02, max: h * 0.07 } },
  ]
  const depths = [0.34, 0.22, 0.1, 0]
  const ridges = specs.map((spec) => ridge(w, h, spec, r))
  const fogColors = [palette.sky[2], palette.layers[0], palette.layers[1]]
  const layers = ridges.map((rg, i) => ({
    d: rg.d,
    fill: palette.layers[i],
    depth: depths[i],
    fog: i < 3 ? { y: specs[i].base - h * 0.02, h: h * 0.1, color: fogColors[i] } : undefined,
  }))
  const lurkX = w * 0.43
  const lurk = { x: lurkX, y: ridges[2].y(lurkX) + h * 0.045 }
  const stars = Array.from({ length: Math.round(w / 22) }, () => ({
    x: f(r() * w),
    y: f(r() * h * 0.46),
    r: f(0.4 + r() * 1.3),
    o: f(0.25 + r() * 0.6),
  }))
  const moon = { x: w * (opts.moonX ?? 0.7), y: h * 0.58, r: h * 0.13 }
  return { width: w, height: h, palette, stars, moon, lurk, layers }
}

// Hunter in a crooked wide-brim hat, holding a lantern. Used for portrait fallbacks
export function figure(cx: number, base: number, s: number, fill: string, glow: string) {
  const p = (x: number, y: number) => `${f(cx + x * s)} ${f(base - y * s)}`
  return `
  <circle cx="${f(cx + 0.62 * s)}" cy="${f(base - 0.5 * s)}" r="${f(0.5 * s)}" fill="url(#lantern)"/>
  <circle cx="${f(cx)}" cy="${f(base - 1.1 * s)}" r="${f(0.2 * s)}" fill="${fill}"/>
  <path fill="${fill}" d="M${p(-0.55, 0)} Q${p(-0.52, 0.62)} ${p(-0.3, 0.96)} Q${p(0, 1.02)} ${p(0.3, 0.96)} Q${p(0.52, 0.62)} ${p(0.55, 0)}Z
    M${p(-0.5, 1.22)} Q${p(0, 1.34)} ${p(0.52, 1.26)} Q${p(0.02, 1.16)} ${p(-0.5, 1.22)}Z
    M${p(-0.2, 1.25)} Q${p(-0.2, 1.52)} ${p(-0.06, 1.62)} Q${p(0.12, 1.74)} ${p(0.36, 1.58)} Q${p(0.2, 1.58)} ${p(0.15, 1.46)} L${p(0.2, 1.26)}Z
    M${p(0.3, 0.62)} L${p(0.62, 0.66)} L${p(0.62, 0.6)} L${p(0.34, 0.54)}Z"/>
  <circle cx="${f(cx + 0.62 * s)}" cy="${f(base - 0.5 * s)}" r="${f(0.07 * s)}" fill="${glow}"/>`
}

export function sceneToSvg(scene: SceneData, extra = '') {
  const { width: w, height: h, palette: p, moon } = scene
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" preserveAspectRatio="xMidYMax slice">
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="${p.sky[0]}"/><stop offset=".45" stop-color="${p.sky[1]}"/><stop offset=".72" stop-color="${p.sky[2]}"/>
  </linearGradient>
  <radialGradient id="moonglow"><stop offset=".35" stop-color="${p.glow}" stop-opacity=".55"/><stop offset="1" stop-color="${p.glow}" stop-opacity="0"/></radialGradient>
  <radialGradient id="lantern"><stop offset="0" stop-color="${p.wisp}" stop-opacity=".55"/><stop offset="1" stop-color="${p.wisp}" stop-opacity="0"/></radialGradient>
</defs>
<rect width="${w}" height="${h}" fill="url(#sky)"/>
${scene.stars.map((s) => `<circle cx="${s.x}" cy="${s.y}" r="${s.r}" fill="${p.moon}" opacity="${s.o}"/>`).join('')}
<circle cx="${f(moon.x)}" cy="${f(moon.y)}" r="${f(moon.r * 2.2)}" fill="url(#moonglow)"/>
<circle cx="${f(moon.x)}" cy="${f(moon.y)}" r="${f(moon.r)}" fill="${p.moon}"/>
${scene.layers.map((l, i) => `<path fill="${l.fill}" d="${l.d}"/>` + (l.fog ? `<linearGradient id="fog${i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${l.fog.color}" stop-opacity="0"/><stop offset=".6" stop-color="${l.fog.color}" stop-opacity=".55"/><stop offset="1" stop-color="${l.fog.color}" stop-opacity="0"/></linearGradient><rect y="${f(l.fog.y)}" width="${w}" height="${f(l.fog.h)}" fill="url(#fog${i})"/>` : '')).join('\n')}
${extra}
</svg>
`
}
