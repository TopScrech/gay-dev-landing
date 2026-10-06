<script lang="ts">
  import Asset from '../components/Asset.svelte'
  import { formatDate, inline, posts } from '../lib/posts'

  let { slug }: { slug: string } = $props()

  const index = $derived(posts.findIndex((p) => p.slug === slug))
  const post = $derived(posts[index])
  const newer = $derived(posts[index - 1])
  const older = $derived(posts[index + 1])

  // '816 / 567' → 1.44, so paired images share one height
  const aspect = (ratio: string) => ratio.split('/').map(Number).reduce((w, h) => w / h)
</script>

<article class="post">
  <header class="container narrow">
    <a class="back" href="/devlog"><span aria-hidden="true">←</span> All posts</a>
    <p class="meta"><time datetime={post.date}>{formatDate(post.date)}</time></p>
    <h1>{post.title}</h1>
    {#if post.tags?.length}
      <ul class="tags" aria-label="Tags">
        {#each post.tags as tag (tag)}<li>{tag}</li>{/each}
      </ul>
    {/if}
  </header>

  <div class="container narrow prose">
    {#each post.body as block, i (i)}
      {#if typeof block !== 'string'}
        <figure class:pair={block.images.length > 1}>
          <div class="images">
            {#each block.images as image (image.src)}
              <div class="cell" style:flex-grow={block.images.length > 1 ? aspect(image.ratio) : undefined}><Asset src={image.src} alt={image.alt} ratio={image.ratio} /></div>
            {/each}
          </div>
          {#if block.caption}<figcaption>{block.caption}</figcaption>{/if}
        </figure>
      {:else if block.startsWith('## ')}
        <h2>{block.slice(3)}</h2>
      {:else}
        <p>
          {#each inline(block) as part, j (j)}
            {#if part.href}
              <a href={part.href} target={part.href.startsWith('http') ? '_blank' : undefined} rel={part.href.startsWith('http') ? 'noopener' : undefined}>{part.text}</a>
            {:else}{part.text}{/if}
          {/each}
        </p>
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
  .tags li { padding: 4px 12px; background: var(--night-raise); clip-path: var(--chip-c); font-size: 0.9rem; color: var(--ink-soft); }
  .prose { margin-top: clamp(40px, 6vw, 64px); font-size: 1.125rem; line-height: 1.75; }
  .prose p { margin: 0 0 1.4em; color: oklch(0.88 0.025 295); }
  .prose a { color: var(--wisp); text-decoration: underline; text-underline-offset: 4px; text-decoration-thickness: 1px; }
  figure { margin: 2.2em 0; }
  .images { display: flex; justify-content: center; align-items: center; gap: 16px; }
  figure:not(.pair) .cell { width: min(100%, 30rem); }
  .pair .cell { flex-basis: 0; min-width: 0; }
  figcaption { margin-top: 12px; text-align: center; color: var(--ink-soft); font-size: 0.95rem; }
  .prose h2 { margin: 1.8em 0 0.6em; font-size: clamp(1.7rem, 3vw, 2.2rem); }
  .pager {
    display: flex;
    justify-content: space-between;
    gap: 24px;
    margin-top: clamp(48px, 7vw, 80px);
    padding-top: 28px;
    position: relative;
  }
  .pager::before {
    content: '';
    position: absolute;
    top: 0;
    left: var(--gutter);
    right: var(--gutter);
    height: 5px;
    background: var(--night-line);
    mask: var(--brush) center / 100% 100% no-repeat;
  }
  .pager a { display: grid; gap: 4px; max-width: 48%; }
  .pager .next { text-align: right; }
  .dir { font-size: 0.85rem; font-weight: 700; color: var(--wisp); }
  .t { font-family: var(--font-display); font-size: 1.35rem; line-height: 1.15; }
  .pager a:hover .t { text-decoration: underline; text-underline-offset: 4px; text-decoration-thickness: 1px; }
  @media (max-width: 640px) {
    .pair .images { flex-direction: column; }
    .pair .cell { flex: none; width: 100%; }
  }
</style>
