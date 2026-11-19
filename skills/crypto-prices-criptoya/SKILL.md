---
name: crypto-prices-criptoya
description: >
  Consulta cotizaciones de criptomonedas con CriptoYa por exchange y en forma agregada.
  Usar cuando el usuario pida "precio BTC en ARS", "cotizacion USDT", "precio ETH en USD",
  "mejor precio por exchange", "comparar exchanges", "precio en belo/ripio/lemon/binance/bybit",
  o cuando pida comisiones de retiro y fees por red.
---

# Crypto Prices CriptoYa

Consulta cotizaciones cripto de CriptoYa por exchange, cotizacion general y comisiones de retiro.

## API Overview

- **Base URL**: `https://criptoya.com`
- **Auth**: None required
- **Response format**: JSON en respuestas validas
- **Nota operativa (errores "Invalid pair")**: el formato depende de la ruta y del motivo:
  - Ruta agregada `/api/{coin}/{fiat}/{volumen}` con coin o fiat inexistente (ej. `/api/FOO/ARS/1`): HTTP `404` con JSON `{"error":"Invalid pair"}`.
  - Ruta por exchange `/api/{exchange}/{coin}/{fiat}/{volumen}` con exchange inexistente o que no cotiza ese par (ej. `/api/airtm/USDT/ARS/1`, `/api/belo/BTC/CLP/1`): HTTP `200` con texto plano `Invalid pair` (no JSON).
  - Ruta por exchange con coin inexistente (ej. `/api/belo/FOO/ARS/1`): HTTP `404` con JSON `{"error":"Invalid pair"}`.
- **Timestamp**: campo `time` en unix epoch en **segundos**

## Endpoints

- `GET /api/{exchange}/{coin}/{fiat}/{volumen}`
- `GET /api/{coin}/{fiat}/{volumen}`
- `GET /api/fees`
- `GET /api/exchanges` (lista de exchanges por pais; fuente de verdad para `exchange`)

Ejemplos:

```bash
curl -s "https://criptoya.com/api/BTC/ARS/0.1" | jq '.'
curl -s "https://criptoya.com/api/belo/BTC/ARS/0.1" | jq '.'
curl -s "https://criptoya.com/api/fees" | jq '.'
curl -s "https://criptoya.com/api/exchanges" | jq '.ar'
# Mejor ask/bid (ignora ask/bid <= 0 y cotizaciones con time > 24h)
curl -s "https://criptoya.com/api/USDT/ARS/1" | jq --argjson now "$(date +%s)" '
  to_entries
  | map(select(.value.time > ($now - 86400)))
  | { mejor_ask: (map(select(.value.totalAsk > 0)) | min_by(.value.totalAsk) | {exchange:.key, totalAsk:.value.totalAsk, time:.value.time}),
      mejor_bid: (map(select(.value.totalBid > 0)) | max_by(.value.totalBid) | {exchange:.key, totalBid:.value.totalBid, time:.value.time}) }'
```

## Valores admitidos

### `coin`

Verificadas contra ARS (lista no exhaustiva; la disponibilidad cambia y varia por fiat):

`BTC, ETH, USDT, USDC, DAI, WLD, BNB, SOL, XRP, ADA, AVAX, DOGE, TRX, LINK, DOT, POL, SHIB, LTC, BCH, XLM, AAVE, UNI, ALGO, PAXG, CAKE`

- Usar `POL` (no `MATIC`).
- Ya no cotizan contra ARS (HTTP `404`): `MATIC, FTM, UXD, SLP, EOS, USDP, BAT, AXS, MANA, SAND, CHZ`.
- Ante una coin no listada, probar la ruta agregada y tratar `404` como no soportada.

### `fiat`

`ARS, BRL, CLP, COP, MXN, PEN, VES, BOB, UYU, DOP, PYG, USD, EUR`

### `exchange`

Fuente de verdad: `GET https://criptoya.com/api/exchanges` devuelve un objeto pais -> lista de exchanges (`ar`, `br`, `cl`, `co`, `mx`, `pe`, `uy`, `bo`, `py`, `ve`, `eu`, ...). Consultarlo cuando haya dudas; la lista cambia.

Argentina (`.ar`, snapshot verificado):

