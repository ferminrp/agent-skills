# comparadolar (REST) — v1
Site: https://comparadolar.ar (open source: github.com/enzonotario/comparadolar.ar, same author as ArgentinaDatos/comparatasas). Public API, explicitly invited for devs/agents.
Base: https://api.comparadolar.ar · Auth: none · CORS `*` · `cache-control: public, max-age=60` · Rate limit not published (poll ≥60 s, don't hammer).
Spec: https://comparadolar.ar/openapi.json · Docs: https://comparadolar.ar/docs/ · /llms.txt.
Verified 2026-10-28 (HTTP 200): /usd, /usd/providers, /usd/providers/{slug}/history, /usdt, /btc, /usdt/providers/{slug}/history, /health. /usdc, /eth (+ providers/history) are in the OpenAPI spec, same shape (not called).

## Endpoints
| Endpoint | Use | Key fields |
|---|---|---|
| /usd | USD quotes per provider (29 on 2026-10-28: 15 Oficial, 3 MEP, 5 CCL, 6 Cripto; 11 banks) | slug, prettyName, bid (you sell), ask (you buy) ARS/USD, usdType (Oficial/MEP/CCL/Cripto), isBank, is24x7, pct_variation (% daily), lastSeenAt (ISO UTC), stale, logoUrl, url (referral), conditions |
| /usd/providers | provider metadata, no prices | slug, prettyName, logoUrl, usdType, isBank, is24x7, url, conditions |
| /usd/providers/{slug}/history | per-provider series (~intraday points; start varies per provider: on 2026-11-19 astropay/banco-nacion from 2026-08-21, balanz 2026-08-24, banco-bica 2026-09-10 — looks like a rolling ~90-day window) | bid, ask, timestamp (UTC) |
| /usdt, /usdc, /btc, /eth | crypto quotes per exchange in ARS (e.g. Belo, Binance, Astropay) | slug, prettyName, bid, ask, totalBid, totalAsk, logo, lastSeenAt, stale, url, conditions |
| /{coin}/providers, /{coin}/providers/{slug}/history | crypto metadata / series | ask, totalAsk, bid, totalBid, timestamp |
| /health | liveness | `{"status":"ok"}` |

Slugs are per asset: a slug from /usdt (e.g. `belo`) 404s under /usd. Take slugs from the matching list.

## How to answer
- "Dónde conviene comprar dólar": min `ask` = cheapest to buy; max `bid` = best to sell. Filter by `usdType`; never mix Oficial with MEP/CCL/Cripto.
- Drop `stale:true` rows (or show them flagged "desactualizado").
- Round floats to 2 decimals (values like 1675.00000045 or 1624.2995208316413).
- Convert `lastSeenAt`/`timestamp` from UTC to Buenos Aires (UTC-3).
- Name each provider: "Brubank vía comparadolar: compra 1.545 / venta 1.515 (14:43 ART)". List the best 3–5, not one number.
- `url` carries `?ref=comparadolar`; don't present it as our link. Link https://comparadolar.ar or the provider's plain site instead.
- Logos: `logoUrl` (argentinadatos static) or loguitos.

## Example
curl -s https://api.comparadolar.ar/usd | jq -r 'map(select(.usdType=="Oficial" and (.stale|not))) | sort_by(.ask)[:3][] | "\(.prettyName) ask=\(.ask*100|round/100) bid=\(.bid*100|round/100) \(.lastSeenAt)"'
# 2026-10-28 → Brubank ask=1545 bid=1515 · Reba ask=1545 bid=1490 · Balanz ask=1547 bid=1533 (17:43Z = 14:43 ART)
curl -s https://api.comparadolar.ar/usd/providers/banco-nacion/history | jq '.[-1]'
