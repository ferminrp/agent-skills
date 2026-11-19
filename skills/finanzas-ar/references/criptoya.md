# CriptoYa (REST) — v1
Base: https://criptoya.com/api · Auth: none · Docs: https://criptoya.com/api. Rate limit documented loosely (~120 req/min per IP; treat as unverified). Verified 2026-10-28.
- /dolar — mayorista, oficial, ahorro, tarjeta, blue, mep/ccl (by instrument), cripto: {price|ask|bid, variation, timestamp}
- /{coin}/{fiat}/{volume} e.g. /btc/ars/0.1, /usdt/ars/100, /btc/usd/0.1, /usdt/brl/100 — object per exchange {ask, totalAsk, bid, totalBid, time} (totals include fees)
- /{exchange}/{coin}/{fiat}/{volume} e.g. /binancep2p/usdt/ars/1, /belo/usdt/ars/1 — single {ask, totalAsk, bid, totalBid, time}
- /bancostodos — USD retail price per bank {ask, totalAsk, bid, totalBid, time}. Some banks are not updated anymore (2026-11-19: santander `time` 2025-10, galicia/brubank/macro/piano 2025-12, others months old): filter by `time` (epoch s) and drop rows older than 24 h.
- /fees — withdrawal fees per exchange/coin/network
- /exchanges — exchange ids per country (ar, ...)
```
curl -s https://criptoya.com/api/usdt/ars/100 | jq 'to_entries|sort_by(.value.totalAsk)|.[0:3]'
```
