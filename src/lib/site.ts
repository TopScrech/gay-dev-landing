// Placeholder title: change it here and it updates everywhere
export const GAME_TITLE = 'Mirewick'
export const STUDIO_NAME = 'gay.dev'
export const TAGLINE = 'A first-person monster hunt through a marsh that keeps odd hours'

// Swap '#' for real URLs when they exist
export const LINKS = {
  wishlist: '#',
  discord: '#',
  bluesky: '#',
  presskit: '#',
}

// YouTube/Vimeo embed URL. Empty shows the poster with "Trailer coming soon"
export const TRAILER_URL = ''

// 'cards' = small portrait card per person, 'photo' = one big group photo with a roster
// Preview either with ?team=cards or ?team=photo on /about
export type TeamLayout = 'cards' | 'photo'
export const TEAM_LAYOUT: TeamLayout = 'cards'

export type Member = { slug: string; name: string; role: string; bio: string }

// Portraits load from /images/team/<slug>.jpg, the group photo from /images/team/group.jpg
export const team: Member[] = [
  { slug: 'ada', name: 'Ada Placeholder', role: 'Creative direction', bio: 'Decides which monsters are allowed to be cute. Overruled weekly' },
  { slug: 'bram', name: 'Bram Stand-in', role: 'Programming', bio: 'Wrote the physics for a kettle that screams. Would do it again' },
  { slug: 'cleo', name: 'Cleo Temporary', role: 'Art & animation', bio: 'Paints every tree slightly crooked on purpose' },
  { slug: 'dax', name: 'Dax Namegoeshere', role: 'Sound & music', bio: 'Recorded the Bog Choir in an actual bathtub' },
  { slug: 'eli', name: 'Eli Tbd', role: 'Design & puzzles', bio: 'Keeps a spreadsheet of every way a hex can go wrong' },
]
