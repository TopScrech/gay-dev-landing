FROM oven/bun:1.4.2 AS build
WORKDIR /app

COPY package.json bun.lock ./
RUN --mount=type=cache,id=gay-dev-landing-bun,target=/root/.bun/install/cache \
    BUN_INSTALL_CACHE_DIR=/root/.bun/install/cache bun install --frozen-lockfile

# Keep unrelated files and nginx changes from invalidating the app build
COPY index.html vite.config.ts svelte.config.js tsconfig*.json ./
COPY src ./src
COPY public ./public
RUN bun run build

FROM nginx:stable-alpine AS runtime
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
