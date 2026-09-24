<script lang="ts">
  import Asset from '../components/Asset.svelte'
  import PageHero from '../components/PageHero.svelte'
  import { location_ } from '../lib/router.svelte'
  import { GAME_TITLE, STUDIO_NAME, TEAM_LAYOUT, team, type TeamLayout } from '../lib/site'

  const dev = import.meta.env.DEV
  const fromQuery = new URLSearchParams(location_.search).get('team')
  let layout = $state<TeamLayout>(fromQuery === 'cards' || fromQuery === 'photo' ? fromQuery : TEAM_LAYOUT)

  const facts = [
    ['Genre', 'First-person adventure with puzzle combat'],
    ['Platform', 'PC (Steam). Others once the marsh allows'],
    ['Players', 'Single-player'],
    ['Status', 'In development'],
    ['Release', 'When it’s ready, and not a full moon before'],
  ]
</script>

<PageHero title="About" image="/images/about/hero.jpg">
  <p>{GAME_TITLE} is a first-person monster hunt about a haunted marsh, a lodge full of strange inventions, and the person foolish enough to take the job.</p>
</PageHero>

<section class="story container" aria-labelledby="story-title">
  <div class="story-text">
    <h2 id="story-title">The job nobody else wanted</h2>
    <p>
      The marsh around {GAME_TITLE} has always had monsters. For a hundred years the lodge kept them in check: a keeper, a ledger, and
      a workshop full of tools built for problems no ordinary tool could solve.
    </p>
    <p>
      Then the last keeper vanished, the contracts piled up, and the creatures got comfortable. You arrive with a borrowed lantern and a
      key that doesn’t quite fit the door.
    </p>
    <p>
      Every hunt starts with watching. Every fight is a puzzle you solve with your hands, in first person, while something very large
      is working on the same puzzle from the other side.
    </p>
  </div>
  <Asset class="story-art" src="/images/about/world.jpg" alt="The marsh at dusk, seen from the lodge porch" ratio="4 / 5" />
</section>

<section class="facts container" aria-labelledby="facts-title">
  <h2 id="facts-title" class="visually-hidden">Fact sheet</h2>
  <dl>
    {#each facts as [term, value] (term)}
      <div>
        <dt>{term}</dt>
        <dd>{value}</dd>
      </div>
    {/each}
  </dl>
</section>

<section class="studio container" aria-labelledby="studio-title">
  <h2 id="studio-title">The studio</h2>
  <div class="studio-text">
    <p>
      We’re {STUDIO_NAME}, a small independent team who like games that are funny right up until they aren’t. We grew up on lantern-lit
      adventure games and wanted to make one where the tools are as strange as the monsters.
    </p>
    <p>We build in the open. The <a class="text-link" href="/devlog">dev blog</a> is where we share progress, dead ends, and the occasional creature that didn’t make the cut.</p>
  </div>
</section>

<section class="team container" aria-labelledby="team-title">
  <div class="team-head">
    <h2 id="team-title">The team</h2>
    {#if dev}
      <div class="layout-switch" role="group" aria-label="Team layout preview (dev only)">
        <button aria-pressed={layout === 'cards'} onclick={() => (layout = 'cards')}>Cards</button>
        <button aria-pressed={layout === 'photo'} onclick={() => (layout = 'photo')}>Group photo</button>
      </div>
    {/if}
  </div>

  {#if layout === 'cards'}
    <ul class="cards">
      {#each team as m (m.slug)}
        <li>
          <Asset src="/images/team/{m.slug}.jpg" alt="Portrait of {m.name}" ratio="4 / 5" />
          <h3>{m.name}</h3>
          <p class="role">{m.role}</p>
          <p class="bio">{m.bio}</p>
        </li>
      {/each}
    </ul>
  {:else}
    <Asset class="group" src="/images/team/group.jpg" alt="The {STUDIO_NAME} team" />
    <ul class="roster">
      {#each team as m (m.slug)}
        <li>
          <span class="name">{m.name}</span>
          <span class="role">{m.role}</span>
        </li>
      {/each}
    </ul>
  {/if}
</section>

<style>
  .story {
    display: grid;
    grid-template-columns: 1.1fr 1fr;
    gap: clamp(32px, 6vw, 96px);
    align-items: center;
    padding-block: clamp(56px, 8vw, 120px);
  }
  h2 { font-size: clamp(2.2rem, 5vw, 3.5rem); }
  .story-text p, .studio-text p { max-width: 58ch; color: var(--ink-soft); font-size: 1.075rem; }
  .story-text h2 { margin-bottom: 28px; }

  .facts dl {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    margin: 0;
    border-block: 1px solid var(--night-line);
  }
  .facts dl div { padding: 24px 24px 24px 0; }
  .facts dt { font-size: 0.9rem; font-weight: 700; color: var(--wisp); }
  .facts dd { margin: 6px 0 0; font-family: var(--font-display); font-size: 1.4rem; line-height: 1.2; }

  .studio {
    display: grid;
    grid-template-columns: 1fr 1.6fr;
    gap: 24px clamp(32px, 6vw, 96px);
    padding-block: clamp(72px, 10vw, 140px) clamp(48px, 6vw, 80px);
  }
  .studio-text p:first-child { margin-top: 0; }

  .team { padding-block: clamp(48px, 6vw, 80px) clamp(96px, 12vw, 160px); }
  .team-head { display: flex; justify-content: space-between; align-items: center; gap: 16px; flex-wrap: wrap; margin-bottom: clamp(28px, 4vw, 48px); }
  .layout-switch { display: inline-flex; padding: 3px; border: 1px dashed var(--night-line); border-radius: 999px; font-size: 0.85rem; }
  .layout-switch button {
    padding: 6px 14px;
    border: 0;
    border-radius: 999px;
    background: none;
    color: var(--ink-soft);
    font: inherit;
    font-weight: 600;
    cursor: pointer;
  }
  .layout-switch button[aria-pressed='true'] { background: var(--night-raise); color: var(--ink); }

  .cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: clamp(28px, 3vw, 40px) clamp(16px, 2vw, 28px);
    margin: 0;
    padding: 0;
    list-style: none;
  }
  .cards h3 { margin-top: 16px; font-size: 1.6rem; }
  .role { margin: 4px 0 0; color: var(--wisp); font-weight: 600; font-size: 0.95rem; }
  .bio { margin: 10px 0 0; color: var(--ink-soft); font-size: 0.95rem; line-height: 1.55; }
  .cards li :global(.asset) { transition: transform 0.5s var(--ease-out); }
  .cards li:hover :global(.asset) { transform: translateY(-4px) rotate(-0.6deg); }

  .team :global(.group) { aspect-ratio: 21 / 9; }
  .roster {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 20px 32px;
    margin: 28px 0 0;
    padding: 0;
    list-style: none;
  }
  .roster li { display: grid; gap: 2px; }
  .name { font-family: var(--font-display); font-size: 1.4rem; line-height: 1.15; }

  @media (max-width: 860px) {
    .story, .studio { grid-template-columns: 1fr; }
    .story :global(.story-art) { aspect-ratio: 16 / 10 !important; }
    .team :global(.group) { aspect-ratio: 4 / 3; }
  }
  @media (prefers-reduced-motion: reduce) {
    .cards li :global(.asset) { transition: none; }
  }
</style>
