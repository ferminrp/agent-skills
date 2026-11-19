# loguitos (REST, public reads) — v1
Site/docs: https://loguitos.app/docs ("Logos Argentina"). No /llms.txt (404 page). Directory of Argentine entities (banks, fintechs, crypto, ALyCs, etc.) with favicon URLs + country flags (SVG).
Base: https://loguitos.app/api · Auth: none · Rate limit: not published (be gentle; responses are CDN-cached 24h with filters).
Terms: none published; site says "Los logos son propiedad de sus respectivas empresas." Use for identification only, never alter/recolor.
All below verified 2026-10-28 (HTTP 200) unless marked.

## Endpoint
GET /api/logos — params: `q` (free text, name or domain), `domain` (partial match, e.g. `com.ar`), `category`, `limit` (default 50, **max 200**; 500 → clamped to 200), `offset`.
Categories: bancos, fintechs, crypto, tecnologias, alycs, acciones, prepagas, banderas, … (19 on the site; 573 entries on 2026-10-28).
Response: {datasetVersion, items[], total, hasMore, filters}. Header `X-Logos-Dataset-Version`.
- Entity item: name, domain, google_domain (Google favicon URL, `sz=128`), duck_domain (DuckDuckGo .ico URL), categoryId, categoryName.
- Flag item (`category=banderas`): code (ISO2), name, svgUrl (country-flag-icons 3x2 SVG), categoryId, categoryName.
- **No size / format / dark-light params.** Images are third-party favicons (PNG/ICO); size only via `sz=` in the Google URL (16–256). No dark variants: put logos on a white/neutral rounded chip in dark UIs.

## Verified examples
| Call | Result |
|---|---|
| `?q=galicia` | 2: Banco Galicia (www.galicia.ar, bancos), Galicia (acciones) |
| `?q=mercado%20pago` | Mercado Pago, mercadopago.com.ar, fintechs |
| `?q=binance` | Binance, binance.com, crypto |
| `?q=ripio` | Ripio, ripio.com, fintechs |
| `?q=bbva` | 2: BBVA Argentina (bbva.com.ar, bancos), BBVA (acciones) |
| `?category=banderas&q=argentina` | AR, svgUrl .../3x2/AR.svg |
| `?q=zzzxq` | items [], total 0 (no 404) |

```bash
curl -s "https://loguitos.app/api/logos?q=ripio" | jq -r '.items[0].google_domain'
# https://s2.googleusercontent.com/s2/favicons?domain=ripio.com&sz=128
```

## Gotchas
- Same brand can appear in several categories (bancos + acciones): filter with `category=` or pick by categoryId.
- Search is by name/domain substring; try the short brand ("galicia", not "Banco de Galicia y Buenos Aires S.A.U.").
- Logo URLs point at Google/DDG, not loguitos; Google redirects (301) and may return a generic globe for unknown domains. Prefer `google_domain` (PNG, sizable), `duck_domain` as backup.
- Cache: `datasetVersion` changes when the dataset updates; cache results per version.

## Fallback when a logo is missing
total 0, image fails to load, or generic globe → render initials (e.g. "MP") or the plain name in a neutral circle/badge. **Never invent, draw, or generate a logo**, and don't pull random images from the web.
