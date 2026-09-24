<footer>
  <div class="footer-invitation">
    <div class="content invitation-inner">
      <h2>Follow the adventure<br />as it takes shape</h2>
      <a class="journal-button" href="#/blog">Development journal <span aria-hidden="true">↗</span></a>
    </div>
  </div>
  <div class="footer-landscape">
    <div class="content footer-inner">
      <a class="footer-brand" href="#/" aria-label="Untitled adventure home">
        <span class="footer-emblem" aria-hidden="true">✳</span>
        <span>UNTITLED<small>A STRANGE LITTLE ADVENTURE</small></span>
      </a>
      <div class="footer-details">
        <p class="footer-status"><span aria-hidden="true"></span> An independent game in development</p>
        <nav aria-label="Footer navigation">
          <a href="#/">Home</a>
          <a href="#/about">About the game</a>
          <a href="#/blog">Dev blog</a>
        </nav>
        <p class="copyright">Untitled adventure © {new Date().getFullYear()}<br />Working title · More from the wilds soon</p>
      </div>
    </div>
  </div>
</footer>

<style>
  footer { background: #314b40 }
  .footer-invitation { background: #3d5749 }
  .invitation-inner { display: flex; justify-content: space-between; align-items: center; gap: 40px; padding-block: 42px }
  h2 { margin: 0; font-family: 'Arial Narrow', Arial, sans-serif; font-stretch: condensed; font-size: clamp(24px, 3vw, 36px); font-weight: 700; line-height: 1.25; letter-spacing: .04em; text-transform: uppercase }
  .journal-button { display: inline-flex; align-items: center; justify-content: space-between; gap: 30px; background: #a94d40; border: 1px solid #e9e4d1; padding: 21px 26px; font-size: 13px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase }
  .journal-button:hover { background: #bb5b4d }
  .journal-button span { font-size: 21px }
  .footer-landscape { background: linear-gradient(#243e33e6, #142f27eb), url('/images/forest.svg') center 65% / cover }
  .footer-inner { display: flex; justify-content: space-between; align-items: flex-start; gap: 50px; padding-block: 52px 36px }
  .footer-brand { display: flex; align-items: center; gap: 18px; padding-top: 8px; color: #f0ead7; font: bold 29px Georgia, serif; letter-spacing: .08em }
  .footer-emblem { font-size: 66px; line-height: 1; font-weight: normal }
  .footer-brand small { display: block; margin-top: 8px; font: 8px Arial, sans-serif; letter-spacing: .15em }
  .footer-details { text-align: right }
  .footer-status { display: flex; align-items: center; justify-content: flex-end; gap: 9px; color: #d2dbcb; font-size: 11px; margin-bottom: 17px }
  .footer-status span { width: 6px; height: 6px; border-radius: 50%; background: #d5bc89 }
  nav { display: flex; justify-content: flex-end; gap: 22px; flex-wrap: wrap }
  nav a { padding: 4px 0; font-size: 12px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase }
  nav a:hover { color: #eabd7b }
  .copyright { margin: 32px 0 0; color: #bccbbd; font-size: 10px; line-height: 1.8 }
  @media (max-width: 760px) {
    .invitation-inner { align-items: flex-start; flex-direction: column; gap: 24px; padding-block: 32px }
    .journal-button { padding: 17px 20px; font-size: 11px }
    .footer-inner { flex-direction: column; gap: 32px; padding-block: 36px }
    .footer-brand { font-size: 26px }
    .footer-emblem { font-size: 56px }
    .footer-details { text-align: left }
    .footer-status, nav { justify-content: flex-start }
    nav { gap: 20px }
    nav a { font-size: 11px }
    .copyright { margin-top: 26px }
  }
</style>