`airtm, astropay, belo, binance, binancep2p, bingxp2p, bitgetp2p, bitso, bitsoalpha, bybit, bybitp2p, cocoscrypto, cryptomkt, cryptomktpro, decrypto, dolarapp, eldoradop2p, fiwind, huobip2p, kucoinp2p, lemoncash, lemoncashp2p, letsbit, mexc, mexcp2p, nexo, okexp2p, p2pme, peanut, ripio, ripioexchange, saldo, satoshitango, takenos, tiendacrypto, universalcoins, vibrant, vitawallet, wallbit, weexp2p`

- Que un exchange figure no garantiza que cotice todo par: hoy `airtm` y `vibrant` estan en `.ar` pero no cotizan `USDT/ARS` (`Invalid pair`).
- Otros paises suman exchanges propios (ej. `xapo`, `buda`, `foxbit`, `mercadobitcoin`, `kucoin`, `bitget`); `xapo` no cotiza en ARS.
- No figuran en `/api/exchanges` y devuelven `Invalid pair`: `eluter`, `buenbit`, `paydecep2p`, `trubit`, `pluscrypto`, `coinexp2p`.
- `kraken` aparece en `/api/fees` pero no en `/api/exchanges` (no tiene cotizacion).

### `volumen`

Numero decimal usando punto: `0.1`, `1`, `250.5`.

## Campos clave

- Cotizacion por exchange:
  - `ask`, `totalAsk`, `bid`, `totalBid`, `time`
- Cotizacion general:
  - Objeto por exchange con los mismos campos (`ask`, `totalAsk`, `bid`, `totalBid`, `time`)
- Fees:
  - Estructura anidada `exchange -> coin -> red -> {withdraw, time}`
  - `withdraw` = comision de retiro en unidades de la coin (no hay campo `fee`); `time` en epoch segundos (puede venir `0`)
  - Ej.: `curl -s "https://criptoya.com/api/fees" | jq '.belo.USDT'`

## Workflow

1. Detectar intencion:
   - Cotizacion general
   - Cotizacion por exchange
   - Fees de retiro
2. Validar inputs requeridos:
   - `coin`, `fiat`, `volumen`
   - `exchange` cuando aplique
3. Ejecutar `curl -s` y parsear con `jq`.
4. Si la respuesta es `Invalid pair` (texto plano HTTP `200` o JSON `{"error":"Invalid pair"}` HTTP `404`) o no es JSON esperado, informar parametros invalidos.
5. Antes de calcular mejores precios, descartar filas invalidas:
   - `ask`/`totalAsk` <= 0 para el mejor ask, y `bid`/`totalBid` <= 0 para el mejor bid (ej. `huobip2p` o `weexp2p` pueden venir con `0`).
   - Cotizaciones con `time` viejo (ej. mas de 24h: `time < now - 86400`, en segundos).
6. Presentar primero resumen accionable:
   - Mejor `bid`
   - Mejor `ask`
   - Spread relevante
7. Presentar detalle:
   - Top exchanges y `time` por cotizacion

## Error Handling

- **Parametro invalido / par no soportado**:
  - Ruta por exchange: detectar texto plano `Invalid pair` aunque HTTP sea `200` (exchange inexistente o par no cotizado).
  - Ruta agregada (y coin inexistente en ruta por exchange): HTTP `404` con JSON `{"error":"Invalid pair"}`.
  - Informar claramente que la combinacion solicitada no esta soportada.
- **Red/timeout**:
  - Reintentar hasta 2 veces con espera corta.
  - Si falla, devolver mensaje claro con endpoint consultado.
- **JSON inesperado**:
  - Mostrar minimo crudo util y aclarar inconsistencia del origen.

## Presenting Results

- Priorizar:
  - Mejor precio de compra (`ask`)
  - Mejor precio de venta (`bid`)
  - Spread (`ask - bid`) por exchange
  - Ignorar en "mejor precio" las filas con `ask`/`bid` <= 0 o con `time` de mas de 24h; si se muestran en la tabla, marcarlas como "sin cotizacion" / "desactualizada"
- En comparativas:
  - Tabla corta por exchange con `ask`, `bid`, `totalAsk`, `totalBid`, `time`
- Aclarar:
  - Datos informativos y sin recomendacion financiera

## Out of Scope

Esta skill no debe usar en v1:

- `/api/dolar`
- `/api/cer`
- `/api/uva`
- `/api/bancostodos`
