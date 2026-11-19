# polymarket (REST, public reads) — v1
Docs index: https://docs.polymarket.com/llms.txt · API ref: /_llms/en/api-reference.txt · Rate limits: /api-reference/rate-limits.md
Prediction markets. Price of a "Yes" token (0–1 pUSD) = implied probability. **Read-only: never trade, sign, or create API keys.**

## Auth / limits
- No auth for any endpoint below. Gamma JSON has `cache-control: public, max-age=300` (data can be up to 5 min old).
- Cloudflare IP limits, sliding windows; over the limit requests are **throttled (delayed), not rejected**. Global 15,000 req/10s.
- Gamma 4,000/10s (`/events` 500, `/markets` 300, `/public-search` 350). CLOB 9,000/10s (`/book` `/price` `/midpoint` 1,500; `/books` `/prices` `/midpoints` 500; `/prices-history` 1,000). Data v1 1,000/10s (`/trades` 200); Data v2 800/10s (`/v2/prices-history` 200).

## Model
Event (slug from the URL, `polymarket.com/es/event/<slug>`) → `markets[]`, one binary market per candidate (`groupItemTitle` = name, `negRisk: true` = mutually exclusive set). Each market has 2 CLOB tokens: Yes and No.
**`outcomes`, `outcomePrices`, `clobTokenIds` are JSON-encoded strings**, not arrays: `json.loads()` them. Index 0 = "Yes". Prices are strings ("0.465").

## Links (attribution)
Every polymarket.com link shown to the user (chat, Pages, routine alerts, recipes) **must** carry `via=oraculo.ar`: append `?via=oraculo.ar`, or `&via=oraculo.ar` if the URL already has a query string. Applies to polymarket.com only, not to API hosts (gamma-api / clob / data-api).
- `https://polymarket.com/es/event/argentina-presidential-election-winner?via=oraculo.ar`
- `https://polymarket.com/es/event/argentina-presidential-election-winner?tid=123&via=oraculo.ar`
```python
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
def pm_link(u):
    s=urlsplit(u); q=[(k,v) for k,v in parse_qsl(s.query) if k!="via"]+[("via","oraculo.ar")]
    return urlunsplit(s._replace(query=urlencode(q)))
```

## Endpoints (V = verified live 2026-10-28)
| API | Call | Key fields |
|---|---|---|
| Gamma `https://gamma-api.polymarket.com` | GET /events?slug={slug} (array) or /events/slug/{slug} (object) (V) | id, slug, title, endDate (UTC), active, closed, volume, liquidity, updatedAt, markets[] |
| Gamma | GET /markets?slug={marketSlug} (V), /markets/{id} (V) | id, question, conditionId, slug, groupItemTitle, outcomes, outcomePrices, clobTokenIds, lastTradePrice, bestBid, bestAsk, spread, oneMonthPriceChange, volume24hr, active, closed, negRisk, updatedAt |
| Gamma | GET /public-search?q=argentina%20presidential&limit_per_type=3 (V) | events[] |
| CLOB `https://clob.polymarket.com` | GET /midpoint?token_id= (V) | {"mid":"0.465"} — best probability estimate |
| CLOB | GET /price?token_id=&side=BUY\|SELL (V) | {"price"} — BUY returned best bid (0.46), SELL best ask (0.47) |
| CLOB | GET /spread?token_id= (V) · GET /last-trade-price?token_id= (V) | {"spread"} · {"price","side"} |
| CLOB | GET /book?token_id= (V) | market, asset_id, timestamp (**ms** string), hash, bids[]/asks[]{price,size} (bids ascending: best bid is last) |
| CLOB | POST /midpoints, /prices body `[{"token_id":..,"side"?:..}]` (V) | {token_id: mid} / {token_id:{BUY:..}} |
| CLOB | GET /prices-history?market={token_id}&interval=1h\|6h\|1d\|1w\|1m\|max&fidelity={min} (or startTs/endTs) (V) | history[]{t (unix **s**), p} — `market` is the token id, not conditionId |
| Data `https://data-api.polymarket.com` | GET /v2/prices-history?token_id=&interval=1d (V) | data[]{timestamp (s), price, resolution_seconds} (1-min bars); `market` param → 400 |
| Data | GET /oi?market={conditionId} (V) | [{market, value}] open interest USD |
| Data | GET /holders?market={conditionId}&limit= (V) · /trades?market={conditionId}&limit= (V) | top holders; trades{side,size,price,timestamp (s),title,slug,...} |
Timestamps: Gamma ISO UTC (`Z`); CLOB history and Data in unix seconds; /book in ms. Convert to Buenos Aires (UTC-3).

## Example: Argentina presidential election 2027
```
S=argentina-presidential-election-winner
curl -s "https://gamma-api.polymarket.com/events?slug=$S" | python3 -c '
import json,sys; e=json.load(sys.stdin)[0]
for m in e["markets"]:
  if m["active"] and not m["closed"]:
    p=json.loads(m["outcomePrices"]); t=json.loads(m["clobTokenIds"])
    print(m["groupItemTitle"], float(p[0])*100, t[0])'
Y=<Yes token id>
curl -s "https://clob.polymarket.com/midpoint?token_id=$Y"
curl -s "https://clob.polymarket.com/prices-history?market=$Y&interval=1w&fidelity=1440"
```
Live 2026-10-28 08:07 (Buenos Aires): event 435390, 21 candidate markets, volume ~US$1.13M, ends 2027-10-25T03:59Z. Milei 46.5% (bid 0.46/ask 0.47), Kicillof 29.5%, Massa 11.1%, P. Bullrich 6.4%, Bregman 1.05%, Gebel 1.0%; rest <1%. Milei 1w history 0.475 → 0.465; max history starts 2026-05-01.
Caveats: thin markets (bestBid null, wide spread) → prefer midpoint and flag low liquidity; probabilities across candidates need not sum to exactly 100%. Not a forecast or advice; cite "Polymarket" + time.
