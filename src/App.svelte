<script lang="ts">
  import { onMount } from 'svelte'
  import Artwork from './components/Artwork.svelte'
  import Footer from './components/Footer.svelte'
  let route = $state(window.location.hash.slice(1) || '/')
  const page = $derived(route.startsWith('/about') ? 'about' : route.startsWith('/blog') ? 'blog' : 'home')
  const posts = [
    { slug: 'a-world-worth-getting-lost-in', category: 'The world', title: 'A world worth getting lost in', excerpt: 'Finding the balance between a welcoming wilderness and the feeling that something is watching', body: 'Our starting point is a world that invites you to wander a little further — past the familiar path, toward the strange light between the trees. We want curiosity to be as important as courage. This space will become a closer look at the environments, sketches, and small discoveries that shape the adventure' },
    { slug: 'tools-of-the-trade', category: 'Gameplay', title: 'Not your usual tools of the trade', excerpt: 'A little magic, a little improvisation, and a very questionable plan', body: 'Inventive magical tools are at the heart of this adventure. We are exploring how a single tool can help you understand a creature, solve a puzzle, and turn a frantic encounter around. Future entries will share prototypes and the lessons we learn along the way' },
    { slug: 'the-first-step', category: 'Studio notes', title: 'Every strange adventure starts somewhere', excerpt: 'A small introduction to the game we’re making and the journey ahead', body: 'We are making a whimsical first-person monster-hunting adventure with a dark streak. This journal is a place for the work in progress: the experiments, the discoveries, and the things that surprise us. Thanks for being here at the beginning' },
  ]
  const post = $derived(posts.find(item => route === `/blog/${item.slug}`))
  onMount(() => {
    const navigate = () => { route = window.location.hash.slice(1) || '/'; window.scrollTo(0, 0) }
    window.addEventListener('hashchange', navigate)
    return () => window.removeEventListener('hashchange', navigate)
  })
</script>

<svelte:head>
  <title>{post ? post.title : page === 'about' ? 'About the game' : page === 'blog' ? 'Dev blog' : 'Into the unfamiliar'} — Untitled adventure</title>
  <meta name="description" content="A whimsical first-person monster-hunting adventure with a dark streak — currently in development" />
</svelte:head>

<a class="skip-link" href="#main" onclick={(event) => { event.preventDefault(); document.getElementById('main')?.focus() }}>Skip to content</a>
<header>
  <a class="brand" href="#/" aria-label="Untitled adventure home"><span class="brand-symbol" aria-hidden="true">✳</span><span>UNTITLED<br /><small>AN ADVENTURE IN THE MAKING</small></span></a>
  <nav aria-label="Main navigation">
    <a href="#/" aria-current={page === 'home' ? 'page' : undefined}>Home</a>
    <a href="#/about" aria-current={page === 'about' ? 'page' : undefined}>About</a>
    <a href="#/blog" aria-current={page === 'blog' ? 'page' : undefined}>Dev blog</a>
  </nav>
  <span class="development"><i></i> In development</span>
