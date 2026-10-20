<script lang="ts">
  // The studio home's first screen: a layered night scene with the studio name, one line about us, and the way to the game
  import Asset from './Asset.svelte'
  import { GAME_TITLE, STUDIO_NAME, games } from '../lib/site'

  const game = games[0]

  // Scene layers, back to front. `depth` is how far a layer drifts per pixel scrolled: far things lag, near things keep up
  const layers = [
    { name: 'sky', src: '/images/home/scene/sky.jpg', depth: 0.55 },
    { name: 'hills', src: '/images/home/scene/hills.png', depth: 0.38 },
    { name: 'marsh', src: '/images/home/scene/marsh.png', depth: 0.2 },
  ]

  let hero: HTMLElement | undefined = $state()

  // Feeds the scroll offset to CSS while the scene is on screen; reduced motion never attaches the listener
  $effect(() => {
    const el = hero
    if (!el) return
    const still = matchMedia('(prefers-reduced-motion: reduce)')
    let frame = 0
    const update = () => {
      frame = 0
      const y = Math.min(window.scrollY, el.offsetHeight)
      el.style.setProperty('--scroll', `${y}px`)
      el.style.setProperty('--fade', `${Math.max(0, 1 - y / 700)}`)
    }
    const onScroll = () => {
      if (!frame) frame = requestAnimationFrame(update)
    }
    const sync = () => {
      window.removeEventListener('scroll', onScroll)
      if (still.matches) {
        el.style.removeProperty('--scroll')
        el.style.removeProperty('--fade')
      } else {
        window.addEventListener('scroll', onScroll, { passive: true })
        update()
      }
    }
    sync()
    still.addEventListener('change', sync)
    return () => {
      window.removeEventListener('scroll', onScroll)
      still.removeEventListener('change', sync)
      cancelAnimationFrame(frame)
    }
  })
</script>

<section class="scene" bind:this={hero} aria-labelledby="studio-name">
  <div class="layers" aria-hidden="true">
    {#each layers as layer (layer.name)}
      <div class="layer layer-{layer.name}" style:--depth={layer.depth}>
        <Asset cover={layer.name === 'sky'} cutout={layer.name !== 'sky'} src={layer.src} alt="" eager />
      </div>
      {#if layer.name === 'marsh'}
        <span class="lantern"></span>
      {/if}
    {/each}
  </div>

  <div class="scene-copy container">
    <h1 id="studio-name">{STUDIO_NAME}</h1>
    <p class="pitch">
      A student studio in Groningen making lantern-lit games about clever tools, crooked marshes, and the creatures that would rather not be
      caught
    </p>
    <a class="btn btn-ghost meet" href={game.href}>Meet {GAME_TITLE}</a>
  </div>
</section>

<style>
  /* ── The scene ─────────────────────────────────────────── */
  .scene {
    --scroll: 0px;
    position: relative;
    display: flex;
    align-items: flex-start;
    min-height: max(620px, 100svh);
    padding: calc(var(--header-h) + clamp(48px, 12vh, 140px)) 0 0;
    overflow: hidden;
    isolation: isolate;
  }
  .layers { position: absolute; inset: 0; z-index: -1; }
  .layer {
    position: absolute;
    inset: auto 0 0;
    transform: translate3d(0, calc(var(--scroll) * var(--depth)), 0);
    will-change: transform;
  }
  .layer :global(.asset) { height: 100%; }
  .layer :global(img) { object-position: center bottom; }
  .layer :global(.cutout img) { object-fit: cover; }

  /* Until the art lands, each blank layer becomes a painted silhouette in its own shade of night */
  .layer-sky { inset: -10% 0 0; --night-raise: oklch(0.24 0.075 282); }
  .layer-sky::after {
    content: '';
    position: absolute;
    inset: 0;
    background:
      radial-gradient(circle at 76% 24%, oklch(0.93 0.04 95 / 0.9) 0 clamp(18px, 2.6vw, 34px), oklch(0.85 0.06 95 / 0.18) clamp(20px, 3vw, 38px), transparent clamp(80px, 14vw, 200px)),
      linear-gradient(oklch(0.16 0.05 285 / 0.6), transparent 60%);
    pointer-events: none;
  }
  .layer-sky:not(:has(:global(.blank)))::after { display: none; }
  .layer-hills { height: 58%; --night-raise: oklch(0.2 0.06 278); }
  .layer-marsh { height: 40%; --night-raise: oklch(0.16 0.045 220); }
  .layer-hills:has(:global(.blank)) { mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100' preserveAspectRatio='none'%3E%3Cpath d='M0 34C9 22 18 26 28 14S46 22 57 17 77 3 88 13L100 9V100H0Z'/%3E%3C/svg%3E") 0 0 / 100% 100%; }
  .layer-marsh:has(:global(.blank)) { mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100' preserveAspectRatio='none'%3E%3Cpath d='M0 30C7 24 13 29 21 21S37 28 45 24 61 13 71 22 88 27 100 18V100H0Z'/%3E%3C/svg%3E") 0 0 / 100% 100%; }

  /* One lit window out on the marsh, and the faint glow it throws on the water */
  .lantern {
    position: absolute;
    left: 22%;
    bottom: 27%;
    width: 7px;
    height: 9px;
    background: var(--ember);
    border-radius: 2px;
    box-shadow: 0 0 10px 3px oklch(from var(--ember) l c h / 0.7), 0 0 60px 26px oklch(from var(--ember) l c h / 0.16);
    transform: translate3d(0, calc(var(--scroll) * 0.2), 0);
    animation: flicker 5s steps(1) infinite;
  }
  @keyframes flicker {
    0%, 100% { opacity: 1; }
    47% { opacity: 0.75; }
    49% { opacity: 1; }
    83% { opacity: 0.85; }
  }

  /* A dusk scrim behind the words, and the scene sinking into the page below */
  .scene::before {
    content: '';
    position: absolute;
    inset: 0;
    z-index: -1;
    background:
      radial-gradient(70% 55% at 30% 30%, oklch(from var(--night-deep) l c h / 0.55), transparent 70%),
      linear-gradient(to bottom, transparent 70%, var(--night));
    pointer-events: none;
  }

  .scene-copy {
    display: grid;
    justify-items: start;
    gap: 22px;
    transform: translate3d(0, calc(var(--scroll) * 0.3), 0);
    opacity: var(--fade, 1);
    animation: copy-in 1.2s var(--ease-out) 0.3s backwards;
  }
  @keyframes copy-in {
    from { opacity: 0; translate: 0 14px; }
  }
  h1 {
    font-size: clamp(3.4rem, 12vw, 7.5rem);
    font-weight: 800;
    text-shadow: 0 4px 40px oklch(from var(--night-deep) l c h / 0.8);
  }
  .pitch {
    max-width: 36ch;
    margin: 0;
    font-size: clamp(1.1rem, 2vw, 1.35rem);
    font-weight: 500;
    line-height: 1.45;
    text-shadow: 0 1px 18px oklch(from var(--night-deep) l c h / 0.95);
  }
  /* Secondary, in the same dusty grape as the store button */
  .meet {
    --oak: oklch(0.38 0.09 295);
    --oak-edge: oklch(0.2 0.05 288);
    min-height: 64px;
    margin-top: 6px;
    padding-inline: 36px;
    font-size: 1.15rem;
  }

  @media (max-width: 540px) {
    .lantern { left: 14%; }
  }
  @media (prefers-reduced-motion: reduce) {
    .layer, .lantern, .scene-copy { transform: none; will-change: auto; }
    .lantern, .scene-copy { animation: none; }
    .scene-copy { opacity: 1; }
  }
</style>
