---
name: coingecko-and-coinmarketcap-apis
description: >
  Consulta precios, market cap, trending, historico OHLC, Fear & Greed y datos
  DEX/onchain via APIs keyless (sin API key) de CoinGecko, GeckoTerminal y
  CoinMarketCap. Usar cuando el usuario pida "precio bitcoin", "market cap eth",
  "trending crypto", "fear and greed", "pools solana", "ohlcv dex", "conversion
  BTC a USD/ARS", "CoinGecko", "CoinMarketCap", "GeckoTerminal", o datos crypto
  publicos sin autenticacion.
---

# CoinGecko and CoinMarketCap Keyless APIs

Consulta datos de criptomonedas con las APIs **keyless/public** de CoinGecko,
GeckoTerminal y CoinMarketCap. No requiere API key.

Para catálogo ampliado, comparación de proveedores y docs oficiales, leer
`references/keyless-apis.md`.

## API Overview

| Servicio | Base URL | Auth | Rate limit (aprox.) |
|----------|----------|------|---------------------|
| **CoinGecko** | `https://api.coingecko.com/api/v3` | Ninguna | ~10–30 calls/min (por IP) |
| **GeckoTerminal** | `https://api.geckoterminal.com/api/v2` | Ninguna | ~10 calls/min |
| **CoinMarketCap Keyless** | `https://pro-api.coinmarketcap.com/public-api` | Ninguna (GET only; **no** enviar `X-CMC_PRO_API_KEY`) | Más agresivo que keyed |

- Respuestas: JSON.
- Scope de este skill: solo keyless. No usar Demo/Pro keys en v1.
- No recomendado para producción ni polling frecuente.
- **Realidad empírica del rate limit (jul 2026)**: los límites de arriba son optimistas bajo uso sostenido. Ráfagas cada ~2-3s a CoinGecko o GeckoTerminal empiezan a devolver `429` a los ~8 requests, no a los ~10-30/min nominales — probablemente porque el límite es compartido entre ambos servicios por IP, no independiente por servicio. Espaciar al menos 6-8s entre requests (no 2s) evita la mayoría de los 429 en sesiones de varios minutos.
- **Failure mode no obvio**: cuando se llama desde un browser (`fetch`), un 429 a veces **no** llega como respuesta HTTP 429 sino como `TypeError: Failed to fetch` — un error de red opaco indistinguible de un problema de conectividad real. Si el código solo reintenta en `response.status === 429`, este caso se escapa. Tratar cualquier `fetch` que falle (catch) durante una ráfaga como candidato a rate limit y aplicar el mismo backoff, no solo reintentar en 429 explícito.

### Llamar desde el browser (CORS)

Ambos, CoinGecko y GeckoTerminal, responden `access-control-allow-origin: *`
(confirmado jul 2026) — `fetch()` funciona directo desde código client-side
(ej. un artifact HTML estático) sin proxy ni backend intermedio. Útil para
construir widgets/dashboards que corren enteramente en el browser del
usuario.

## Cuándo usar cada fuente

| Intención | Fuente | Endpoints típicos |
|-----------|--------|-------------------|
| Precio simple, markets, histórico, trending, global | CoinGecko | `/simple/price`, `/coins/markets`, `/coins/{id}/market_chart`, `/search/trending`, `/global` |
| Pools, trades, OHLCV onchain | GeckoTerminal | `/networks/.../trending_pools`, `.../ohlcv/{timeframe}`, `.../trades` |
| Listings, quotes, Fear & Greed, conversión, DEX CMC | CoinMarketCap | `/v3/cryptocurrency/listings/latest`, `/v3/cryptocurrency/quotes/latest`, `/v3/fear-and-greed/latest`, `/v2/tools/price-conversion` |

Regla práctica: CoinGecko para precios/histórico; CMC para rankings/índices/Fear & Greed; GeckoTerminal para DEX onchain.

## Endpoints clave

### CoinGecko

- `GET /simple/price`
- `GET /coins/markets`
- `GET /coins/{id}`
- `GET /coins/{id}/market_chart`
- `GET /coins/{id}/ohlc`
- `GET /coins/{id}/tickers` — mercados individuales donde CoinGecko detecta el coin (exchange/DEX, volumen, spread, `is_stale`, `is_anomaly`, `last_traded_at`). Es el endpoint para responder "¿qué mercados conoce CoinGecko de este token?" o para cruzar contra datos onchain (ver GeckoTerminal abajo) y detectar pools que CoinGecko todavía no lista.
- `GET /search/trending`
- `GET /global`
- `GET /coins/categories`

`{id}` usa slugs de CoinGecko (`bitcoin`, `ethereum`), no tickers sueltos.

Ejemplos:

```bash
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd,ars" | jq '.'

curl -s "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&per_page=10&page=1" | jq '.'

curl -s "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=30&interval=daily" | jq '.'

curl -s "https://api.coingecko.com/api/v3/search/trending" | jq '.'
```

### GeckoTerminal (Onchain DEX)

