export const STUDIO_NAME = 'Moonberry Games'

// Placeholder game title: change it here and it updates everywhere
export const GAME_TITLE = 'game_title'
export const TAGLINE = 'A first-person monster hunt through a marsh that keeps odd hours'

// Swap '#' for real URLs when they exist
export const LINKS = {
  wishlist: '#',
  discord: '#',
  instagram: 'https://instagram.com/moonberry.games',
  tiktok: 'https://tiktok.com/@moonberrygames',
  presskit: '#',
  hosting: 'https://crunchy.host',
}

// Listed under the Games dropdown in the header
export const games = [{ title: GAME_TITLE, href: '/games/untitled' }]

// YouTube/Vimeo embed URL. Empty shows the poster with "Trailer coming soon"
export const TRAILER_URL = ''

// Product owner shown above the teams on the About page
export const PRODUCT_OWNER = { name: 'Alex', role: 'Product Owner' }

// Each department has a Discord lead avatar and group photo in /images/team/<slug>/
export const teams = [
  {
    slug: 'tech', name: 'Tech',
    lead: { name: 'Pavlos', role: 'Lead Developer' },
    paragraphs: [
      'Tech makes the strange inventions work, from the first pull of a lever to the moment a creature decides to chase you through the marsh',
      'Behind every unruly tool is a carefully built system — and a fair amount of testing to make sure the surprises belong to the game',
    ],
  },
  {
    slug: 'design', name: 'Design',
    lead: { name: 'Ronnie', role: 'Lead Designer' },
    paragraphs: [
      'Design sets the traps, leaves the clues, and gives you just enough room to come up with a terrible idea that might actually work',
      'Every hunt brings tools, creatures, and puzzles together, inviting you to watch closely, experiment, and change your plan when something starts running at you',
    ],
  },
  {
    slug: 'art', name: 'Art',
    lead: { name: 'Lizet', role: 'Lead Artist' },
    paragraphs: [
      'Art gives the marsh its crooked silhouette, the lodge its cluttered warmth, and the monsters faces you might almost trust',
      'From the smallest workshop oddity to the shapes lurking beyond the lantern light, the team balances a little charm with the feeling that something is very wrong',
    ],
  },
  {
    slug: 'audio', name: 'Audio',
    lead: { name: 'Alex Monster', role: 'Lead Audio Design' },
    paragraphs: [
      'Audio fills the marsh with creaking wood, humming contraptions, and noises you would rather believe came from a very small animal',
      'Music and sound give each hunt its rhythm, offering clues, building tension, and making the quiet moments worth listening to',
    ],
  },
  {
    slug: 'marketing', name: 'Marketing',
    lead: { name: 'Padouk de Bie', role: 'Lead Marketing' },
    paragraphs: [
      'Marketing opens the lodge door to the outside world, sharing glimpses of the game and introducing the peculiar things taking shape inside it',
      'Through development stories, trailers, and conversations with players, the team helps curious newcomers find their way to the marsh — preferably before nightfall',
    ],
  },
]
