<script lang="ts">
  import Asset from '../components/Asset.svelte'
  import PageHero from '../components/PageHero.svelte'
  import { formatDate, posts } from '../lib/posts'

  const [featured, ...rest] = posts
</script>

<PageHero title="Dev blog" image="/images/blog/hero.jpg">
  <p>Notes from the lodge: what we’re building, what broke, and which monsters survived the latest round of cuts.</p>
</PageHero>

<section class="devlog container" aria-label="Posts">
  <article class="featured">
    <a class="cover-link" href="/devlog/{featured.slug}" tabindex="-1" aria-hidden="true">
      <Asset src="/images/blog/{featured.slug}.jpg" alt="" ratio="3 / 2" eager />
    </a>
    <div>
      <p class="meta">Devlog #{featured.number} · <time datetime={featured.date}>{formatDate(featured.date)}</time></p>
      <h2><a href="/devlog/{featured.slug}">{featured.title}</a></h2>
      <p class="excerpt">{featured.excerpt}</p>
      <a class="text-link" href="/devlog/{featured.slug}">Read the post<span class="visually-hidden">: {featured.title}</span></a>
    </div>
  </article>

  <ol class="list">
    {#each rest as post (post.slug)}
      <li>
        <a href="/devlog/{post.slug}">
          <Asset src="/images/blog/{post.slug}.jpg" alt="" ratio="3 / 2" />
          <span class="body">
            <span class="meta">Devlog #{post.number} · <time datetime={post.date}>{formatDate(post.date)}</time></span>
            <span class="title">{post.title}</span>
            <span class="excerpt">{post.excerpt}</span>
          </span>
        </a>
      </li>
    {/each}
  </ol>
</section>

<style>
  .devlog { padding-block: clamp(40px, 6vw, 80px) clamp(96px, 12vw, 160px); }
  .featured {
    display: grid;
    grid-template-columns: 1.3fr 1fr;
    gap: clamp(24px, 5vw, 72px);
    align-items: center;
  }
  .featured h2 { font-size: clamp(2.2rem, 4.6vw, 3.5rem); margin-top: 12px; }
  .featured h2 a:hover { color: var(--wisp); }
  .meta { margin: 0; color: var(--ink-soft); font-size: 0.9rem; }
  .excerpt { color: var(--ink-soft); font-size: 1.075rem; max-width: 46ch; }
  .featured .excerpt { margin: 16px 0 24px; }
  .cover-link :global(.asset) { transition: transform 0.6s var(--ease-out); }
  .cover-link:hover :global(.asset) { transform: scale(1.01); }

  .list { list-style: none; margin: clamp(56px, 8vw, 104px) 0 0; padding: 0; border-top: 1px solid var(--night-line); }
  .list li { border-bottom: 1px solid var(--night-line); }
  .list a {
    display: grid;
    grid-template-columns: minmax(140px, 240px) 1fr;
    gap: clamp(16px, 3vw, 40px);
    align-items: center;
    padding: clamp(20px, 3vw, 32px) 0;
  }
  .body { display: grid; gap: 6px; }
  .title { font-family: var(--font-display); font-size: clamp(1.6rem, 2.6vw, 2.1rem); line-height: 1.1; }
  .list .excerpt { font-size: 1rem; }
  .list a:hover .title { color: var(--wisp); }

  @media (max-width: 760px) {
    .featured { grid-template-columns: 1fr; }
    .list a { grid-template-columns: 1fr; }
  }
  @media (prefers-reduced-motion: reduce) {
    .cover-link :global(.asset) { transition: none; }
  }
</style>
