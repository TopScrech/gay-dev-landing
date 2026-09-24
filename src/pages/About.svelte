<script lang="ts">
  import Asset from '../components/Asset.svelte'
  import PageHero from '../components/PageHero.svelte'
  import { GAME_TITLE, teams } from '../lib/site'
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

<section class="team container" aria-labelledby="team-title">
  <h2 id="team-title">Our teams</h2>
  <div class="teams">
    {#each teams as team (team.slug)}
      <section class="department" aria-labelledby="team-{team.slug}">
        <h3 id="team-{team.slug}">{team.name}</h3>
        <div class="team-description">
          {#each team.paragraphs as paragraph (paragraph)}
            <p>{paragraph}</p>
          {/each}
        </div>
        <div class="team-photos">
          <figure class="lead">
            <Asset src="/images/team/{team.slug}/lead.jpg" alt="{team.name} team lead" ratio="4 / 5" />
            <figcaption>Team lead</figcaption>
          </figure>
          <figure class="group">
            <Asset src="/images/team/{team.slug}/group.jpg" alt="The {team.name} team together" ratio="16 / 10" />
            <figcaption>The {team.name} team</figcaption>
          </figure>
        </div>
      </section>
    {/each}
  </div>
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
  .story-text p { max-width: 58ch; color: var(--ink-soft); font-size: 1.075rem; }
  .story-text h2 { margin-bottom: 28px; }

  .team { padding-block: clamp(48px, 6vw, 80px) clamp(96px, 12vw, 160px); }
  .team > h2 { margin-bottom: clamp(28px, 4vw, 48px); }
  .teams { display: grid; gap: clamp(48px, 7vw, 88px); }
  .department { border-top: 1px solid var(--night-line); padding-top: 24px; }
  .department h3 { margin: 0 0 24px; font-size: clamp(1.8rem, 3vw, 2.6rem); }
  .team-description { max-width: 65ch; margin-bottom: clamp(24px, 3vw, 40px); color: var(--ink-soft); font-size: 1.075rem; }
  .team-description p { margin: 0; }
  .team-description p + p { margin-top: 1em; }
  .team-photos { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 2fr); gap: clamp(16px, 3vw, 40px); align-items: start; }
  figure { margin: 0; min-width: 0; }
  figcaption { margin-top: 14px; font-size: 0.95rem; color: var(--ink-soft); }
  .lead figcaption { color: var(--wisp); }

  @media (max-width: 860px) {
    .story { grid-template-columns: 1fr; }
    .story :global(.story-art) { aspect-ratio: 16 / 10 !important; }
  }
  @media (max-width: 540px) {
    .team-photos { grid-template-columns: 1fr; gap: 24px; }
    .lead { width: 60%; }
  }
</style>
