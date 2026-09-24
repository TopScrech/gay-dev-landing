<script lang="ts">
  import { onMount } from 'svelte'
  import { buildScene, palettes, rng, type PaletteName } from '../lib/landscape'

  type Props = { palette?: PaletteName; seed?: number; tall?: boolean; parallax?: boolean; eyes?: boolean }
  let { palette = 'dusk', seed = 3, tall = true, parallax = false, eyes = false }: Props = $props()

  const W = 1600
  const H = $derived(tall ? 900 : 620)
  const scene = $derived(buildScene({ width: W, height: H, seed, palette: palettes[palette] }))
  const p = $derived(scene.palette)
  const uid = $props.id()

  // Wisps drift over the lower half of the scene
  const wisps = $derived.by(() => {
    const r = rng(seed + 100)
    return Array.from({ length: 16 }, () => ({
      x: 4 + r() * 92,
      y: 48 + r() * 44,
      size: 3 + r() * 4,
      delay: -r() * 12,
      dur: 9 + r() * 8,
      dx: (r() - 0.5) * 80,
      dy: -20 - r() * 50,
    }))
  })

  let root: HTMLDivElement
  onMount(() => {
    if (!parallax || matchMedia('(prefers-reduced-motion: reduce)').matches) return
    let frame = 0
    const update = () => {
      frame = 0
      const y = Math.min(scrollY, root.offsetHeight)
      root.style.setProperty('--sy', `${y}px`)
    }
    const onScroll = () => (frame ||= requestAnimationFrame(update))
    addEventListener('scroll', onScroll, { passive: true })
    update()
    return () => {
      removeEventListener('scroll', onScroll)
      cancelAnimationFrame(frame)
    }
  })
</script>

<div class="scene" class:tall bind:this={root} aria-hidden="true">
  <svg class="layer" style="--d: .5" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMax slice">
    <defs>
      <linearGradient id="{uid}-sky" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color={p.sky[0]} />
        <stop offset=".45" stop-color={p.sky[1]} />
        <stop offset=".72" stop-color={p.sky[2]} />
      </linearGradient>
      <radialGradient id="{uid}-glow">
        <stop offset=".35" stop-color={p.glow} stop-opacity=".55" />
        <stop offset="1" stop-color={p.glow} stop-opacity="0" />
      </radialGradient>
    </defs>
    <rect width={W} height={H} fill="url(#{uid}-sky)" />
    {#each scene.stars as s, i (i)}
      <circle class="star" cx={s.x} cy={s.y} r={s.r} fill={p.moon} opacity={s.o} style:animation-delay="{-i * 0.37}s" />
    {/each}
    <circle cx={scene.moon.x} cy={scene.moon.y} r={scene.moon.r * 2.2} fill="url(#{uid}-glow)" />
    <circle cx={scene.moon.x} cy={scene.moon.y} r={scene.moon.r} fill={p.moon} />
  </svg>

  {#each scene.layers as layer, i (i)}
    <svg class="layer ridge" style="--d: {layer.depth}; --i: {i}" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMax slice">
      <g class="rise">
        <path fill={layer.fill} d={layer.d} />
        {#if layer.fog}
          <linearGradient id="{uid}-fog{i}" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stop-color={layer.fog.color} stop-opacity="0" />
            <stop offset=".6" stop-color={layer.fog.color} stop-opacity=".55" />
            <stop offset="1" stop-color={layer.fog.color} stop-opacity="0" />
          </linearGradient>
          <rect class="fog" y={layer.fog.y} width={W + 80} height={layer.fog.h} fill="url(#{uid}-fog{i})" />
        {/if}
        {#if eyes && i === 2}
          <!-- Something in the treeline is watching -->
          <g class="eyes">
            {#each [-1, 1] as side (side)}
              <g transform="rotate({side * -14} {scene.lurk.x + side * 17} {scene.lurk.y})">
                <ellipse cx={scene.lurk.x + side * 17} cy={scene.lurk.y} rx="8" ry="5" fill={p.wisp} />
              </g>
            {/each}
          </g>
        {/if}
      </g>
    </svg>
  {/each}

  <div class="wisps">
    {#each wisps as w, i (i)}
      <span
        style:left="{w.x}%"
        style:top="{w.y}%"
        style:width="{w.size}px"
        style:height="{w.size}px"
        style:animation-delay="{w.delay}s"
        style:animation-duration="{w.dur}s"
        style:--dx="{w.dx}px"
        style:--dy="{w.dy}px"
      ></span>
    {/each}
  </div>
</div>

<style>
  .scene {
    --sy: 0px;
    position: absolute;
    inset: 0;
    overflow: hidden;
    background: var(--night);
  }
  .layer {
    position: absolute;
    inset: -2px 0 0;
    width: 100%;
    height: calc(100% + 2px);
    transform: translate3d(0, calc(var(--sy) * var(--d)), 0);
    will-change: transform;
  }
  .rise {
    animation: rise 1.6s var(--ease-out) backwards;
    animation-delay: calc(var(--i) * 110ms + 150ms);
  }
  @keyframes rise {
    from { transform: translateY(60px); opacity: 0; }
  }
  .fog { animation: mist 14s ease-in-out infinite alternate; }
  @keyframes mist {
    to { transform: translateX(-40px); opacity: 0.6; }
  }
  .star { animation: twinkle 5s ease-in-out infinite alternate; }
  @keyframes twinkle {
    to { opacity: 0.15; }
  }
  .eyes ellipse {
    transform-box: fill-box;
    transform-origin: center;
    animation: blink 7s infinite;
    filter: drop-shadow(0 0 6px var(--wisp));
  }
  @keyframes blink {
    0%, 92%, 100% { transform: scaleY(1); }
    94%, 96% { transform: scaleY(0.08); }
  }
  .wisps span {
    position: absolute;
    border-radius: 50%;
    background: var(--wisp);
    box-shadow: 0 0 10px 3px oklch(0.88 0.17 128 / 0.45);
    animation: drift linear infinite;
    opacity: 0;
  }
  @keyframes drift {
    0% { transform: translate(0, 0); opacity: 0; }
    15% { opacity: 0.9; }
    50% { opacity: 0.35; }
    70% { opacity: 0.85; }
    100% { transform: translate(var(--dx), var(--dy)); opacity: 0; }
  }
  @media (prefers-reduced-motion: reduce) {
    .rise, .star, .fog, .eyes ellipse { animation: none; }
    .wisps span { animation: none; opacity: 0.6; }
  }
</style>
