# APIs Keyless de CoinGecko y CoinMarketCap

Documento de referencia (Julio 2026). Las APIs keyless (Public API / Trial API)
permiten acceder a datos de criptomonedas **sin API key**. Ideales para
prototipado, open source, pruebas, educación y experimentación.

## 1. CoinGecko Keyless Public API

### Base URLs

| Servicio | Base URL | Notas |
|----------|----------|-------|
| **CoinGecko** | `https://api.coingecko.com/api/v3` | Principal |
| **GeckoTerminal** (Onchain DEX) | `https://api.geckoterminal.com/api/v2` | Pools, trades, OHLCV |

### Características

- **Sin autenticación**: no header ni query param.
- **Rate limit**:
  - CoinGecko: ~10–30 calls/min (compartido por IP, dinámico)
  - GeckoTerminal: ~10 calls/min
  - **En la práctica (jul 2026)**: ambos límites parecen compartir presupuesto por IP — ráfagas cada 2-3s cortan a 429 mucho antes de los ~10-30/min nominales (a los ~8 requests). Espaciar 6-8s+ entre llamadas es más confiable que confiar en el número nominal. Desde un browser, el 429 a veces aparece como `TypeError: Failed to fetch` en vez de una respuesta HTTP — tratarlo igual.
- **CORS**: ambos responden `access-control-allow-origin: *` — llamables directo desde `fetch()` client-side sin proxy.
- **Límite mensual**: no hay cuota mensual estricta como Demo; el cuello es el rate limit por IP.
- **Catálogo**: 50+ endpoints CoinGecko + 20+ GeckoTerminal (mismo catálogo que Demo, rate más bajo).

### Endpoints útiles (Keyless)

**CoinGecko:**

- `/simple/price` — precios simples
- `/coins/markets` — lista con market cap, volumen, etc.
- `/coins/{id}` — detalle de una moneda
- `/coins/{id}/market_chart` — histórico (hasta ~1 año en muchos casos)
- `/coins/{id}/ohlc` — OHLC
- `/search/trending` — tendencias
- `/global` — estadísticas globales
- `/coins/categories` — categorías

**GeckoTerminal:**

- `/networks/{network}/trending_pools`
- `/networks/new_pools`
- `/networks/{network}/pools/{address}/ohlcv/{timeframe}`
- `/networks/{network}/pools/{address}/trades`
- `/networks/{network}/tokens/{address}/pools` — todos los pools de un token
- `/networks/{network}/tokens/multi/{addresses}` — batch (~30 addresses, coma-separadas) + `?include=top_pools`

### Ejemplos

```bash
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd,ars" | jq '.'

curl -s "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&per_page=10&page=1" | jq '.'

curl -s "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=30&interval=daily" | jq '.'

curl -s "https://api.coingecko.com/api/v3/coins/bitcoin/tickers?include_exchange_logo=false" | jq '.tickers[] | {market: .market.identifier, vol: .converted_volume.usd, stale: .is_stale}'

curl -s "https://api.geckoterminal.com/api/v2/networks/solana/trending_pools" | jq '.'

# batch: N tokens conocidos en una red, 1 sola llamada
curl -s "https://api.geckoterminal.com/api/v2/networks/eth/tokens/multi/0xdac17f958d2ee523a2206206994597c13d831ec7,0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48?include=top_pools" | jq '.'
```

### Keyless vs Demo Key (CoinGecko)

| Aspecto | Keyless | Demo Key |
|---------|---------|----------|
| Auth | Ninguna | Header `x-cg-demo-api-key` |
| Rate limit | ~10–30/min (IP) | Más alto y estable (~30–100/min) |
| Tracking | No | Sí (dashboard) |
| Ideal para | Prototipado, OSS, tests | Personal / staging |
| Producción | No recomendado | Aceptable bajo volumen |

**Docs oficiales:**

