<script lang="ts">
  import PageHero from '../components/PageHero.svelte'
</script>

<PageHero title="Lost in the marsh" palette="ember" seed={31}>
  <p>This page wandered off, or never existed. Either way, it’s getting dark.</p>
  <p class="back"><a class="btn btn-wisp" href="/">Head back to the lodge</a></p>
</PageHero>

<style>
  .back { margin-top: 24px !important; }
</style>