</header>
<main id="main" tabindex="-1">
  {#if page === 'home'}
    <section class="hero">
      <img class="hero-art" src="/images/forest.svg" alt="Layers of misty mountains and pine forests surrounding a winding river" />
      <div class="hero-shade"></div>
      <div class="hero-copy"><p class="eyebrow">A little wonder · A little wicked</p><h1>Into the<br /><em>unfamiliar</em></h1><p>Curious creatures, peculiar magic<br />and a wilderness with something to hide</p><a class="button" href="#/about">Discover the game <span>↗</span></a></div>
      <div class="hero-bottom"><span>FIRST-PERSON ADVENTURE · WORK IN PROGRESS</span><a href="#discover" onclick={(event) => { event.preventDefault(); document.getElementById('discover')?.scrollIntoView({ behavior: 'smooth' }) }}>Venture further ↓</a><span>CONCEPT LANDSCAPE / PLACEHOLDER</span></div>
    </section>
    <section id="discover" class="intro content"><span class="ornament" aria-hidden="true">✳</span><p class="eyebrow">Welcome to the wilds</p><h2>Something strange<br />is out there</h2><p class="lead">Step into a whimsical world with a dark streak<br class="desktop" /> Hunt peculiar monsters, wield inventive magical tools, and<br class="desktop" /> think on your feet when the wilderness bites back</p><a class="text-link" href="#/about">A closer look at the adventure <span>↗</span></a></section>
    <section class="content glimpse"><div class="section-heading"><div><p class="eyebrow">Beyond the beaten path</p><h2>A world taking shape</h2></div><span class="aside">A little room for what’s to come</span></div><div class="art-grid"><Artwork caption="01 / The wilds · artwork to come" /><Artwork variant="detail" caption="02 / The unknown · gameplay to come" /></div></section>
    <section class="journal content"><div class="section-heading"><div><p class="eyebrow">Notes from behind the scenes</p><h2>The development journal</h2></div><a class="text-link" href="#/blog">All entries ↗</a></div><a class="journal-row" href={`#/blog/${posts[0].slug}`}><span class="eyebrow">Preview entry / 01</span><div><h3>{posts[0].title}</h3><p>{posts[0].excerpt}</p></div><span class="arrow">↗</span></a></section>
  {:else if page === 'about'}
    <section class="page-heading content"><p class="eyebrow">About the adventure</p><h1>A curious world<br /><em>with a dark streak</em></h1><p class="lead">A first-person monster-hunting adventure where a quick mind<br class="desktop" /> is just as useful as a little magic</p></section>
    <div class="content"><Artwork caption="The world of the game · key artwork placeholder" /></div>
    <section class="content about-copy"><div><p class="eyebrow">Wonder meets wilderness</p><h2>Stay curious<br />Stay on your toes</h2></div><div><p>Follow the strange sounds off the trail and discover a world that’s as playful as it is unsettling</p><p>Get to know its peculiar monsters, experiment with inventive magical tools, and piece together solutions in frantic puzzle combat</p><p class="muted">The adventure is still taking shape — the title, artwork, and more details will be revealed as development continues</p></div></section>
    <section class="team content"><div class="section-heading"><div><p class="eyebrow">The people behind the peculiar</p><h2>Meet the team</h2></div><span class="aside">Introductions coming soon</span></div><p class="team-note">Our full team will be listed here once the names and roles are ready</p><div class="team-grid">{#each [1, 2, 3, 4] as member}<article class="team-card"><img src="/images/portrait.svg" alt="Team portrait placeholder" loading="lazy" /><span class="eyebrow">Team member / 0{member}</span><h3>Name to come</h3><p>Role to come</p></article>{/each}</div></section>
  {:else if post}
    <article class="content article"><a class="text-link" href="#/blog">← Back to the journal</a><p class="eyebrow">{post.category} · Preview entry</p><h1>{post.title}</h1><p class="lead">{post.excerpt}</p><Artwork caption="Journal artwork · placeholder" /><p>{post.body}</p><aside class="preview-note">This is a sample journal entry — development updates are coming soon</aside></article>
  {:else}
    <section class="page-heading content"><p class="eyebrow">Field notes from development</p><h1>Making something<br /><em>a little strange</em></h1><p class="lead">Ideas, experiments, and dispatches from the wilds<br />A journal of the adventure taking shape</p></section>
    <section class="content blog-list" aria-label="Development journal entries">{#each posts as entry, index}<a class="blog-card" href={`#/blog/${entry.slug}`}><Artwork variant={index === 1 ? 'detail' : ''} caption={`Journal / 0${index + 1} · placeholder`} /><div><p class="eyebrow">{entry.category} · Preview entry</p><h2>{entry.title}</h2><p>{entry.excerpt}</p><span class="text-link">Read entry ↗</span></div></a>{/each}<p class="preview-note">Sample entries for now — real stories from development are coming soon</p></section>
  {/if}
</main>
<Footer />
