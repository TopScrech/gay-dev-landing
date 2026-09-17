<script lang="ts">
  const year = new Date().getFullYear()
</script>

<svelte:head>
  <meta name="description" content="A little corner of the internet for building things with pride" />
</svelte:head>

<a class="skip-link" href="#main">Skip to content</a>

<div class="page" id="top">
  <header>
    <a class="wordmark" href="#top" aria-label="gay.dev home">gay<span>.</span>dev</a>
    <nav aria-label="Main navigation">
      <a href="#about">About <span aria-hidden="true">↗</span></a>
    </nav>
  </header>

  <main id="main">
    <section class="hero" aria-labelledby="hero-title">
      <div class="eyebrow"><span class="status" aria-hidden="true"></span> A little corner of the internet</div>
      <h1 id="hero-title">Made of code<br />and a little <span class="pride">pride<span class="asterisk" aria-hidden="true">✳</span></span></h1>
      <div class="hero-bottom">
        <p>A space for curious minds, colorful ideas,<br class="desktop-break" /> and things worth putting into the world</p>
        <a class="button" href="#about">Take a look around <span aria-hidden="true">↘</span></a>
      </div>
      <div class="rainbow" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i></div>
    </section>

    <section class="about" id="about" aria-labelledby="about-title">
      <div class="section-label"><span aria-hidden="true">01 /</span> Hello, world</div>
      <div>
        <h2 id="about-title">Good things start<br />with a blank page</h2>
        <p>This is the beginning of something new — a place to share projects, explore ideas, and make the web a little more personal</p>
        <span class="note">More to come <span aria-hidden="true">✳</span></span>
      </div>
    </section>
  </main>

  <footer>
    <span>© {year} gay.dev</span>
    <span>Built with Svelte <span class="footer-star" aria-hidden="true">✳</span> Made with pride</span>
    <a href="#top">Back to top ↑</a>
  </footer>
</div>
