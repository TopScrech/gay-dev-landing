<script lang="ts">
  import Asset from '../components/Asset.svelte'
  // import MerchSection from '../components/MerchSection.svelte'
  import TrailerPlayer from '../components/TrailerPlayer.svelte'
  // import WishlistButton from '../components/WishlistButton.svelte'
  import { GAME_TITLE, STUDIO_NAME, TAGLINE } from '../lib/site'

  let logoFailed = $state(false)

  const features = [
    {
      title: 'Breathe in, fire back',
      text: 'Built for fights. Suck in air to hurt creatures and tear through cobwebs, or grab an object, hold it, and launch it back at whatever is chasing you.',
      art: '/images/tools/air-tool.webp',
      chip: 'a' as const,
    },
    {
      title: 'The monster eye',
      text: 'Click to see what used to be there. A cane’s silhouette against the wall, the same cane later in an NPC’s hand. If a shape has no match, something has gone missing. The view is warped and narrow while you look.',
      art: '/images/tools/monster-eye.webp',
      chip: 'a' as const,
      tint: true,
    },
    {
      title: 'A lamp with a fairy in it',
      text: 'Her glow makes fairy dust visible to the naked eye, and she changes color when other fae are near. Just walk close enough and watch her light.',
      art: '/images/tools/lamp.webp',
      chip: 'a' as const,
    },
  ]
</script>

