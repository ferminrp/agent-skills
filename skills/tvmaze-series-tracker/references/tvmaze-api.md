# TVmaze API — digest for agents

Official docs: https://www.tvmaze.com/api  
Root: `https://api.tvmaze.com`  
License: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — credit TVmaze and link back.

## Conventions

- JSON over HTTPS.
- No API key for the public API.
- Rate limit: **≥ 20 calls / 10 s** per IP. On HTTP **429**, wait a few seconds and retry.
- Responses may be edge-cached ~**60 minutes**.
- Send a clear **User-Agent**.
- Image URLs on `static.tvmaze.com` are stable per URL (content does not mutate in place).

## Search

### `GET /search/shows?q={query}`

Fuzzy search (fuzziness 2). Returns array of `{ score, show }`, best first.

Use this when building a **local mapping of names → TVmaze ids** and when the user must pick among candidates.

### `GET /singlesearch/shows?q={query}`

Zero or one result (fuzziness 1). Supports `embed=…`.  
**Unsafe for auto-subscribe** when multiple shows share a name.

### `GET /lookup/shows?imdb=tt…` / `?thetvdb=…`

301 redirect to the show resource when known external ids match.

## Shows

### `GET /shows/{id}`

Primary show record. Optional embedding via `?embed=cast` (and others — see official embedding docs).

Useful fields: `id`, `name`, `type`, `language`, `genres[]`, `status`, `premiered`, `ended`, `runtime` / `averageRuntime`, `network` / `webChannel`, `image.{medium,original}`, `summary` (HTML), `url`, `officialSite`, `externals`.

### `GET /shows/{id}/episodes`

All episodes in air order. Default **excludes** specials; `?specials=1` includes them.

Episode fields: `id`, `url`, `name`, `season`, `number` (null for some specials), `airdate`, `airtime`, `airstamp`, `runtime`, `image`, `summary`.

### `GET /shows/{id}/episodesbydate?date=YYYY-MM-DD`

Episodes of that show on a calendar date (when available).

## Schedule

### `GET /schedule?country={ISO3166}&date={YYYY-MM-DD}`

Broadcast/network schedule for a country (default US). UK code is **`GB`**, not UK.  
Does **not** include global streamers like Netflix.

### `GET /schedule/web?date={YYYY-MM-DD}&country={optional}`

Web/streaming schedule. Omit `country` for local+global; `country=` empty string for global-only; set ISO code for local web channels.

### `GET /schedule/full`

All known future episodes (multi-MB). Cached 24h. Prefer per-show `/episodes` for a small favorites list.

## Embedding

Some endpoints accept `embed` / `embed[]` to inline related resources (e.g. `episodes`, `cast`). Prefer embedding only when it saves round-trips you need immediately.

## Agent policy for favorites

1. Resolve titles with **`/search/shows`**.
2. Present **poster + synopsis + network + year** and wait for confirmation.
3. Persist the numeric **`show.id`**, not the free-text name alone.
4. For “airs today”, filter each favorite’s episodes where `airdate == today` (in the user’s timezone policy).
5. Dedupe notifications by **`episode.id`**.
6. Always attribute TVmaze on user-visible digests.
