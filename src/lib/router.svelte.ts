import { tick } from 'svelte'
import { posts } from './posts'

export type Route =
  | { page: 'home' }
  | { page: 'about' }
  | { page: 'devlog' }
  | { page: 'post'; slug: string }
  | { page: 'missing' }

const normalize = (path: string) => (path.length > 1 ? path.replace(/\/+$/, '') : path)

export const location_ = $state({ path: normalize(location.pathname), search: location.search })

export function resolve(path: string): Route {
  if (path === '/') return { page: 'home' }
  if (path === '/about') return { page: 'about' }
  if (path === '/devlog') return { page: 'devlog' }
  const post = path.match(/^\/devlog\/([\w-]+)$/)
  if (post && posts.some((p) => p.slug === post[1])) return { page: 'post', slug: post[1] }
  return { page: 'missing' }
}

export async function navigate(to: string) {
  const url = new URL(to, location.href)
  history.pushState({}, '', url)
  location_.path = normalize(url.pathname)
  location_.search = url.search
  await tick()
  if (url.hash) document.querySelector(url.hash)?.scrollIntoView()
  else window.scrollTo({ top: 0, behavior: 'instant' })
  document.getElementById('main')?.focus({ preventScroll: true })
}

addEventListener('popstate', () => {
  location_.path = normalize(location.pathname)
  location_.search = location.search
})

// Route plain same-origin link clicks through the SPA router
export function interceptLinks(event: MouseEvent) {
  if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return
  const a = (event.target as Element).closest('a')
  if (!a || a.target || a.hasAttribute('download')) return
  const href = a.getAttribute('href')
  if (!href || href.startsWith('#') || href.startsWith('mailto:')) return
  const url = new URL(href, location.href)
  if (url.origin !== location.origin || /\.\w+$/.test(url.pathname)) return
  event.preventDefault()
  if (url.pathname + url.search !== location.pathname + location.search || !url.hash) navigate(url.href)
  else document.querySelector(url.hash)?.scrollIntoView({ behavior: 'smooth' })
}