<section class="hero">
  <Asset cover src="/images/key-art.jpg" alt="" />
  <div class="hero-inner">
    <h1 class="title">
      {#if logoFailed}
        {GAME_TITLE}
      {:else}
        <img src="/images/logo.svg" alt={GAME_TITLE} onerror={() => (logoFailed = true)} />
      {/if}
    </h1>
    <p class="tagline">{TAGLINE}</p>
    <div class="actions">
      <!-- <WishlistButton /> -->
      <a class="btn btn-ghost" href="#trailer">Watch the teaser</a>
    </div>
  </div>
  <p class="credit">A game by <a href="/">{STUDIO_NAME}</a></p>
</section>

<section id="premise" class="premise container">
  <p class="lede">
    You are the new keeper of the {GAME_TITLE} hunting lodge. The last keeper left behind a crate of half-finished inventions, a
    map with teeth marks in it, and <em>forty-one unpaid monster contracts</em>.
  </p>
  <p class="lede-sub">Pack strange tools, learn what lives in the marsh, and try to get home before the lamps go out.</p>
</section>

<section id="trailer" class="trailer container" aria-label="Trailer">
  <TrailerPlayer />
</section>

<section class="features container" aria-labelledby="features-title">
  <h2 id="features-title" class="section-title">Tools that shouldn’t work</h2>
  {#each features as f (f.title)}
    <article class="feature">
      <Asset class={f.tint ? 'tint' : ''} src={f.art} alt={f.title} ratio="1 / 1" chip={f.chip} />
      <div class="feature-text">
        <h3>{f.title}</h3>
        <p>{f.text}</p>
      </div>
    </article>
  {/each}
</section>

<!-- <section class="gallery container" aria-labelledby="gallery-title">
  <h2 id="gallery-title" class="section-title">Postcards from the marsh</h2>
  <div class="gallery-grid">
    {#each [1, 2, 3, 4] as n (n)}
      <Asset class="shot shot-{n}" src="/images/screenshots/0{n}.jpg" alt="Screenshot {n}" />
    {/each}
  </div>
</section> -->

<!-- <MerchSection /> -->

<style>
  .hero {
    position: relative;
    display: grid;
    place-items: center;
    min-height: max(620px, 100svh);
    padding: var(--header-h) var(--gutter) 18vh;
    text-align: center;
    isolation: isolate;
  }
  .hero :global(.asset) { z-index: -2; }
  .hero::after {
    content: '';
    position: absolute;
    inset: auto 0 0;
    height: 18vh;
    z-index: -1;
    background: linear-gradient(to bottom, transparent, var(--night));
  }
  .hero-inner {
    display: grid;
    justify-items: center;
    gap: 20px;
    margin-top: -12vh;
    animation: hero-in 1.4s var(--ease-out) 0.5s backwards;
  }
  @keyframes hero-in {
    from { opacity: 0; transform: translateY(16px); filter: blur(6px); }
  }
  .title {
    font-size: clamp(4rem, 14vw, 6rem);
    font-weight: 800;
    letter-spacing: 0.01em;
    text-shadow: 0 4px 40px oklch(from var(--night-deep) l c h / 0.7);
  }
  .title img { display: block; width: min(640px, 80vw); height: auto; }
  .tagline {
    max-width: 30ch;
    margin: 0;
    font-size: clamp(1.1rem, 2vw, 1.35rem);
    font-weight: 500;
    line-height: 1.45;
    text-shadow: 0 1px 18px oklch(from var(--night-deep) l c h / 0.9);
  }
  .actions { display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 12px; margin-top: 8px; }
  .actions .btn-ghost {
    --oak: oklch(0.38 0.09 295);
    --oak-edge: oklch(0.2 0.05 288);
    min-height: 64px;
    padding-inline: 36px;
  }
  .premise { padding-block: clamp(72px, 11vw, 160px) clamp(48px, 7vw, 96px); }
  .lede {
    max-width: 30ch;
    margin: 0;
    font-family: var(--font-display);
    font-size: clamp(1.9rem, 4.2vw, 3.25rem);
    font-weight: 500;
    line-height: 1.12;
  }
  .lede em { font-style: normal; color: var(--ember); }
  .lede-sub {
    max-width: 44ch;
    margin: 28px 0 0 auto;
    font-size: clamp(1.05rem, 1.5vw, 1.2rem);
    color: var(--ink-soft);
  }

  .section-title { font-size: clamp(2.4rem, 5.5vw, 4rem); }
  .features { padding-block: clamp(96px, 13vw, 180px) clamp(48px, 6vw, 80px); }
  .features .section-title { margin-bottom: clamp(40px, 6vw, 80px); }
  .feature {
    display: grid;
    grid-template-columns: minmax(0, 360px) 1fr;
    align-items: center;
    gap: clamp(28px, 5vw, 80px);
  }
  .feature + .feature { margin-top: clamp(32px, 5vw, 64px); }
  /* Prints pinned up by hand: never quite level */
  .feature :global(.asset) { rotate: -0.8deg; }
  .feature:nth-of-type(even) :global(.asset) { rotate: 0.7deg; }
  /* Transparent art sits on a dark purple panel instead of the default print color */
  .feature :global(.asset.tint) { background: radial-gradient(circle, oklch(0.3 0.11 300), oklch(0.18 0.07 295)); }
  .feature h3 { font-size: clamp(1.9rem, 3.4vw, 2.75rem); }
  .feature p { max-width: 42ch; margin: 18px 0 0; color: var(--ink-soft); font-size: 1.075rem; }

  /* Gallery section is commented out above
  .gallery { padding-block: clamp(64px, 9vw, 120px); }
  .gallery .section-title { margin-bottom: clamp(28px, 4vw, 48px); }
  .gallery-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: clamp(10px, 1.4vw, 18px);
  }
  .gallery-grid :global(.shot-1), .gallery-grid :global(.shot-4) { grid-column: span 2; aspect-ratio: 16 / 9; }
  .gallery-grid :global(.shot-2), .gallery-grid :global(.shot-3) { height: 100%; }
  .gallery-grid :global(.shot-1) { rotate: -0.6deg; }
  .gallery-grid :global(.shot-2) { rotate: 1deg; }
  .gallery-grid :global(.shot-3) { rotate: -1.1deg; }
  .gallery-grid :global(.shot-4) { rotate: 0.5deg; } */

  .credit {
    position: absolute;
    left: 0;
    right: 0;
    bottom: clamp(20px, 4vh, 40px);
    margin: 0;
    font-size: 0.95rem;
    color: var(--ink-soft);
    text-shadow: 0 1px 12px oklch(from var(--night-deep) l c h / 0.95);
  }
  .credit a {
    font-family: var(--font-display);
    font-size: 1.25rem;
    color: var(--ink);
    transition: color 0.2s;
  }
  .credit a:hover { color: var(--wisp); }

  @media (max-width: 860px) {
    .feature { grid-template-columns: 1fr; }
    .feature :global(.asset) { width: min(100%, 320px); justify-self: center; }
  }
  @media (max-width: 640px) {
    /* .gallery-grid { grid-template-columns: 1fr; }
    .gallery-grid :global(.shot) { grid-column: auto !important; aspect-ratio: 16 / 9 !important; height: auto !important; } */
    .lede-sub { margin-left: 0; }
  }
  @media (prefers-reduced-motion: reduce) {
    .hero-inner { animation: none; }
  }
</style>
