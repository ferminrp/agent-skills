# comparapix (REST) — v1
Endpoint: GET https://api.comparapix.ar/quotes · Auth: none. Verified 2026-10-28.
Response: object keyed by provider (fiwind, belo, cocos, takenos, satoshitango, prex, lemon, astropay, decrypto, wallbit, arq, mercado-pago, p2pme, vesseo, yodl-pay, wayni, global66, real-tarjeta, real-tarjeta-mep, caipi, ripio, binance, peanut, personal-pay, banco-*, buepp...).
Each: {quotes:[{symbol (BRLARS, BRLUSDT, ...), buy, sell, spread, spread_pct}], logo, url, isPix, updatedAt, stale}
Use: best rate to pay PIX in Brazil from ARS/USDT.
```
curl -s https://api.comparapix.ar/quotes | jq 'to_entries|map({p:.key,q:(.value.quotes[]|select(.symbol=="BRLARS"))})'
```
