<script lang="ts">
  export let caption = 'Environment artwork · placeholder'
  export let variant = ''
</script>
<figure class:detail={variant === 'detail'}>
  <img src="/images/forest.svg" alt="Illustrated evergreen forest, distant mountains and a winding river" loading="lazy" />
  <figcaption>{caption}</figcaption>
</figure>
<style>
  figure { margin: 0; position: relative; overflow: hidden; background: #29443d; aspect-ratio: 16 / 10 }
  img { width: 100%; height: 100%; object-fit: cover; display: block }
  .detail img { transform: scale(1.5); transform-origin: right bottom; filter: hue-rotate(20deg) brightness(.8) }
  figcaption { position: absolute; bottom: 16px; left: 18px; color: #f3ead2; font-size: 10px; letter-spacing: .1em; text-transform: uppercase; background: #112d29d9; padding: 7px 10px }
</style>
