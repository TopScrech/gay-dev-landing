import { LINKS } from './site'

export type Figure = {
  images: { src: string; alt: string; ratio: string }[]
  caption?: string
}

export type Post = {
  slug: string
  number: number
  title: string
  date: string
  excerpt: string
  tags?: string[]
  // Thumbnail on the dev blog list
  cover: string
  // Strings are paragraphs: lines starting with '## ' render as subheadings, [text](url) as links
  // Figures render one or more images side by side
  body: (string | Figure)[]
}

// Newest first
export const posts: Post[] = [
  {
    slug: 'laying-the-foundations',
    number: 1,
    title: 'Laying the foundations',
    date: '2026-10-06',
    excerpt: 'Weeks 1 & 2: we set up the studio, split into teams, and took our game from paper to a first playable prototype.',
    cover: '/images/blog/devblog-1/creature-concept.webp',
    body: [
      'Welcome to the very first Moonberry Games dev blog! We didn’t just spend the last two weeks building our studio from the ground up — we also took the idea for our upcoming game off the paper and turned it into a first playable prototype.',
      'Follow along for a look behind the scenes of our magical forest.',
      '## Moonberry’s vision',
      'Long story short: we’re building a fantasy puzzle game with investigation and action elements, which should soon be playable on platforms like Steam.',
      'You step into the role of a grumpy veteran. A cheeky gnome has burned down your hut, and as if that weren’t enough, it also swiped your belongings and vanished into the forest. You’re basically back to square one. The villagers are kind enough to help you out with tips and tools — but they expect something in return: help with their own monstrous problems.',
      {
        images: [{ src: '/images/blog/devblog-1/veteran-concept.png', alt: 'Sketch of the veteran: a broad-shouldered man with brown hair and stubble, hands on hips', ratio: '651 / 955' }],
        caption: 'A peek at the concept art for our veteran',
      },
      'Ronnie, our Design Lead, describes the core concept like this:',
      '“The flow has two parts. First, you pick up a quest in the village and use your tools like a detective to find clues and track down the creature. Once you know what’s lurking out there, you suddenly have to use those same tools in a completely different way — as combat mechanics, to outsmart the beast.”',
      '## Where we are right now',
      'To keep from getting in each other’s way, we used the first weeks to define roles and form departments.',
      'Team Village looks after the place where our story unfolds. This is also where Team Cabin turns ordinary houses into magical huts. The first layouts for our village are done, and more than one house already has something living in it.',
      'Team Player gives our hero a personality, while Teams Tool 1 & 2 are already equipping players with the means to take investigations in the forest to a whole new level. What these tools will ultimately do during an investigation is something our veteran will have to find out.',
      {
        images: [{ src: '/images/blog/devblog-1/lantern.png', alt: 'Two black lanterns with purple glass roofs, one dark and one glowing warm yellow', ratio: '954 / 717' }],
        caption: 'One of the tools taking shape',
      },
      'We didn’t want to leave out the inhabitants of the forest either, so we’ve already made progress on concepts and first iterations for villagers and other creatures.',
      {
        images: [
          { src: '/images/blog/devblog-1/spider-sketches.png', alt: 'Sketches of spider creatures with button-covered bodies, notes reading “fatter”, “skinny” and “fluffy”, and a curly web', ratio: '816 / 567' },
          { src: '/images/blog/devblog-1/creature-concept.webp', alt: 'Animated greyscale painting of a tentacled creature with a single eye', ratio: '961 / 1021' },
        ],
        caption: 'Early creature concepts',
      },
      'The Sound Department has made its first strides too, turning our forest into an experience for the ears.',
      'After just two weeks, the whole team has already put together a first playable prototype. You can find out more about our team on our [About page](/about).',
      '## Website & socials are live!',
      `To grow Moonberry Games’ online presence, our Marketing Department has already put words into action. Find us on [Instagram](${LINKS.instagram}) and [TikTok](${LINKS.tiktok}).`,
      '## Where are we headed?',
      'We’ll spend the next two weeks polishing our prototype and making the experience more immersive. Our features should tie together more closely and give the player a real goal.',
      'Join us on our journey through the magical forest, and check out our socials so you don’t miss any updates!',
      'Your Moonberry Games',
    ],
  },
]

export const formatDate = (iso: string) =>
  new Date(iso + 'T12:00:00').toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' })

// Splits a paragraph into plain text and [text](url) links
export const inline = (text: string) =>
  text.split(/(\[[^\]]+\]\([^)]+\))/).map((part) => {
    const link = part.match(/^\[([^\]]+)\]\(([^)]+)\)$/)
    return link ? { text: link[1], href: link[2] } : { text: part }
  })
