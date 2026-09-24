<script lang="ts">
  import SiteFooter from './components/SiteFooter.svelte'
  import SiteHeader from './components/SiteHeader.svelte'
  import { interceptLinks, location_, resolve } from './lib/router.svelte'
  import { posts } from './lib/posts'
  import { GAME_TITLE } from './lib/site'
  import About from './pages/About.svelte'
  import Devlog from './pages/Devlog.svelte'
  import Home from './pages/Home.svelte'
  import Missing from './pages/Missing.svelte'
  import Post from './pages/Post.svelte'

  const route = $derived(resolve(location_.path))

  $effect(() => {
    const titles = { home: '', about: 'About', devlog: 'Dev blog', missing: 'Lost in the marsh' }
    const part = route.page === 'post' ? posts.find((p) => p.slug === route.slug)?.title : titles[route.page]
    document.title = part ? `${part} · ${GAME_TITLE}` : GAME_TITLE
  })
</script>

<svelte:document onclick={interceptLinks} />

<a class="skip-link" href="#main">Skip to content</a>
<SiteHeader />

<main id="main" tabindex="-1">
  {#key location_.path}
    <div class="route">
      {#if route.page === 'home'}
        <Home />
      {:else if route.page === 'about'}
        <About />
      {:else if route.page === 'devlog'}
        <Devlog />
      {:else if route.page === 'post'}
        <Post slug={route.slug} />
      {:else}
        <Missing />
      {/if}
    </div>
  {/key}
</main>

<SiteFooter />
