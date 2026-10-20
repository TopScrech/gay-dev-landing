<script lang="ts">
  // The game on the studio home: title and one line on the left, the way in stacked on the right, the trailer below
  import TrailerPlayer from './TrailerPlayer.svelte'
  import WishlistButton from './WishlistButton.svelte'
  import { GAME_TITLE, TAGLINE, games } from '../lib/site'

  const game = games[0]
</script>

<section id="trailer" class="trailer container" aria-labelledby="trailer-title">
  <div class="trailer-head">
    <div class="trailer-copy">
      <h2 id="trailer-title">{GAME_TITLE}</h2>
      <p class="tagline">{TAGLINE}</p>
    </div>
    <div class="head-actions">
      <WishlistButton />
      <a class="text-link" href={game.href}>Learn more</a>
    </div>
  </div>
  <TrailerPlayer />
</section>

<style>
  .trailer { padding-block: clamp(56px, 8vw, 110px) clamp(48px, 7vw, 96px); }
  /* Centred against the text block, and dropped underneath it once there's no room beside it */
  .trailer-head {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 24px 40px;
    margin-bottom: clamp(24px, 3.5vw, 40px);
  }
  .trailer-copy { display: grid; gap: 16px; }
  h2 { font-size: clamp(2.3rem, 5.5vw, 3.75rem); }
  .tagline { max-width: 44ch; margin: 0; color: var(--ink-soft); font-size: 1.075rem; }
  .head-actions { display: flex; flex-direction: column; align-items: center; gap: 18px; }

  @media (max-width: 860px) {
    .head-actions { width: 100%; }
  }
</style>
