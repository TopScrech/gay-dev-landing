<script lang="ts">
  import { LINKS, STUDIO_NAME, games } from '../lib/site'
  const year = new Date().getFullYear()
</script>

<footer class="site-footer">
  <div class="container wrap">
    <div class="sign">
      <a class="brand" href="/">{STUDIO_NAME}</a>
      <p>An indie studio making whimsical games with a dark streak.</p>
    </div>
    <nav aria-label="Footer">
      <div>
        <h2>Explore</h2>
        <a href="/">Home</a>
        {#each games as game (game.href)}
          <a href={game.href}>{game.title}</a>
        {/each}
        <a href="/about">About</a>
        <a href="/devlog">Dev blog</a>
        <a href="/merch">Merch</a>
      </div>
      <div>
        <h2>Follow</h2>
        <a href={LINKS.instagram}>Instagram</a>
        <a href={LINKS.tiktok}>TikTok</a>
        <a href={LINKS.presskit}>Press kit</a>
      </div>
    </nav>
  </div>
  <div class="container wrap legal">
    <span>© {year} {STUDIO_NAME}</span>
    <span>Powered by <a class="host" href={LINKS.hosting} target="_blank" rel="noopener">Crunchy.Host<svg viewBox="0 0 64 64" aria-hidden="true"><defs><linearGradient id="crunchy-logo" x1="16" y1="4" x2="46" y2="60" gradientUnits="userSpaceOnUse"><stop stop-color="#FFE08A" /><stop offset="0.5" stop-color="#F5AF19" /><stop offset="1" stop-color="#F06B50" /></linearGradient></defs><path fill="url(#crunchy-logo)" d="M59 7L38 24L24 22L17 33L26 44L39 40L57 48L36 60L13 50L3 29L18 9L35 4L29 14Z" /></svg></a></span>
  </div>
</footer>

<style>
  /* The footer drops into deeper dark along a ragged, torn edge */
  .site-footer {
    background: var(--night-deep);
    padding: clamp(64px, 8vw, 104px) 0 32px;
    mask:
      var(--torn-top) left top / 240px 14px repeat-x,
      linear-gradient(#000, #000) left 14px / 100% calc(100% - 14px) no-repeat;
  }
  .wrap {
    display: flex;
    justify-content: space-between;
    gap: 48px;
    flex-wrap: wrap;
  }
  .brand { font-family: var(--font-display); font-weight: 800; font-size: 2.4rem; line-height: 1; }
  .sign p { max-width: 34ch; margin: 16px 0 0; color: var(--ink-soft); }
  nav { display: flex; gap: clamp(40px, 8vw, 120px); }
  nav div { display: flex; flex-direction: column; gap: 10px; }
  h2 { margin: 0 0 6px; font-size: 1.5rem; font-weight: 700; color: var(--wisp); }
  nav a { color: var(--ink-soft); }
  nav a:hover, .legal a:hover { color: var(--ink); }
  .legal {
    margin-top: clamp(40px, 6vw, 72px);
    padding-top: 24px;
    position: relative;
    font-size: 0.9rem;
    color: var(--ink-soft);
    gap: 12px 32px;
  }
  .host { display: inline-flex; align-items: center; gap: 6px; }
  .host svg { width: 1.1em; height: 1.1em; }
  .legal::before {
    content: '';
    position: absolute;
    top: -2px;
    left: var(--gutter);
    right: var(--gutter);
    height: 5px;
    background: var(--night-line);
    mask: var(--brush) center / 100% 100% no-repeat;
  }
</style>
