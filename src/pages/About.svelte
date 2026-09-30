<script lang="ts">
  import Asset from '../components/Asset.svelte'
  import PageHero from '../components/PageHero.svelte'
  import { GAME_TITLE, PRODUCT_OWNER, STUDIO_NAME, teams } from '../lib/site'
</script>

<PageHero title="About" image="/images/about/hero.jpg">
  <p>{GAME_TITLE} is a first-person monster hunt about a haunted marsh, a lodge full of strange inventions, and the person foolish enough to take the job.</p>
</PageHero>

<section class="game-intro container" aria-labelledby="studio-title">
  <h2 id="studio-title">Meet {STUDIO_NAME}</h2>
  <div class="intro-text">
    <p>
      We are {STUDIO_NAME}. We started in 2026 and are currently based at Hanze University of Applied Sciences, studying CMGT. We are
      currently developing our new product, and you can follow our progress through our biweekly blog posts.
    </p>
    <p>
      Our goal is to listen to feedback and continuously improve the quality of our work, making sure everyone who uses our products has
      a pleasant experience.
    </p>
  </div>
</section>

<section class="owner container" aria-labelledby="owner-title">
  <div class="owner-text">
    <h2 id="owner-title">The product owner</h2>
    <p>
      Keeping a lodge full of strange ideas pointed in the same direction is a job of its own — the product owner looks after the vision
      for {GAME_TITLE}, helping the teams turn that vision into an adventure that feels like one connected world
    </p>
    <p>
      From setting priorities to weighing player feedback, the role is about deciding what matters most for the next step, giving each team
      room to experiment while keeping the monster hunts, inventive tools, and playful sense of unease at the heart of the game
    </p>
  </div>
  <figure class="owner-portrait">
    <Asset src="/images/team/product-owner.jpg" alt="Portrait of {PRODUCT_OWNER.name}, {PRODUCT_OWNER.role}" ratio="4 / 5" />
    <figcaption><span class="name">{PRODUCT_OWNER.name}</span> {PRODUCT_OWNER.role}</figcaption>
  </figure>
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
            <Asset src="/images/team/{team.slug}/lead.jpg" alt="Portrait of {team.lead.name}, {team.lead.role}" ratio="4 / 5" />
            <figcaption><span class="name">{team.lead.name}</span> {team.lead.role}</figcaption>
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
  .owner {
    display: grid;
    grid-template-columns: 1.1fr 1fr;
    gap: clamp(32px, 6vw, 96px);
    align-items: center;
    padding-block: clamp(56px, 8vw, 120px);
  }
  .game-intro { padding-top: clamp(56px, 8vw, 120px); }
  .game-intro h2 { margin-bottom: 28px; }
  .intro-text { max-width: 72ch; color: var(--ink-soft); font-size: 1.075rem; }
  .owner-portrait { width: 100%; max-width: 400px; justify-self: center; }
  h2 { font-size: clamp(2.2rem, 5vw, 3.5rem); }
  .owner-text p { max-width: 58ch; color: var(--ink-soft); font-size: 1.075rem; }
  .owner-text h2 { margin-bottom: 28px; }

  .team { padding-block: clamp(48px, 6vw, 80px) clamp(96px, 12vw, 160px); }
  .team > h2 { margin-bottom: clamp(28px, 4vw, 48px); }
  .teams { display: grid; gap: clamp(48px, 7vw, 88px); }
  .department { position: relative; padding-top: 28px; }
  .department::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 5px;
    background: var(--night-line);
    mask: var(--brush) center / 100% 100% no-repeat;
  }
  .department h3 { margin: 0 0 24px; font-size: clamp(1.8rem, 3vw, 2.6rem); }
  .team-description { max-width: 65ch; margin-bottom: clamp(24px, 3vw, 40px); color: var(--ink-soft); font-size: 1.075rem; }
  .team-description p { margin: 0; }
  .team-description p + p { margin-top: 1em; }
  .team-photos { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 2fr); gap: clamp(16px, 3vw, 40px); align-items: start; }
  figure { margin: 0; min-width: 0; }
  figcaption { margin-top: 14px; font-size: 0.95rem; color: var(--ink-soft); }
  figcaption .name { display: block; font-family: var(--font-display); font-size: 1.6rem; line-height: 1.1; color: var(--ink); }
  .lead figcaption, .owner-portrait figcaption { color: var(--wisp); }

  @media (max-width: 860px) {
    .owner { grid-template-columns: 1fr; }
  }
  @media (max-width: 540px) {
    .team-photos { grid-template-columns: 1fr; gap: 24px; }
    .lead { width: 60%; }
  }
</style>
