<script lang="ts">
  import Asset from './Asset.svelte'
  import { STUDIO_NAME } from '../lib/site'
</script>

<section class="merch container" aria-labelledby="merch-title">
  <div class="merch-art">
    <Asset cutout src="/images/merch.png" alt="Graphic shirts, a black cap, an embroidered patch and a diner mug" ratio="1" />
  </div>
  <div class="merch-copy">
    <h2 id="merch-title" class="section-title">Official {STUDIO_NAME} merch</h2>
    <p>Lodge-issue shirts, mugs and pins for anyone who has signed a contract with the marsh. See the full range in our store.</p>
    <a class="btn btn-ghost merch-btn" href="/merch">Visit the store</a>
  </div>
</section>

<style>
  .merch {
    display: grid;
    grid-template-columns: 1.1fr 1fr;
    align-items: center;
    gap: clamp(40px, 6vw, 96px);
    padding-block: clamp(80px, 11vw, 150px) clamp(96px, 12vw, 160px);
  }
  .merch-art { width: min(100%, 560px); justify-self: center; }
  .merch-copy { display: grid; justify-items: start; gap: 20px; }
  .merch-copy p { max-width: 40ch; margin: 0; color: var(--ink-soft); font-size: 1.1rem; }
  .merch-btn {
    --oak: oklch(0.38 0.09 295);
    --oak-edge: oklch(0.2 0.05 288);
    min-height: 64px;
    margin-top: 8px;
    padding-inline: 36px;
  }

  @media (max-width: 860px) {
    .merch { grid-template-columns: 1fr; }
  }
</style>
