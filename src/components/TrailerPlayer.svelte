<script lang="ts">
  // The trailer frame: a poster with a wax-seal play button, swapped for the embed only when pressed.
  // With no TRAILER_URL in site.ts the seal is disabled and reads "Trailer coming soon"
  import Asset from './Asset.svelte'
  import { GAME_TITLE, TRAILER_URL } from '../lib/site'

  let playing = $state(false)
</script>

<div class="frame">
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
</div>

<style>
  /* The shadow sits on the wrapper so the chipped clip on the player doesn't cut it off */
  .frame { filter: drop-shadow(0 30px 40px oklch(0.08 0.03 280 / 0.8)); }
  .player { position: relative; overflow: hidden; clip-path: var(--chip-b); }
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
    background: oklch(from var(--night-deep) l c h / 0.25);
    color: var(--ink);
    font: 700 1rem var(--font-body);
    text-shadow: 0 1px 12px oklch(from var(--night-deep) l c h / 0.9);
    cursor: pointer;
    transition: background-color 0.3s;
  }
  .play:focus-visible { outline-offset: -8px; }
  .play:disabled { cursor: default; }
  .play:not(:disabled):hover { background: oklch(from var(--night-deep) l c h / 0.1); }
  /* A wax seal, pressed a little off-centre, with the play mark stamped into it */
  .play-icon {
    display: grid;
    place-items: center;
    width: clamp(68px, 9vw, 104px);
    aspect-ratio: 1;
    border-radius: 47% 53% 50% 50% / 52% 46% 54% 48%;
    background:
      radial-gradient(circle at 36% 30%, oklch(1 0 0 / 0.22), transparent 40%),
      var(--wax);
    box-shadow:
      inset 0 0 0 clamp(6px, 0.9vw, 9px) oklch(0.44 0.15 28),
      inset 0 0 0 clamp(7px, 1vw, 10px) oklch(0.36 0.12 28),
      0 6px 18px oklch(0.08 0.03 30 / 0.6);
    rotate: -8deg;
    transition: transform 0.4s var(--ease-out);
  }
  .play-icon::after {
    content: '';
    margin-left: 12%;
    border-style: solid;
    border-width: 14px 0 14px 24px;
    border-color: transparent transparent transparent oklch(0.3 0.1 28);
    filter: drop-shadow(0 1px 0 oklch(0.62 0.15 30));
  }
  .play:not(:disabled):hover .play-icon { transform: scale(1.06) rotate(6deg); }
  .play:disabled .play-icon { opacity: 0.8; }

  @media (prefers-reduced-motion: reduce) {
    .play, .play-icon { transition: none; }
    .play:not(:disabled):hover .play-icon { transform: none; }
  }
</style>
