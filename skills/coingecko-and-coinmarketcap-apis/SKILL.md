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

Ejemplo:

```bash
curl -s "https://api.geckoterminal.com/api/v2/networks/solana/trending_pools" | jq '.'
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
4. Si hay `429`, aplicar exponential backoff (ver Error Handling). Evitar ráfagas.
5. Presentar primero un resumen accionable; luego detalle.
6. Aclarar que los datos son informativos, sin recomendación financiera.
7. Preferir cache local de respuestas recientes para no abusar del rate limit.

## Error Handling

- **429 Too Many Requests**:
  - CoinGecko ~10–30/min; GeckoTerminal ~10/min; CMC keyless más agresivo.
  - Esperar y reintentar con backoff (ej. 2s, 4s, 8s). Máximo 2–3 reintentos.
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
