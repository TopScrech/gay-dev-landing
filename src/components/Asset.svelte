<script lang="ts">
  // An image slot: shows `src` once the file exists in public/, a blank block until then.
  // In dev, blank slots are tagged with the path the real asset should live at
  // `cutout` is for transparent PNGs: no panel behind the image once it loads
  type Props = { src: string; alt: string; ratio?: string; eager?: boolean; cover?: boolean; cutout?: boolean; class?: string }
  let { src, alt, ratio, eager = false, cover = false, cutout = false, class: className = '' }: Props = $props()

  let failed = $state(false)
  const dev = import.meta.env.DEV
</script>

<div class="asset {className}" class:cover class:cutout={cutout && !failed} class:blank={failed} style:aspect-ratio={ratio}>
  {#if !failed}
    <img {src} {alt} loading={eager || cover ? 'eager' : 'lazy'} decoding="async" onerror={() => (failed = true)} />
  {:else if dev}
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
  .asset:not(.cover)::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: inherit;
    box-shadow: inset 0 0 0 1px oklch(0.95 0.02 150 / 0.09);
    pointer-events: none;
  }
  .cutout { background: none; }
  .cutout::after { display: none; }
  .cutout img { object-fit: contain; }
  .cover {
    position: absolute;
    inset: 0;
    border-radius: 0;
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
    background: oklch(0.12 0.03 160 / 0.8);
    color: var(--ink-soft);
    font: 500 11px/1.3 ui-monospace, monospace;
    pointer-events: none;
  }
  .cover .asset-tag { left: auto; right: 16px; bottom: 16px; }
</style>
