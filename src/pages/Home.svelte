<!-- Studio home: the night-scene hero, then the game, who we are, the latest devlog and merch -->
<script lang="ts">
  import Asset from '../components/Asset.svelte'
  import FeaturedGame from '../components/FeaturedGame.svelte'
  import HomeHero from '../components/HomeHero.svelte'
  import MerchSection from '../components/MerchSection.svelte'
  import { STUDIO_NAME, teams } from '../lib/site'
  import { formatDate, posts } from '../lib/posts'

  const latest = posts.slice(0, 2)
  const teamNames = teams.map((t) => t.name.toLowerCase())
  const teamList = `${teamNames.slice(0, -1).join(', ')} and ${teamNames.at(-1)}`
</script>

<HomeHero />

<FeaturedGame />

<section class="story container" aria-labelledby="story-title">
  <h2 id="story-title">Who are we?</h2>
  <div class="story-text">
    <p class="story-lede">
      We are {STUDIO_NAME}: a student studio founded in 2026 at Hanze University of Applied Sciences, where we study Creative Media and
      Game Technologies.
    </p>
    <p>
      Our favourite moment in any game is the one where the plan falls apart and you have to improvise. So we are building a whole game
      out of that moment: tools that do two jobs, monsters with daily routines, and a marsh that punishes anyone who stops paying attention
    </p>
    <p>
      {teams.length} small teams - {teamList} - share one lodge and one stubborn idea. We went from a sketch on paper to a first playable
      prototype in two weeks, and we write it all down in a devlog every other week, gnome included
    </p>
  </div>
  <a class="text-link" href="/about">Meet the teams</a>
</section>

{#if latest.length}
  <section class="devlog container" aria-labelledby="devlog-title">
    <div class="devlog-head">
      <h2 id="devlog-title">Fresh from the devlog</h2>
      <a class="text-link" href="/devlog">All devlog posts</a>
    </div>
    <div class="posts" class:single={latest.length === 1}>
      {#each latest as post (post.slug)}
        <article class="post">
          <a class="post-cover" href="/devlog/{post.slug}" tabindex="-1" aria-hidden="true">
            <Asset src={post.cover} alt="" ratio="4 / 3" />
          </a>
          <div class="post-text">
            <p class="post-meta"><time datetime={post.date}>{formatDate(post.date)}</time></p>
            <h3><span class="post-number">#{post.number}</span> <a href="/devlog/{post.slug}">{post.title}</a></h3>
            <p class="post-excerpt">{post.excerpt}</p>
            <a class="text-link" href="/devlog/{post.slug}">Read the post<span class="visually-hidden">: {post.title}</span></a>
          </div>
        </article>
      {/each}
    </div>
  </section>
{/if}

<MerchSection />

<style>
  h2 { font-size: clamp(2.4rem, 5.5vw, 4rem); }
  p { margin: 0; }

  /* ── The studio ────────────────────────────────────────── */
  /* Heading, then the story across the page */
  .story {
    position: relative;
    display: grid;
    justify-items: start;
    gap: clamp(28px, 4vw, 48px);
    padding-block: clamp(64px, 9vw, 120px);
  }
  .story::before, .devlog::before {
    content: '';
    position: absolute;
    top: 0;
    left: var(--gutter);
    right: var(--gutter);
    height: 5px;
    background: var(--night-line);
    mask: var(--brush) center / 100% 100% no-repeat;
  }
  .story-text { display: grid; gap: 1em; max-width: 92ch; color: var(--ink-soft); font-size: 1.075rem; }
  .story-lede {
    font-family: var(--font-display);
    font-size: clamp(1.5rem, 2.6vw, 2rem);
    line-height: 1.15;
    color: var(--ink);
  }

  /* ── The devlog ────────────────────────────────────────── */
  .devlog { position: relative; padding-block: clamp(64px, 9vw, 120px) clamp(96px, 12vw, 160px); }
  .devlog-head {
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    justify-content: space-between;
    gap: 12px 32px;
    margin-bottom: clamp(32px, 5vw, 56px);
  }
  .posts { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: clamp(40px, 5vw, 72px); }
  .post { display: grid; gap: 22px; align-content: start; }
  .posts.single { grid-template-columns: 1fr; }
  .single .post { grid-template-columns: 1.2fr 1fr; align-items: center; gap: clamp(28px, 5vw, 72px); }
  .post-cover { display: block; rotate: 0.6deg; }
  .post-text { display: grid; justify-items: start; gap: 12px; }
  .post-meta { color: var(--ember); font-size: 0.95rem; font-weight: 700; }
  .post h3 { font-size: clamp(1.9rem, 3.4vw, 2.75rem); }
  .post h3 a:hover { color: var(--wisp); }
  .post-number { color: var(--ink-soft); font-weight: 500; }
  .post-excerpt { max-width: 46ch; color: var(--ink-soft); font-size: 1.075rem; }
  .post-text .text-link { margin-top: 6px; }

  @media (max-width: 860px) {
    .posts, .single .post { grid-template-columns: 1fr; }
  }
</style>
