import { GAME_TITLE } from './site'

export type Post = {
  slug: string
  number: number
  title: string
  date: string
  excerpt: string
  tags: string[]
  // Paragraphs. Lines starting with '## ' render as subheadings
  body: string[]
}

// Covers load from /images/blog/<slug>.jpg, newest first
export const posts: Post[] = [
  {
    slug: 'teaching-the-kettle-to-scream',
    number: 3,
    title: 'Teaching the kettle to scream',
    date: '2026-09-12',
    excerpt: 'How a joke prop became the most reliable ghost-repellent in the game, and the three versions we threw in the marsh first.',
    tags: ['Tools', 'Design'],
    body: [
      'The kettle started as a gag in a greybox level. You picked it up, it whistled, a placeholder ghost flinched. Playtesters would not put it down.',
      '## Version one: too loud',
      'The first kettle screamed whenever it was full, which meant it screamed constantly. Ghosts fled, sure, but so did every other creature in a two-hundred-metre radius, including the one you were hunting.',
      '## Version three: just loud enough',
      'Now the scream builds with heat. You choose when to let it go, and how long to hold it. Hold it too long and the lid comes off. We are still arguing about whether the lid should be collectible.',
      'Next time: why the butterfly net only catches shadows on Tuesdays.',
    ],
  },
  {
    slug: 'the-marsh-keeps-a-routine',
    number: 2,
    title: 'The marsh keeps a routine',
    date: '2026-08-02',
    excerpt: 'Every creature has a schedule. Here is how we built the timetable, and why the Tallow Hound is always late.',
    tags: ['Monsters', 'Systems'],
    body: [
      `Monsters in ${GAME_TITLE} do not wait for you. They sleep, eat, argue, and wander on a clock that keeps running whether you are watching or not.`,
      'The Bog Choir sings at dusk and sleeps through noon. The Tallow Hound eats candles, so it follows the lamplighter. The thing in the well does not have a schedule, and that is the point.',
      '## Learning a habit is the hunt',
      'Most of your preparation happens before a fight: watching, taking notes in the ledger, choosing which tools to pack. The fight itself is short and loud.',
    ],
  },
  {
    slug: 'why-first-person',
    number: 1,
    title: 'Why first person?',
    date: '2026-06-20',
    excerpt: 'We tried an over-the-shoulder camera for a month. Then a monster stood behind us and we understood.',
    tags: ['Design'],
    body: [
      'A third-person camera lets you see what is behind you. That is a lovely feature for most games and a terrible one for ours.',
      'In first person, your tools are right there in your hands, and the marsh gets to keep its secrets just outside your view. Puzzles become physical: you turn the crank, you pour the salt, you look down and realise you have been standing in the wrong circle.',
    ],
  },
  {
    slug: 'hello-from-the-lodge',
    number: 0,
    title: 'Hello from the lodge',
    date: '2026-05-01',
    excerpt: 'A small team, one very strange marsh, and a crate of half-finished magical inventions. This is where we write things down.',
    tags: ['Studio'],
    body: [
      'We are a small team making a first-person monster-hunting game with inventive tools and frantic puzzle combat. It is early. Most of it is grey boxes and good intentions.',
      'This devlog is where we will share what we are building, what broke, and which monsters survived the latest round of cuts. Thanks for reading along.',
    ],
  },
]

export const formatDate = (iso: string) =>
  new Date(iso + 'T12:00:00').toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' })