- [Keyless Public API - CoinGecko](https://docs.coingecko.com/docs/keyless-public-api)
- [Demo Endpoint Overview](https://docs.coingecko.com/demo/reference/endpoint-overview)
- [GeckoTerminal DEX API](https://www.geckoterminal.com/dex-api)

## 2. CoinMarketCap Keyless Public API

Ambos caminos viven en `pro-api.coinmarketcap.com`:

| Tipo | Base URL | Prefijo | Uso |
|------|----------|---------|-----|
| **Keyless Public API** | `https://pro-api.coinmarketcap.com/public-api` | `/public-api` | Principal (este skill) |
| **Trial Pro API** | `https://pro-api.coinmarketcap.com/trial-pro-api` | `/trial-pro-api` | Evaluación; fuera de scope v1 del skill |

### Reglas Keyless Public API

- Prefijo `/public-api` antes del endpoint normal.
- Solo **GET**.
- **No enviar** `X-CMC_PRO_API_KEY`.
- Formato de respuesta igual al de la versión keyed.
- Muchos endpoints (incl. algunos históricos) soportan keyless.

### Endpoints disponibles (Keyless)

**Standard API (ejemplos):**

- `/v1/cryptocurrency/map`
- `/v3/cryptocurrency/listings/latest`
- `/v3/cryptocurrency/quotes/latest`
- `/v2/cryptocurrency/info`
- `/v1/global-metrics/quotes/latest`
- `/v2/tools/price-conversion`
- `/v1/cryptocurrency/categories`
- `/v3/fear-and-greed/latest` y `/historical`
- Índices CMC100 / CMC20 (latest + historical)
- Altcoin Season Index

**DEX API (ejemplos):**

- `/v4/dex/spot-pairs/latest`
- `/v4/dex/pairs/quotes/latest`
- `/v1/dex/token`, `/v1/dex/token/price`, `/v1/dex/search`

### Ejemplos

```bash
curl -s "https://pro-api.coinmarketcap.com/public-api/v1/simple/price?ids=1,1027&convert=USD" | jq '.'

curl -s "https://pro-api.coinmarketcap.com/public-api/v3/cryptocurrency/listings/latest?limit=10" | jq '.'

curl -s "https://pro-api.coinmarketcap.com/public-api/v3/fear-and-greed/latest" | jq '.'

curl -s "https://pro-api.coinmarketcap.com/public-api/v2/tools/price-conversion?amount=100&symbol=BTC&convert=USD,ARS" | jq '.'
```

### Limitaciones Keyless CMC

- Rate limit más agresivo que con API key (por IP).
- No todos los endpoints están en keyless (históricos profundos a menudo no).
- No recomendado para producción o polling frecuente.
- Ideal para: prototipado, pruebas de respuesta, agentes/LLMs, evaluación rápida.

**Docs oficiales:**

- [Keyless Public API - CoinMarketCap](https://coinmarketcap.com/api/documentation/pro-api-reference/keyless-public-api)
- [Trial Pro API](https://coinmarketcap.com/api/documentation/pro-api-reference/trial-pro-api)

## Comparación: Keyless CoinGecko vs CoinMarketCap

| Característica | CoinGecko Keyless | CoinMarketCap Keyless | Preferencia práctica |
|----------------|-------------------|------------------------|----------------------|
| Facilidad | Excelente (sin nada) | Buena (`/public-api`) | CoinGecko |
| Cantidad de endpoints | 50+ + 20 onchain | ~18 Standard + 17 DEX | CoinGecko |
| Histórico keyless | Bueno (~1 año en muchos casos) | Limitado | CoinGecko |
| Onchain / DEX | Excelente (GeckoTerminal) | Bueno | CoinGecko |
| Rate limit | ~10–30/min | Más agresivo | CoinGecko |
| Consistencia de respuesta | Muy buena | Excelente (mismo formato keyed) | CMC |
| Prototipado | Muy fuerte | Fuerte | CoinGecko |
| Producción | No | No | — |

## Recomendaciones de uso

### Usar keyless cuando

- Prototipás o testeás endpoints
- Integrás datos rápido en script, notebook o agente
- Armás un proyecto open source o educativo
- Querés evitar registración inicial

### Pasar a API Key (Demo/Basic) cuando

- Necesitás rate limits más altos y estables
- Hacés polling frecuente o producción
- Querés tracking de uso y cuotas
- El volumen del proyecto crece

### Buenas prácticas

1. **Caching**: cacheá respuestas aunque sea keyless.
2. **Exponential backoff**: reintentos ante `429`.
3. **Fallback**: en proyectos reales, keyless + Demo/Basic como fallback (fuera de scope v1 de este skill).
4. **Combinar fuentes**: CoinGecko para precios/histórico; CMC para rankings, Fear & Greed e índices.

## Fuentes oficiales

- CoinGecko Keyless: https://docs.coingecko.com/docs/keyless-public-api
- CoinGecko Demo Endpoints: https://docs.coingecko.com/demo/reference/endpoint-overview
- CoinMarketCap Keyless: https://coinmarketcap.com/api/documentation/pro-api-reference/keyless-public-api
- CoinMarketCap Trial Pro: https://coinmarketcap.com/api/documentation/pro-api-reference/trial-pro-api
- CoinMarketCap Pricing: https://pro.coinmarketcap.com/pricing
- CoinGecko Pricing: https://www.coingecko.com/en/api/pricing

Nota: los rate limits pueden variar según carga del servidor. Verificá dashboards Demo/Basic para valores actuales si usás cuenta keyed.
