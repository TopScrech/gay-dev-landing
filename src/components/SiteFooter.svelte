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
      </div>
      <div>
        <h2>Follow</h2>
        <a href={LINKS.discord}>Discord</a>
        <a href={LINKS.bluesky}>Bluesky</a>
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
  .site-footer {
    border-top: 1px solid var(--night-line);
    background: oklch(0.135 0.03 305);
    padding: clamp(48px, 7vw, 88px) 0 32px;
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
  h2 { margin: 0 0 6px; font-size: 0.95rem; font-weight: 700; color: var(--wisp); }
  nav a { color: var(--ink-soft); }
  nav a:hover { color: var(--ink); text-decoration: underline; text-underline-offset: 4px; }
  .legal {
    margin-top: clamp(40px, 6vw, 72px);
    padding-top: 24px;
    background: linear-gradient(var(--night-line), var(--night-line)) top center / calc(100% - 2 * var(--gutter)) 1px no-repeat;
    font-size: 0.875rem;
    color: var(--ink-soft);
    gap: 12px 32px;
  }
</style>
