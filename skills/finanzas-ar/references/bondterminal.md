# bondterminal (REST + MCP) — v1
Site: https://bondterminal.com · Docs: /developers.md, /llms.txt, OpenAPI /openapi.json (v1.3.0, also /openapi-v1.yaml), Swagger /api/v1/docs/.
ISIN-first analytics for USD (and EUR) sovereign/corporate bonds, focused on Argentina: price ↔ yield (TIR) ↔ spread, duration, convexity, DV01, cashflows, history, riesgo país.
Base URL: https://bondterminal.com/api/v1 · MCP: https://bondterminal.com/mcp (JSON-RPC, same keys/quotas).

## Auth — you need to sign up and get an API key
- **Unlike the other sources, this one needs an account.** Create a free account at https://bondterminal.com/developers#your-key (passwordless: magic link or Google; no card). Create a self-serve key (`bt_live_...`, 12-month expiry).
- Keep it in env **`BONDTERMINAL_API_KEY`**. Header: `Authorization: Bearer $BONDTERMINAL_API_KEY` (no query-string option).
- Without a key: only `GET /treasury-curve` (REST) and MCP `bondterminal_treasury_curve` / `bondterminal_riesgo_pais` (snapshot). Everything else returns 402 (x402 pay-per-call: $0.01 USDC on Base, history $0.10) or 401. Do not use x402.
- Without the key, fall back to data912 (prices) / comparatasas (CER TIR) / argentinadatos (riesgo país).

## Limits (free self-serve key, per docs)
| Limit | Value |
|---|---|
| Requests/min | 100 per key (header `RateLimit-Policy: "default";q=100;w=60`, verified) |
| /bonds/facets, /bonds/batch | 30/min · /bonds/search 60/min · 4 concurrent search/batch |
| Calculations/day | **25** (each bond in /calculate, /calculate/batch, /analytics, /cashflows = 1) |
| Read units/day | **200** (facets 1; search 1/row; batch 1/identifier; history 10, 304 via If-None-Match = 0; riesgo-pais 0; riesgo-pais/history 1) |
| Pro plan | 250 calc + 2,000 reads/day |
| Reset | 00:00 UTC (21:00 Buenos Aires). Read `X-Quota-Remaining`, `X-Read-Quota-Remaining`, `X-Quota-Reset` headers. |
Budget hard: 25 calcs/day is small. Prefer one /bonds/batch (≤10 ids on Basic) over many /analytics.

## Identifiers
Any one of `isin` (US040114HS26), `ticker` ("ARGENT 0.75 30"), `localTicker` (GD30D). AL30/AL30C/AL30D resolve to the same bond; Argentine bonds price off **cable USD** by default (`market.quoteBasis`). Exact match only; unknown → 404.

## Endpoints
Status: V = verified live 2026-10-28; D = from docs/OpenAPI (needs key, returned 401/402 keyless).
| Method / path | Status keyless | Cost | Notes / key fields |
|---|---|---|---|
| GET /treasury-curve | **200 (V)** | free | date, rates{1M..30Y}, source, lastUpdated |
| GET /riesgo-pais | 402 | 0 reads | EMBI-style spread bps (D) |
| GET /riesgo-pais/history?range|start&end | 402 | 1 read | series (D) |
| GET /riesgo-pais/methodology | 401 | — | (D) |
| GET /bonds?search&country=AR&type=sovereign&limit&offset | 402 | — | catalog list (D) |
| GET /bonds/facets | 402 | 1 read | coverage counts (D) |
| POST /bonds/search {filters{country,currency,ytwMin,ytwMax,outstandingMinMillions...}} | 402 | 1 read/row | rows with ytm, leadYield, gSpread, paymentFrequency (D) |
| POST /bonds/batch {identifiers:[...]} | **401 (key only)** | 1 read/id | watchlist quotes (D) |
| GET /bonds/{isin} | 402 | — | reference data (D) |
| GET /bonds/{id}/analytics?fields=market,yields,risk,spreads,pricing,schedule,issuance,workout | 402 | 1 calc | latest price + full analytics (D) |
| GET /bonds/{id}/cashflows?settlement=YYYY-MM-DD | 402 | 1 calc | cashflows[]{date, couponPayment, principalPayment, totalPayment, remainingNotional, paymentType}, summary (D) |
| GET /bonds/{id}/history?range=1w|1m|3m|ytd|1y|2y or start/end | 402 | 10 reads | daily price, ytm, ytw, gSpread; ETag (D) |
| POST /calculate {one id + one of price|ytm|gSpread|zSpread, settlement?} | 402 | 1 calc | what-if (D) |
| POST /calculate/batch {bonds:[...≤50]} | **401 (key only)** | 1 calc/bond | (D) |

Response blocks (analytics/calculate): `market{price,timestamp,change{points1D,percent1D,previousClose}}`, `yields{ytm,ytw,ytc,currentYield,headline,headlineBasis}`, `risk{modifiedDuration,macaulayDuration,effectiveDuration,convexity,dv01}`, `spreads{gSpread,zSpread,treasuryYield,treasuryTenor}` (bps), `pricing{cleanPrice,accruedInterest,dirtyPrice}`, `schedule{nextCouponDate,daysToNextCoupon,averageLife}`, `issuance{...}`, `conventions`.
**Yields are semi-annual bond-equivalent (S.A., ACT/365)**, not effective annual: 9.24% TEA ≈ 9.04% S.A. Say so when comparing with TIRs from other sources. Prices per 100 face.

Errors: `{error,message,details}` · 401 missing_auth / invalid_auth (verified with a bogus key) · 402 payment_required (+ `PAYMENT-REQUIRED` header, verified) · 404 not_found / NO_HISTORY · 422 no_market_data · 429 rate_limited / concurrency_limited / quota_exceeded (stop until resetAt).

## Examples
```
# verified keyless
curl -s https://bondterminal.com/api/v1/treasury-curve
# → {"date":"2026-10-27","rates":{"1M":4.1,...,"10Y":4.99,"30Y":5.3},"source":"TREASURY_GOV",...}

# keyless riesgo país via MCP (verified: 753 bps as of 2026-10-27, deltas 1d -12, 1w +81, 1m +144)
curl -s -X POST https://bondterminal.com/mcp -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"bondterminal_riesgo_pais","arguments":{}}}'

# with key (docs)
H="Authorization: Bearer $BONDTERMINAL_API_KEY"
curl -s -H "$H" "https://bondterminal.com/api/v1/bonds/GD30D/analytics?fields=market,yields,risk"
curl -s -H "$H" https://bondterminal.com/api/v1/bonds/GD35D/cashflows
curl -s -H "$H" -H 'Content-Type: application/json' -X POST https://bondterminal.com/api/v1/calculate -d '{"localTicker":"AL30","price":80}'
```
Doc example (GD30D analytics, 2026-06): price 65.84, ytm 6.10, modifiedDuration 1.85, gSpread 205 bps, accrued 0.229.
MCP tools: bondterminal_search_bonds, _get_bonds, _calculate, _get_history, _riesgo_pais, _treasury_curve, _get_usage (free; quota check).
