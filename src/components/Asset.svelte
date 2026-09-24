<script lang="ts">
  // An image slot: tries `src` (drop the real file into public/), falls back to placeholder art.
  // In dev, fallbacks are tagged with the path the real asset should live at
  type Props = { src: string; fallback: string; alt: string; ratio?: string; eager?: boolean; class?: string }
  let { src, fallback, alt, ratio, eager = false, class: className = '' }: Props = $props()

  let failed = $state(false)
  const dev = import.meta.env.DEV
</script>

<div class="asset {className}" class:is-fallback={failed} style:aspect-ratio={ratio}>
  <img
    src={failed ? fallback : src}
    {alt}
    loading={eager ? 'eager' : 'lazy'}
    decoding="async"
    onerror={() => (failed = true)}
  />
  {#if failed && dev}
    <span class="asset-tag" aria-hidden="true">public{src}</span>
  {/if}
</div>

<style>
  .asset {
    position: relative;
    overflow: hidden;
    background: var(--night-raise);
    border-radius: var(--radius);
  }
  .asset::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: inherit;
    box-shadow: inset 0 0 0 1px oklch(0.95 0.02 300 / 0.09);
    pointer-events: none;
  }
  img {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  .asset-tag {
    position: absolute;
    left: 10px;
    bottom: 10px;
    padding: 4px 8px;
    border-radius: 3px;
    background: oklch(0.12 0.03 305 / 0.8);
    color: var(--ink-soft);
    font: 500 11px/1.3 ui-monospace, monospace;
    pointer-events: none;
  }
</style>
