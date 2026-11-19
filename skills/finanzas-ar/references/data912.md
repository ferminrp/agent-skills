# data912 (REST) — v1
Base: https://data912.com · Auth: none · Docs: /openapi.json, /docs. "Educational, not real-time": data refreshed ~every 20 s (spec: "Not real time, endpoints data refreshed every 20 seconds"). Cloudflare cache: `max-age=30` on /live/*, `max-age=3600` (1 h) on /historical/* and /eod/*. Rate limit 120 req/min (per spec).
All 15 GET endpoints verified 2026-10-28 (HTTP 200).

## Live panels (array of rows)
Fields: symbol, q_bid, px_bid, px_ask, q_ask, v (volume), q_op (trades), c (last), pct_change
- /live/arg_stocks — BYMA acciones
- /live/arg_cedears — CEDEARs (ARS)
- /live/arg_bonds — soberanos (AL30, GD30, AE38...)
- /live/arg_notes — letras/LECAPs
- /live/arg_corp — ONs
- /live/arg_options — opciones BYMA (symbol e.g. GFGC...)
- /live/usa_stocks, /live/usa_adrs — US quotes (USD)
- /live/mep — implied MEP per ticker: ticker, bid, ask, close, mark, v_ars, v_usd, q_ars, q_usd, ars_bid...
- /live/ccl — implied CCL: ticker_usa, ticker_ar, CCL_bid, CCL_ask, CCL_close, CCL_mark, ars_volume, volume_rank...

## Historical daily OHLC (array)
- /historical/stocks/{ticker} · /historical/cedears/{ticker} · /historical/bonds/{ticker}
Fields: date, o, h, l, c, v, dr (daily return), sa (sigma annualized = annualized vol, decimal). Sorted ascending (oldest first): use `.[-N:]` for latest bars.
Unknown ticker → HTTP 200 with `{"Error":"Nahh no tengo ese ticker loko"}` (object, not array): check for an `Error` key.

## EOD options
- /eod/volatilities/{ticker} — iv_s_term, iv_m_term, iv_l_term + *_percentile, ...
- /eod/option_chain/{ticker} — rows: opex, s_symbol, type, k, oi, c, iv, bid, ask, greeks, fair_value

```
curl -s https://data912.com/live/arg_bonds | jq '.[]|select(.symbol=="AL30")'
curl -s https://data912.com/historical/stocks/GGAL | jq '.[-5:]'
```
