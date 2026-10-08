<script lang="ts">
  import { onMount } from 'svelte'
  import { location_ } from '../lib/router.svelte'
  import { STUDIO_NAME, games } from '../lib/site'

  const nav = [
    { href: '/merch', label: 'Merch' },
    { href: '/devlog', label: 'Dev blog' },
    { href: '/about', label: 'About' },
  ]

  let scrolled = $state(false)
  let open = $state(false)
  let gamesOpen = $state(false)
  let gamesMenu: HTMLElement

  const isCurrent = (href: string) => (href === '/' ? location_.path === '/' : location_.path.startsWith(href))

  $effect(() => {
    location_.path
    open = false
    gamesOpen = false
  })

  onMount(() => {
    const onScroll = () => (scrolled = scrollY > 24)
    onScroll()
    addEventListener('scroll', onScroll, { passive: true })
    return () => removeEventListener('scroll', onScroll)
  })
</script>

<svelte:window
  onkeydown={(e) => e.key === 'Escape' && (open = gamesOpen = false)}
  onclick={(e) => gamesOpen && !gamesMenu.contains(e.target as Node) && (gamesOpen = false)}
/>

<header class="site-header" class:scrolled class:open>
  <a class="brand" href="/" aria-label="{STUDIO_NAME} home">{STUDIO_NAME}</a>

  <button class="menu-toggle" aria-expanded={open} aria-controls="site-nav" onclick={() => (open = !open)}>
    <span class="bars" aria-hidden="true"><i></i><i></i></span>
    <span class="visually-hidden">Menu</span>
  </button>

  <nav id="site-nav" aria-label="Main">
    <a href="/" aria-current={isCurrent('/') ? 'page' : undefined}><span>Home</span></a>
    <div class="dropdown" class:expanded={gamesOpen} bind:this={gamesMenu}>
      <button class="dropdown-toggle" class:current={isCurrent('/games')} aria-expanded={gamesOpen} aria-controls="games-menu" onclick={() => (gamesOpen = !gamesOpen)}>
        <span>Games</span>
        <svg class="caret" viewBox="0 0 12 8" aria-hidden="true"><path d="M1.5 1.5 6 6l4.5-4.5" /></svg>
      </button>
      <ul id="games-menu" class="dropdown-menu">
        {#each games as game (game.href)}
          <li><a href={game.href} aria-current={isCurrent(game.href) ? 'page' : undefined}><span>{game.title}</span></a></li>
        {/each}
      </ul>
    </div>
    {#each nav as item (item.href)}
      <a href={item.href} aria-current={isCurrent(item.href) ? 'page' : undefined}><span>{item.label}</span></a>
    {/each}
  </nav>
</header>

<style>
  .site-header {
    position: fixed;
    inset: 0 0 auto;
    z-index: var(--z-sticky);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    height: var(--header-h);
    padding: var(--header-safe-top) max(var(--gutter), env(safe-area-inset-right, 0px)) 0 max(var(--gutter), env(safe-area-inset-left, 0px));
  }
  /* Safari samples the fixed element's own background for the status-bar area */
  .site-header.scrolled, .site-header.open {
    background-color: var(--night-deep);
  }
  /* Keep the decorative mask below the header's solid background */
  .site-header::before {
    content: '';
    position: absolute;
    inset: 100% 0 auto;
    height: 12px;
    z-index: -1;
    background: var(--night-deep);
    mask: url("/images/header-torn-edge.svg") left top / 100% 12px no-repeat;
    opacity: 0;
    transition: opacity 0.4s var(--ease-out);
  }
  .scrolled::before, .open::before { opacity: 1; }
  .brand {
    font-family: var(--font-display);
    font-weight: 800;
    font-size: 2.1rem;
    letter-spacing: 0.01em;
    line-height: 1;
  }
  nav {
    display: flex;
    align-items: center;
    gap: clamp(16px, 2.6vw, 36px);
    font-weight: 700;
    font-size: 1.05rem;
  }
  nav a {
    position: relative;
    padding: 6px 0;
    color: var(--ink-soft);
    transition: color 0.2s;
  }
  nav a:hover, nav a[aria-current='page'] { color: var(--ink); }
  /* Current tab: a brush stroke exactly as wide as the label, painted on left to right */
  nav a span, .dropdown-toggle span { position: relative; }
  nav a span::after, .dropdown-toggle span::after {
    content: '';
    position: absolute;
    left: -2px;
    right: -3px;
    bottom: -7px;
    height: 5px;
    background: var(--wisp);
    mask: var(--brush) center / 100% 100% no-repeat;
    clip-path: inset(0 100% 0 0);
    transition: clip-path 0.45s var(--ease-out);
  }
  nav a[aria-current='page'] span::after, .dropdown-toggle.current span::after { clip-path: inset(0 0 0 0); }
  .dropdown { position: relative; }
  .dropdown-toggle {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 6px 0;
    border: 0;
    background: none;
    font: inherit;
    color: var(--ink-soft);
    cursor: pointer;
    transition: color 0.2s;
  }
  .dropdown-toggle:hover, .dropdown-toggle.current, .expanded .dropdown-toggle { color: var(--ink); }
  .caret {
    width: 11px;
    height: 8px;
    fill: none;
    stroke: currentColor;
    stroke-width: 2;
    stroke-linecap: round;
    stroke-linejoin: round;
    transition: transform 0.3s var(--ease-out);
  }
  .expanded .caret { transform: rotate(180deg); }
  .dropdown-menu {
    position: absolute;
    top: calc(100% + 12px);
    left: -18px;
    min-width: 200px;
    margin: 0;
    padding: 10px 18px;
    list-style: none;
    background: var(--night-deep);
    border-radius: 6px;
    box-shadow: 0 20px 40px oklch(from var(--night-deep) l c h / 0.6);
    opacity: 0;
    translate: 0 -6px;
    visibility: hidden;
    transition: opacity 0.2s, translate 0.25s var(--ease-out), visibility 0s 0.25s;
  }
  .expanded .dropdown-menu {
    opacity: 1;
    translate: 0;
    visibility: visible;
    transition: opacity 0.2s, translate 0.25s var(--ease-out);
  }
  .dropdown-menu a { display: block; white-space: nowrap; }
  /* Open on hover for pointer devices; the gap above the menu is bridged so it stays open */
  @media (hover: hover) and (min-width: 761px) {
    .dropdown-menu::before { content: ''; position: absolute; inset: -12px 0 100%; }
    .dropdown:hover .dropdown-toggle { color: var(--ink); }
    .dropdown:hover .caret { transform: rotate(180deg); }
    .dropdown:hover .dropdown-menu {
      opacity: 1;
      translate: 0;
      visibility: visible;
      transition: opacity 0.2s, translate 0.25s var(--ease-out);
    }
  }
  .menu-toggle {
    display: none;
    width: 44px;
    height: 44px;
    margin-right: -10px;
    border: 0;
    background: none;
    color: inherit;
    cursor: pointer;
  }
  .bars { display: grid; gap: 7px; width: 24px; margin: auto; }
  .bars i {
    display: block;
    height: 2px;
    border-radius: 2px;
    background: currentColor;
    transition: transform 0.3s var(--ease-out);
  }
  .open .bars i:first-child { transform: translateY(4.5px) rotate(45deg); }
  .open .bars i:last-child { transform: translateY(-4.5px) rotate(-45deg); }

  @media (max-width: 760px) {
    /* Expose a solid header on first paint, before Safari samples its top edge */
    .site-header { background-color: var(--night-deep); }
    .site-header::before { opacity: 1; }
    .menu-toggle { display: block; }
    nav {
      position: fixed;
      inset: var(--header-h) 0 auto;
      flex-direction: column;
      align-items: stretch;
      gap: 0;
      padding: 8px var(--gutter) 24px;
      background: oklch(from var(--night-deep) l c h / 0.98);
      box-shadow: 0 30px 40px oklch(from var(--night-deep) l c h / 0.5);
      font-size: 1.15rem;
      clip-path: inset(0 0 100% 0);
      visibility: hidden;
      transition: clip-path 0.4s var(--ease-out), visibility 0s 0.4s;
    }
    .open nav {
      clip-path: inset(0 0 0 0);
      visibility: visible;
      transition: clip-path 0.4s var(--ease-out);
    }
    nav a {
      padding: 14px 0;
      background: linear-gradient(var(--night-line), var(--night-line)) bottom / 100% 5px no-repeat;
      mask: linear-gradient(#000, #000) top / 100% calc(100% - 5px) no-repeat, var(--brush) bottom / 100% 5px no-repeat;
    }
    .dropdown-toggle {
      width: 100%;
      justify-content: space-between;
      padding: 14px 0;
      background: linear-gradient(var(--night-line), var(--night-line)) bottom / 100% 5px no-repeat;
      mask: linear-gradient(#000, #000) top / 100% calc(100% - 5px) no-repeat, var(--brush) bottom / 100% 5px no-repeat;
    }
    /* The submenu opens inline inside the mobile sheet */
    .dropdown-menu {
      position: static;
      display: none;
      min-width: 0;
      padding: 0 0 0 20px;
      background: none;
      box-shadow: none;
      opacity: 1;
      translate: 0;
      visibility: visible;
    }
    .expanded .dropdown-menu { display: block; }
  }
  @media (prefers-reduced-motion: reduce) {
    .site-header::before, nav, .open nav, nav a span::after, .dropdown-toggle span::after, .caret, .dropdown-menu { transition: none; }
  }
</style>
