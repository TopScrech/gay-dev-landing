<script lang="ts">
  import Asset from '../components/Asset.svelte'
  import WishlistButton from '../components/WishlistButton.svelte'
  import { formatDate, posts } from '../lib/posts'
  import { GAME_TITLE, LINKS, TAGLINE, TRAILER_URL } from '../lib/site'

  let logoFailed = $state(false)
  let playing = $state(false)

  const features = [
    {
      title: 'Tools that shouldn’t work',
      text: 'A pepper mill that grinds out hexes. A butterfly net that only catches shadows. A kettle that screams at ghosts. Craft them at the lodge bench, combine them, and misuse them creatively.',
      shot: 1,
    },
    {
      title: 'Monsters with habits',
      text: 'Everything in the marsh keeps a routine. Learn when the Bog Choir sleeps, what the Tallow Hound eats, and why nobody whistles near the old well. Your ledger fills in as you watch.',
      shot: 2,
    },
    {
      title: 'Puzzle fights at full panic',
      text: 'Every fight is a puzzle on a timer you can hear breathing. Swap tools mid-hunt, rearrange the ground under your feet, and work out the creature’s weakness before it works out yours.',
      shot: 3,
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
      <WishlistButton />
      <a class="btn btn-ghost" href="#trailer">Watch the trailer</a>
    </div>
  </div>
  <a class="scroll-cue" href="#premise"><span class="visually-hidden">Read about the game</span></a>
</section>

<section id="premise" class="premise container">
  <p class="lede">
    You are the new keeper of the {GAME_TITLE} hunting lodge. The last keeper left behind a crate of half-finished inventions, a
    map with teeth marks in it, and <em>forty-one unpaid monster contracts</em>.
  </p>
  <p class="lede-sub">Pack strange tools, learn what lives in the marsh, and try to get home before the lamps go out.</p>
</section>

<section id="trailer" class="trailer container" aria-label="Trailer">
  <div class="player">
    {#if playing && TRAILER_URL}
      <iframe src="{TRAILER_URL}?autoplay=1" title="{GAME_TITLE} trailer" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>
    {:else}
      <Asset src="/images/trailer-poster.jpg" alt="" ratio="16 / 9" />
      <button class="play" disabled={!TRAILER_URL} onclick={() => (playing = true)}>
        <span class="play-icon" aria-hidden="true"></span>
        {TRAILER_URL ? 'Play the trailer' : 'Trailer coming soon'}
      </button>
    {/if}
  </div>
</section>

<section class="features container" aria-labelledby="features-title">
  <h2 id="features-title" class="section-title">What’s in the crate</h2>
  {#each features as f, i (f.title)}
    <article class="feature" class:flip={i % 2 === 1}>
      <Asset src="/images/screenshots/0{f.shot}.jpg" alt="Screenshot: {f.title}" ratio="16 / 10" />
      <div class="feature-text">
        <h3>{f.title}</h3>
        <p>{f.text}</p>
      </div>
    </article>
  {/each}
</section>

<section class="gallery container" aria-labelledby="gallery-title">
  <h2 id="gallery-title" class="section-title">Postcards from the marsh</h2>
  <div class="gallery-grid">
    {#each [1, 2, 3, 4] as n (n)}
      <Asset class="shot shot-{n}" src="/images/screenshots/0{n}.jpg" alt="Screenshot {n}" />
    {/each}
  </div>
</section>

<section class="latest container" aria-labelledby="latest-title">
  <div class="latest-head">
    <h2 id="latest-title" class="section-title">From the dev blog</h2>
    <a class="text-link" href="/devlog">Read all posts</a>
  </div>
  <ol class="post-rows">
    {#each posts.slice(0, 3) as post (post.slug)}
      <li>
        <a href="/devlog/{post.slug}">
          <span class="row-meta"><time datetime={post.date}>{formatDate(post.date)}</time></span>
          <span class="row-title">{post.title}</span>
          <span class="row-excerpt">{post.excerpt}</span>
        </a>
      </li>
    {/each}
  </ol>
</section>

<section class="cta" aria-labelledby="cta-title">
  <Asset cover src="/images/cta.jpg" alt="" />
  <div class="cta-inner container">
    <h2 id="cta-title">The lamps go out at nine</h2>
    <p>Wishlist {GAME_TITLE} so you hear when the lodge opens, or come and argue about monsters with us on Discord.</p>
    <div class="actions">
      <WishlistButton />
      <a class="btn btn-ghost" href={LINKS.discord}>Join the Discord</a>
    </div>
  </div>
</section>

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
    text-shadow: 0 4px 40px oklch(0.14 0.05 320 / 0.7);
  }
  .title img { display: block; width: min(640px, 80vw); height: auto; }
  .tagline {
    max-width: 30ch;
    margin: 0;
    font-size: clamp(1.1rem, 2vw, 1.35rem);
    font-weight: 500;
    line-height: 1.45;
    text-shadow: 0 1px 18px oklch(0.14 0.05 320 / 0.9);
  }
  .actions { display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 12px; margin-top: 8px; }
  .actions .btn { min-height: 64px; padding-inline: 26px; }
  .hero .btn-ghost { background: oklch(0.14 0.04 310 / 0.35); }
  .scroll-cue {
    position: absolute;
    bottom: 28px;
    left: 50%;
    width: 28px;
    height: 44px;
    margin-left: -14px;
    border: 1.5px solid oklch(0.95 0.015 300 / 0.6);
    border-radius: 14px;
  }
  .scroll-cue::after {
    content: '';
    position: absolute;
    top: 9px;
    left: 50%;
    width: 4px;
    height: 8px;
    margin-left: -2px;
    border-radius: 2px;
    background: var(--wisp);
    animation: cue 2.2s var(--ease-out) infinite;
  }
  @keyframes cue {
    from { opacity: 1; transform: translateY(0); }
    to { opacity: 0; transform: translateY(14px); }
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

  .player { position: relative; border-radius: var(--radius); overflow: hidden; box-shadow: 0 40px 80px -30px oklch(0.08 0.03 305 / 0.9); }
  .player iframe { display: block; width: 100%; aspect-ratio: 16 / 9; border: 0; }
  .play {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 16px;
    width: 100%;
    border: 0;
    background: oklch(0.12 0.03 305 / 0.25);
    color: var(--ink);
    font: 700 1rem var(--font-body);
    cursor: pointer;
    transition: background-color 0.3s;
  }
  .play:disabled { cursor: default; }
  .play:not(:disabled):hover { background: oklch(0.12 0.03 305 / 0.1); }
  .play-icon {
    display: grid;
    place-items: center;
    width: clamp(64px, 9vw, 96px);
    aspect-ratio: 1;
    border-radius: 50%;
    background: var(--wisp);
    box-shadow: 0 0 0 10px oklch(0.88 0.17 128 / 0.18), 0 0 48px oklch(0.88 0.17 128 / 0.4);
    transition: transform 0.4s var(--ease-out);
  }
  .play-icon::after {
    content: '';
    margin-left: 12%;
    border-style: solid;
    border-width: 14px 0 14px 24px;
    border-color: transparent transparent transparent oklch(0.18 0.05 305);
  }
  .play:not(:disabled):hover .play-icon { transform: scale(1.06); }
  .play:disabled .play-icon { opacity: 0.8; }

  .section-title { font-size: clamp(2.4rem, 5.5vw, 4rem); }
  .features { padding-block: clamp(96px, 13vw, 180px) clamp(48px, 6vw, 80px); }
  .features .section-title { margin-bottom: clamp(40px, 6vw, 80px); }
  .feature {
    display: grid;
    grid-template-columns: 1.35fr 1fr;
    align-items: center;
    gap: clamp(28px, 5vw, 80px);
  }
  .feature + .feature { margin-top: clamp(56px, 9vw, 120px); }
  .feature.flip { grid-template-columns: 1fr 1.35fr; }
  .feature.flip :global(.asset) { order: 2; }
  .feature h3 { font-size: clamp(1.9rem, 3.4vw, 2.75rem); }
  .feature p { max-width: 42ch; margin: 18px 0 0; color: var(--ink-soft); font-size: 1.075rem; }

  .gallery { padding-block: clamp(64px, 9vw, 120px); }
  .gallery .section-title { margin-bottom: clamp(28px, 4vw, 48px); }
  .gallery-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: clamp(10px, 1.4vw, 18px);
  }
  .gallery-grid :global(.shot-1), .gallery-grid :global(.shot-4) { grid-column: span 2; aspect-ratio: 16 / 9; }
  .gallery-grid :global(.shot-2), .gallery-grid :global(.shot-3) { height: 100%; }

  .latest { padding-block: clamp(64px, 9vw, 120px) clamp(96px, 12vw, 160px); }
  .latest-head { display: flex; justify-content: space-between; align-items: baseline; gap: 24px; flex-wrap: wrap; margin-bottom: 24px; }
  .post-rows { list-style: none; margin: 0; padding: 0; border-top: 1px solid var(--night-line); }
  .post-rows li { border-bottom: 1px solid var(--night-line); }
  .post-rows a {
    display: grid;
    grid-template-columns: 13rem 1fr 1.2fr;
    align-items: baseline;
    gap: 8px 32px;
    padding: 28px 0;
    transition: padding 0.4s var(--ease-out);
  }
  .row-meta { color: var(--ink-soft); font-size: 0.9rem; font-variant-numeric: tabular-nums; }
  .row-title { font-family: var(--font-display); font-size: clamp(1.5rem, 2.4vw, 1.9rem); line-height: 1.1; }
  .row-excerpt { color: var(--ink-soft); }
  .post-rows a:hover .row-title { color: var(--wisp); }

  .cta {
    position: relative;
    display: flex;
    align-items: flex-start;
    min-height: clamp(520px, 72vh, 720px);
    padding-top: clamp(72px, 10vw, 140px);
    isolation: isolate;
    overflow: hidden;
  }
  .cta :global(.asset) { z-index: -1; }
  .cta::before {
    content: '';
    position: absolute;
    inset: 0 0 auto;
    height: 40%;
    z-index: -1;
    background: linear-gradient(var(--night), transparent);
  }
  .cta-inner { text-align: center; display: grid; justify-items: center; gap: 16px; }
  .cta h2 { font-size: clamp(2.4rem, 6vw, 4.5rem); }
  .cta p { max-width: 46ch; margin: 0; font-size: 1.1rem; }

  @media (max-width: 860px) {
    .feature, .feature.flip { grid-template-columns: 1fr; }
    .feature.flip :global(.asset) { order: 0; }
    .post-rows a { grid-template-columns: 1fr; }
  }
  @media (max-width: 640px) {
    .gallery-grid { grid-template-columns: 1fr; }
    .gallery-grid :global(.shot) { grid-column: auto !important; aspect-ratio: 16 / 9 !important; height: auto !important; }
    .lede-sub { margin-left: 0; }
  }
  @media (prefers-reduced-motion: reduce) {
    .hero-inner, .scroll-cue::after { animation: none; }
  }
</style>
