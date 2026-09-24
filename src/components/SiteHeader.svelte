<script lang="ts">
  import { onMount } from 'svelte'
  import { location_ } from '../lib/router.svelte'
  import { GAME_TITLE } from '../lib/site'
  import WishlistButton from './WishlistButton.svelte'

  const nav = [
    { href: '/', label: 'Home' },
    { href: '/about', label: 'About' },
    { href: '/devlog', label: 'Dev blog' },
    { href: '/merch', label: 'Merch' },
  ]

  let scrolled = $state(false)
  let open = $state(false)
  let logoFailed = $state(false)

  const isCurrent = (href: string) => (href === '/' ? location_.path === '/' : location_.path.startsWith(href))

  $effect(() => {
    location_.path
    open = false
  })

  onMount(() => {
    const onScroll = () => (scrolled = scrollY > 24)
    onScroll()
    addEventListener('scroll', onScroll, { passive: true })
    return () => removeEventListener('scroll', onScroll)
  })
</script>

<svelte:window onkeydown={(e) => e.key === 'Escape' && (open = false)} />

<header class="site-header" class:scrolled class:open>
  <a class="brand" href="/" aria-label="{GAME_TITLE} home">
    {#if logoFailed}
      {GAME_TITLE}
    {:else}
      <!-- Logo slot: public/images/logo.svg -->
      <img src="/images/logo.svg" alt="" onerror={() => (logoFailed = true)} />
    {/if}
  </a>

  <button class="menu-toggle" aria-expanded={open} aria-controls="site-nav" onclick={() => (open = !open)}>
    <span class="bars" aria-hidden="true"><i></i><i></i></span>
    <span class="visually-hidden">Menu</span>
  </button>

  <nav id="site-nav" aria-label="Main">
    {#each nav as item (item.href)}
      <a href={item.href} aria-current={isCurrent(item.href) ? 'page' : undefined}><span>{item.label}</span></a>
    {/each}
    <WishlistButton compact />
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
    padding: 0 var(--gutter);
    transition: background-color 0.4s var(--ease-out), box-shadow 0.4s var(--ease-out);
  }
  .scrolled, .open {
    background: oklch(0.14 0.035 160 / 0.92);
    box-shadow: 0 1px 0 var(--night-line);
    backdrop-filter: blur(10px);
  }
  .brand {
    font-family: var(--font-display);
    font-weight: 800;
    font-size: 1.9rem;
    letter-spacing: 0.01em;
    line-height: 1;
  }
  .brand img { display: block; height: 40px; width: auto; }
  nav {
    display: flex;
    align-items: center;
    gap: clamp(16px, 2.6vw, 36px);
    font-weight: 600;
    font-size: 0.95rem;
  }
  nav a:not(:global(.wishlist)) {
    position: relative;
    padding: 6px 0;
    color: var(--ink-soft);
    transition: color 0.2s;
  }
  nav a:not(:global(.wishlist)):hover, nav a[aria-current='page'] { color: var(--ink); }
  /* Current tab: a wisp line exactly as wide as the label */
  nav a span { position: relative; }
  nav a span::after {
    content: '';
    position: absolute;
    left: 0;
    right: 0;
    bottom: -6px;
    height: 2px;
    border-radius: 1px;
    background: var(--wisp);
    box-shadow: 0 0 8px var(--wisp);
    transform: scaleX(0);
    transition: transform 0.35s var(--ease-out);
  }
  nav a[aria-current='page'] span::after { transform: scaleX(1); }
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
    .menu-toggle { display: block; }
    nav {
      position: fixed;
      inset: var(--header-h) 0 auto;
      flex-direction: column;
      align-items: stretch;
      gap: 0;
      padding: 8px var(--gutter) 24px;
      background: oklch(0.14 0.035 160 / 0.97);
      box-shadow: 0 1px 0 var(--night-line), 0 30px 40px oklch(0.1 0.03 160 / 0.5);
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
    nav a:not(:global(.wishlist)) { padding: 14px 0; border-bottom: 1px solid var(--night-line); }
    nav :global(.wishlist) { margin-top: 20px; justify-content: center; }
  }
  @media (prefers-reduced-motion: reduce) {
    nav, .open nav, nav a span::after { transition: none; }
  }
</style>
