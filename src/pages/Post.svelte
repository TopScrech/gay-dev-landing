<script lang="ts">
  import Asset from '../components/Asset.svelte'
  import { formatDate, posts } from '../lib/posts'

  let { slug }: { slug: string } = $props()

  const index = $derived(posts.findIndex((p) => p.slug === slug))
  const post = $derived(posts[index])
  const newer = $derived(posts[index - 1])
  const older = $derived(posts[index + 1])
</script>

<article class="post">
  <header class="container narrow">
    <a class="back" href="/devlog"><span aria-hidden="true">←</span> All posts</a>
    <p class="meta"><time datetime={post.date}>{formatDate(post.date)}</time></p>
    <h1>{post.title}</h1>
    <ul class="tags" aria-label="Tags">
      {#each post.tags as tag (tag)}<li>{tag}</li>{/each}
    </ul>
  </header>

  <div class="container cover">
    <Asset src="/images/blog/{post.slug}.jpg" alt="" ratio="21 / 9" eager />
  </div>

  <div class="container narrow prose">
    {#each post.body as block, i (i)}
      {#if block.startsWith('## ')}
        <h2>{block.slice(3)}</h2>
      {:else}
        <p>{block}</p>
      {/if}
    {/each}
  </div>

  <nav class="container narrow pager" aria-label="More posts">
    {#if older}
      <a href="/devlog/{older.slug}"><span class="dir">Older</span><span class="t">{older.title}</span></a>
    {:else}<span></span>{/if}
    {#if newer}
      <a class="next" href="/devlog/{newer.slug}"><span class="dir">Newer</span><span class="t">{newer.title}</span></a>
    {/if}
  </nav>
</article>

<style>
  .post { padding: calc(var(--header-h) + clamp(32px, 6vw, 72px)) 0 clamp(96px, 12vw, 160px); }
  .narrow { max-width: calc(46rem + 2 * var(--gutter)); }
  .back { display: inline-flex; gap: 8px; color: var(--ink-soft); font-weight: 600; font-size: 0.95rem; }
  .back:hover { color: var(--wisp); }
  .meta { margin: 32px 0 12px; color: var(--ink-soft); font-size: 0.95rem; }
  h1 { font-size: clamp(2.6rem, 7vw, 4.75rem); }
  .tags { display: flex; flex-wrap: wrap; gap: 8px; margin: 24px 0 0; padding: 0; list-style: none; }
  .tags li { padding: 4px 12px; border: 1px solid var(--night-line); border-radius: 999px; font-size: 0.85rem; color: var(--ink-soft); }
  .cover { margin-block: clamp(32px, 5vw, 56px); }
  .prose { font-size: 1.125rem; line-height: 1.75; }
  .prose p { margin: 0 0 1.4em; color: oklch(0.88 0.02 300); }
  .prose h2 { margin: 1.8em 0 0.6em; font-size: clamp(1.7rem, 3vw, 2.2rem); }
  .pager {
    display: flex;
    justify-content: space-between;
    gap: 24px;
    margin-top: clamp(48px, 7vw, 80px);
    padding-top: 28px;
    background: linear-gradient(var(--night-line), var(--night-line)) top center / calc(100% - 2 * var(--gutter)) 1px no-repeat;
  }
  .pager a { display: grid; gap: 4px; max-width: 48%; }
  .pager .next { text-align: right; }
  .dir { font-size: 0.85rem; font-weight: 700; color: var(--wisp); }
  .t { font-family: var(--font-display); font-size: 1.35rem; line-height: 1.15; }
  .pager a:hover .t { text-decoration: underline; text-underline-offset: 4px; text-decoration-thickness: 1px; }
  @media (max-width: 640px) {
    .cover :global(.asset) { aspect-ratio: 3 / 2 !important; }
  }
</style>
