# gay.dev

A responsive single-page website built with Svelte 5, TypeScript, and Vite, using Bun 1.4.2

## Development

```sh
bun install
bun run dev
```

## Validation and production

```sh
bun run check
bun run build
bun run preview
```

The production output is in `dist` and can be deployed to any static host

## Editing

- `src/App.svelte` — page content and structure
- `src/app.css` — responsive styles
- `public/favicon.svg` — site icon
- `index.html` — page title and HTML entry point

## Docker

```sh
docker build -t gay-dev-landing .
docker run --rm -p 3000:3000 gay-dev-landing
```

Open http://localhost:3000 to view the production site