- `GET /networks/{network}/trending_pools`
- `GET /networks/new_pools`
- `GET /networks/{network}/pools/{address}/ohlcv/{timeframe}`
- `GET /networks/{network}/pools/{address}/trades`
- `GET /networks/{network}/tokens/{address}/pools` — todos los pools de un token en una red
- `GET /networks/{network}/tokens/multi/{addresses}` — **batch**: hasta ~30 addresses separadas por coma en un solo request, con `?include=top_pools` trae de una los pools top de cada token. Reduce N requests a 1 — usarlo siempre que se consulten varios tokens conocidos en la misma red en vez de iterar uno por uno.

Ejemplo:

```bash
curl -s "https://api.geckoterminal.com/api/v2/networks/solana/trending_pools" | jq '.'

# batch: varios tokens, una sola llamada
curl -s "https://api.geckoterminal.com/api/v2/networks/eth/tokens/multi/0xdac17f958d2ee523a2206206994597c13d831ec7,0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48?include=top_pools" | jq '.'
```

### CoinMarketCap Keyless

Prefijo obligatorio: `/public-api` antes del path del endpoint.
Solo `GET`. No enviar header de API key.

- `GET /public-api/v1/cryptocurrency/map`
- `GET /public-api/v3/cryptocurrency/listings/latest`
- `GET /public-api/v3/cryptocurrency/quotes/latest`
- `GET /public-api/v2/cryptocurrency/info`
- `GET /public-api/v1/global-metrics/quotes/latest`
- `GET /public-api/v2/tools/price-conversion`
- `GET /public-api/v1/cryptocurrency/categories`
- `GET /public-api/v3/fear-and-greed/latest`
- `GET /public-api/v3/fear-and-greed/historical`
- DEX: `/public-api/v4/dex/spot-pairs/latest`, `/public-api/v4/dex/pairs/quotes/latest`, `/public-api/v1/dex/token`, etc.

CMC usa IDs numéricos (`1` = BTC, `1027` = ETH) o `symbol` según el endpoint.

Ejemplos:

```bash
curl -s "https://pro-api.coinmarketcap.com/public-api/v1/simple/price?ids=1,1027&convert=USD" | jq '.'

curl -s "https://pro-api.coinmarketcap.com/public-api/v3/cryptocurrency/listings/latest?limit=10" | jq '.'

curl -s "https://pro-api.coinmarketcap.com/public-api/v3/fear-and-greed/latest" | jq '.'

curl -s "https://pro-api.coinmarketcap.com/public-api/v2/tools/price-conversion?amount=100&symbol=BTC&convert=USD,ARS" | jq '.'
```

## Workflow

1. Detectar intención y elegir fuente (tabla de arriba).
2. Validar parámetros:
   - CoinGecko: `ids`/`{id}` (slug), `vs_currency` / `vs_currencies`, `days`, `per_page`.
   - GeckoTerminal: `network` (ej. `solana`, `eth`), `address` de pool, `timeframe`.
   - CMC: IDs numéricos o `symbol`, `convert`, `limit`; path siempre bajo `/public-api`.
3. Ejecutar `curl -s` y parsear con `jq`.
4. Si hay `429` (o un `fetch` que falla en seco durante una ráfaga — ver nota de rate limit arriba), aplicar exponential backoff (ver Error Handling) partiendo de al menos ~10-25s, no 2s. Evitar ráfagas: espaciar requests, no dispararlos en paralelo.
5. Presentar primero un resumen accionable; luego detalle.
6. Aclarar que los datos son informativos, sin recomendación financiera.
7. Preferir cache local de respuestas recientes para no abusar del rate limit.

## Error Handling

- **429 Too Many Requests**:
  - Los límites nominales (CoinGecko ~10–30/min; GeckoTerminal ~10/min; CMC keyless más agresivo) son optimistas en la práctica — ver nota empírica arriba.
  - Esperar y reintentar con backoff más largo de lo intuitivo (ej. 10s, 20s, 40s en vez de 2s, 4s, 8s). Máximo 2–4 reintentos.
  - Desde un browser, un `TypeError: Failed to fetch` durante ráfaga es casi siempre este mismo caso disfrazado — tratarlo igual que un 429 explícito.
- **4xx por params inválidos**:
  - Revisar slug vs ticker (CG), ID numérico (CMC), network/address (GeckoTerminal).
  - Informar el parámetro incorrecto; no inventar IDs.
- **Red/timeout**:
  - Reintentar hasta 2 veces con espera corta.
  - Si falla, devolver mensaje claro con el endpoint consultado.
- **JSON inesperado / endpoint no keyless**:
  - Mostrar mínimo crudo útil y aclarar que el endpoint puede no estar en keyless.

## Presenting Results

- Precio: valor, moneda fiat, timestamp si existe.
- Markets/listings: top N con precio, market cap, volumen, % cambio.
- Histórico/OHLC: ventana pedida y puntos relevantes (inicio, fin, min/max).
- Trending / Fear & Greed: score o lista corta + contexto.
- DEX: pool, network, liquidez/volumen cuando estén en la respuesta.
- No dar consejo de inversión.

## Out of Scope

Este skill no debe usar en v1:

- Headers/keys Demo o Pro (`x-cg-demo-api-key`, `X-CMC_PRO_API_KEY`)
- Base Trial Pro de CMC (`/trial-pro-api`) salvo lectura documentada en references
- Polling continuo o integraciones de producción
- Endpoints que explícitamente requieren plan pago

## Reference

Detalle ampliado: [references/keyless-apis.md](references/keyless-apis.md)
