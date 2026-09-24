<script lang="ts">
  import { GAME_TITLE, LINKS, STUDIO_NAME } from '../lib/site'
  const year = new Date().getFullYear()
</script>

<footer class="site-footer">
  <div class="container wrap">
    <div class="sign">
      <a class="brand" href="/">{GAME_TITLE}</a>
      <p>In development for PC. Title, art, and everything else subject to change by the marsh.</p>
    </div>
    <nav aria-label="Footer">
      <div>
        <h2>Explore</h2>
        <a href="/">Home</a>
        <a href="/about">About</a>
        <a href="/devlog">Dev blog</a>
        <a href="/merch">Merch</a>
      </div>
      <div>
        <h2>Follow</h2>
        <a href={LINKS.discord}>Discord</a>
        <a href={LINKS.instagram}>Instagram</a>
        <a href={LINKS.presskit}>Press kit</a>
      </div>
    </nav>
  </div>
  <div class="container wrap legal">
    <span>© {year} {STUDIO_NAME}</span>
    <span>No monsters were harmed. Several were inconvenienced</span>
  </div>
</footer>

<style>
  /* The footer drops into deeper dark along a ragged, torn edge */
  .site-footer {
    background: oklch(0.12 0.03 160);
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
  nav a:hover { color: var(--ink); }
  .legal {
    margin-top: clamp(40px, 6vw, 72px);
    padding-top: 24px;
    position: relative;
    font-size: 0.9rem;
    color: var(--ink-soft);
    gap: 12px 32px;
  }
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
