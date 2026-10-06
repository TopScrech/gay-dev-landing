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
  // Strings are paragraphs: '## ' starts a subheading, '- ' lines make a list, [text](url) is a link
  // Figures render one or more images side by side
  body: (string | Figure)[]
}

// Newest first
export const posts: Post[] = [
  {
    slug: 'laying-the-foundations',
    number: 1,
    title: 'The Foundations',
    date: '2026-10-06',
    excerpt: 'Laying the groundwork in a whimsical forest: how our studio built its first playable prototype in just two weeks.',
    cover: '/images/blog/devblog-1/creature-concept.webp',
    body: [
      'Welcome to Moonberry Games’ very first DevBlog! Over the past two weeks, we’ve been building our studio from the ground up to take our upcoming game from an idea on paper to our first playable prototype!',
      'Follow along for a look behind the scenes in our whimsical forest.',
      '## Moonberry’s vision',
      'Long story short: we are building a fantasy-puzzle game with investigative and action elements, which we plan to bring to platforms like Steam in the near future!',
      'Step into the boots of a grumpy veteran. A mischievous gnome just burned down your cabin and, as if that wasn’t enough, snatched your belongings before disappearing into the forest. You’re back at square one. Luckily, the local villagers are friendly enough to help you out with tips and tools, although they do expect a favor or two in return to deal with their own monstrous problems in and around the village.',
      {
        images: [{ src: '/images/blog/devblog-1/veteran-concept.png', alt: 'Sketch of the veteran: a broad-shouldered man with brown hair and stubble, hands on hips', ratio: '651 / 955' }],
        caption: 'Our grumpy veteran',
      },
      'As our Game Design Lead Ronnie describes it, the game flow consists of two parts. First, you grab a quest in the village and use your tools like a detective to uncover clues and track down the creature. Once you know what’s lurking out there, you suddenly have to use those exact same tools in a completely different way. Use them as combat mechanics to outsmart the beasts.',
      '## Where we stand right now',
      'To make our prototype run so quickly, everyone in the studio dove straight into building the essentials. Our world is already taking shape and the early outlines of the village are in place. Magical huts are being built and the first few inhabitants are already moving into their new homes.',
      {
        images: [{ src: '/images/blog/devblog-1/village-layout.png', alt: 'Hand-drawn village map with a river, houses, a church, fields, a village centre, a private training area and the main character’s house', ratio: '640 / 574' }],
        caption: 'Our village is taking shape',
      },
      'But they are not the only ones new to the forest: our veteran hero is learning to walk in these woods again and is busy testing prototype tools that serve multiple purposes. Whether it’s helping the residents solve the mysteries of the forest or defending himself against what lurks within, our hero is getting ready to do it all.',
      {
        images: [
          { src: '/images/blog/devblog-1/lantern.png', alt: 'Two black lanterns with purple glass roofs, one dark and one glowing warm yellow', ratio: '954 / 717' },
          { src: '/images/blog/devblog-1/creature-concept.webp', alt: 'Animated greyscale painting of a tentacled object with a single eye', ratio: '961 / 1021' },
        ],
        caption: 'Tools of various purpose',
      },
      'And with good reason, as the first creatures are already roaming deep among the trees.',
      {
        images: [
          { src: '/images/blog/devblog-1/spider-sketches.png', alt: 'Sketches of spider creatures with button-covered bodies, notes reading “fatter”, “skinny” and “fluffy”, and a curly web', ratio: '816 / 567' },
          { src: '/images/blog/devblog-1/villager-concept.jpg', alt: 'Painted villager: a grey-haired old woman with round glasses, a green cloak over a purple robe, and a large wooden spoon as a staff', ratio: '3 / 4' },
        ],
        caption: 'Some friendly, some unfriendly creatures',
      },
      'If you want to learn more about the team behind the game, check out our [About Us](/about) page!',
      '## Website & socials are live!',
      'Beyond the development, our marketing team has already set up social media accounts so that you can follow our journey and look into upcoming behind-the-scenes content:',
      `- Instagram: [instagram.com/moonberry.games](${LINKS.instagram})\n- TikTok: [tiktok.com/@moonberrygames](${LINKS.tiktok})`,
      '## What’s next?',
      'With the foundation in place, the next two weeks are all about polishing to make the overall player experience more immersive. Our goal is to connect our core features more seamlessly and give the player a clear, rewarding objective.',
      'Check out our socials and stay tuned for upcoming updates!',
      '– Your Moonberry Games Team',
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
