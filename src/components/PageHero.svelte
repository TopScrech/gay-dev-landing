<script lang="ts">
  import type { Snippet } from 'svelte'
  import type { PaletteName } from '../lib/landscape'
  import Scene from './Scene.svelte'

  type Props = { title: string; palette?: PaletteName; seed?: number; children?: Snippet }
  let { title, palette = 'dusk', seed = 8, children }: Props = $props()
</script>

<section class="page-hero">
  <Scene {palette} {seed} tall={false} parallax />
  <div class="container inner">
    <h1>{title}</h1>
    {#if children}<div class="intro">{@render children()}</div>{/if}
  </div>
</section>

<style>
  .page-hero {
    position: relative;
    display: flex;
    align-items: flex-end;
    min-height: clamp(420px, 62vh, 620px);
    padding: calc(var(--header-h) + 48px) 0 clamp(48px, 7vw, 88px);
    isolation: isolate;
  }
  .page-hero :global(.scene) { z-index: -1; }
  .page-hero::after {
    content: '';
    position: absolute;
    inset: 40% 0 0;
    z-index: -1;
    background: linear-gradient(to bottom, transparent, var(--night));
    pointer-events: none;
  }
  h1 {
    font-size: clamp(3.25rem, 9vw, 6rem);
    text-shadow: 0 2px 30px oklch(0.12 0.03 305 / 0.6);
  }
  .intro {
    max-width: 52ch;
    margin-top: 16px;
    font-size: clamp(1.05rem, 1.6vw, 1.25rem);
    color: var(--ink);
    text-shadow: 0 1px 16px oklch(0.12 0.03 305 / 0.9);
  }
  .intro :global(p) { margin: 0; }
</style>
