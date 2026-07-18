---
name: ripio-wfiat
description: >
  Canonical registry and recipes for Ripio wFiat LATAM stablecoins (wARS, wBRL,
  wMXN, wCOP, wPEN, wCLP): contract addresses, CoinGecko ids, chains, and how to
  query prices/DEX via CoinGecko, GeckoTerminal, and Uniswap v4 subgraph.
  Always present wFiat prices inverted (fiat per 1 USD, e.g. USD/ARS).
  Use when the user mentions "wARS", "wBRL", "wMXN", "wCOP", "wPEN", "wCLP",
  "wfiat", "wFiat", "Ripio stablecoin", "stablecoin local Ripio", "peso wrapeado",
  "wrapped ARS/BRL/MXN/COP/PEN/CLP", or asks for addresses/prices/pools of these tokens.
---

# Ripio wFiat

Registry + recipes for Ripio **wFiat** (wrapped LATAM fiat stablecoins). This
skill is the source of truth for identity; for full API mechanics load
`coingecko-and-coinmarketcap-apis` and/or `uniswap-v4-subgraph`.

Issuer docs: https://www.ripio.com/es/criptos/stablecoins-locales

Token detail tables and extra curl samples: `references/tokens.md`.

## Canonical Registry

Same contract address per token across listed EVM chains (18 decimals). Prefer
**lowercase** addresses in GraphQL/`where` filters.

| Symbol | Fiat | CoinGecko id | Address | CoinGecko page |
|--------|------|--------------|---------|----------------|
| **wARS** | ARS | `argentine-peso` | `0x0dc4f92879b7670e5f4e4e6e3c801d229129d90d` | [link](https://www.coingecko.com/en/coins/argentine-peso) |
| **wBRL** | BRL | `brazilian-real` | `0xd76f5faf6888e24d9f04bf92a0c8b921fe4390e0` | [link](https://www.coingecko.com/en/coins/brazilian-real) |
| **wMXN** | MXN | `mexican-peso` | `0x337e7456b420bd3481e7fa61fa9850343d610d34` | [link](https://www.coingecko.com/en/coins/mexican-peso) |
| **wCOP** | COP | `colombian-peso` | `0x8a1d45e102e886510e891d2ec656a708991e2d76` | [link](https://www.coingecko.com/en/coins/colombian-peso) |
| **wPEN** | PEN | `peruvian-sol` | `0x4f34c8b3b5fb6d98da888f0fea543d4d9c9f2ebe` | [link](https://www.coingecko.com/en/coins/peruvian-sol) |
| **wCLP** | CLP | `chilean-peso` | `0x61d450a098b6a7f69fc4b98ce68198fe59768651` | [link](https://www.coingecko.com/en/coins/chilean-peso) |

### Chains (CoinGecko platforms)

For each token, CoinGecko lists the **same address** on:

- `ethereum`
- `base`
- `world-chain`
- `binance-smart-chain` (BSC)
- `polygon-pos`
- `xdai` (Gnosis)

Default when the user does not specify a chain: **Ethereum**, then Base.

### Identity rules

- CoinGecko **id** (slug) is authoritative for prices — not the ticker alone.
- Do **not** look up CMC by symbol `WARS` / `WBRL` alone (collisions exist, e.g. MetaWars). Prefer CoinGecko for wFiat.
- Addresses are case-insensitive; normalize to lowercase for subgraph queries.
- These are **informational** market tokens, not financial advice.

### Price display (inverted)

**Always invert wFiat prices when presenting them.** CoinGecko returns how much USD (or another fiat) one wFiat token is worth; in LATAM it is more natural to show **how much local fiat equals 1 USD** (e.g. "1 USD = 1.450 ARS", not "1 wARS = $0,00069").

| API field | Raw meaning | Present as |
|-----------|-------------|------------|
| `.usd` | 1 wFiat in USD | **1 USD = 1/price_usd {FIAT}** |
| vs other fiat | 1 wFiat in X | **1 {reference} = 1/price {FIAT}** when useful |

Examples:

- wARS `usd: 0.00069` → **1 USD ≈ 1.449 ARS**
- wBRL `usd: 0.18` → **1 USD ≈ 5,56 BRL**
- wMXN `usd: 0.058` → **1 USD ≈ 17,24 MXN**

Rounding: integers (or 0 decimals) for ARS, COP, CLP; 2–4 decimals for BRL, MXN, PEN. Always label the pair explicitly (`USD/ARS`, `USD/BRL`, etc.).

```bash
# Invert CoinGecko USD quote → fiat per 1 USD (wARS example)
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=argentine-peso&vs_currencies=usd" \
  | jq '.["argentine-peso"].usd as $p | { pair: "USD/ARS", rate: (1 / $p) }'
```

## Recipe map — which skill / API

| Intent | Use | Key input |
|--------|-----|-----------|
| Spot / multi-fiat price | CoinGecko keyless (`coingecko-and-coinmarketcap-apis`) | CoinGecko `id` |
| Token markets / detail | CoinGecko `/coins/{id}` | CoinGecko `id` |
| DEX pools / OHLCV onchain | GeckoTerminal | network + token address |
| Uniswap v4 pools / swaps / TVL | `uniswap-v4-subgraph` | token address (lowercase) + chain deployment |
| CEX quotes ARS/BRL vs BTC/USDT | `crypto-prices-criptoya` (optional) | different product; not the wrapped token itself |

## Recipes

### 1) Price all wFiat (CoinGecko keyless)

```bash
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=argentine-peso,brazilian-real,mexican-peso,colombian-peso,peruvian-sol,chilean-peso&vs_currencies=usd,ars,brl,mxn&include_last_updated_at=true" | jq '.'
```

### 2) Single token price

```bash
# wARS
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=argentine-peso&vs_currencies=usd,ars" | jq '.'

# wBRL
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=brazilian-real&vs_currencies=usd,brl" | jq '.'
```

### 3) Coin detail (platforms, market data)

```bash
curl -s "https://api.coingecko.com/api/v3/coins/argentine-peso?localization=false&tickers=false&community_data=false&developer_data=false" \
  | jq '{id, symbol, name, contract_address, platforms, price: .market_data.current_price.usd}'
```

### 4) GeckoTerminal token pools (example: Base wARS)

```bash
curl -s "https://api.geckoterminal.com/api/v2/networks/base/tokens/0x0dc4f92879b7670e5f4e4e6e3c801d229129d90d/pools" | jq '.'
```

Network names commonly used: `eth`, `base`, `bsc`, `polygon_pos`, `xdai`, `world-chain` (confirm against GeckoTerminal if empty).

### 5) Uniswap v4 subgraph — token + pools (Ethereum mainnet)

Requires `$THEGRAPH_API_KEY`. Follow `uniswap-v4-subgraph` for auth and endpoint.

```bash
ENDPOINT="https://gateway.thegraph.com/api/${THEGRAPH_API_KEY}/subgraphs/id/DiYPVdygkfjDWhbxGSqAQxwBKmfKnkWQojqeM2rkLb3G"
TOKEN="0x0dc4f92879b7670e5f4e4e6e3c801d229129d90d"  # wARS

curl -s "$ENDPOINT" \
  -H 'Content-Type: application/json' \
  -d "{\"query\":\"{ token(id: \\\"${TOKEN}\\\") { id symbol name decimals volumeUSD poolCount totalValueLockedUSD } pools(first: 10, orderBy: volumeUSD, orderDirection: desc, where: { or: [{ token0: \\\"${TOKEN}\\\" }, { token1: \\\"${TOKEN}\\\" }] }) { id feeTier liquidity volumeUSD hooks token0 { symbol } token1 { symbol } } }\"}" \
  | jq '.'
```

Swap `TOKEN` for any other wFiat address from the registry. For non-Ethereum chains, use the matching Uniswap v4 subgraph deployment from The Graph Explorer (see `uniswap-v4-subgraph`).

## Workflow

1. Resolve symbol → registry row (address + CoinGecko id + fiat).
2. If chain missing, default to Ethereum (mention the assumption).
3. Choose recipe by intent (price vs DEX vs Uniswap).
4. Execute `curl` + `jq`; on `429` backoff (CoinGecko/GeckoTerminal rate limits).
5. Present: symbol, fiat peg, address, chain, **inverted** price (and pool summary if DEX).
6. Cross-load API skills only when deeper endpoint docs are needed.

## Presenting Results

Lead with a compact card per token:

- Symbol / fiat / CoinGecko id
- Address + chain(s)
- **Inverted price**: fiat per 1 USD (e.g. `USD/ARS 1.449`, `USD/BRL 5,56`) — never lead with "1 wFiat = X USD"
- Optional: top pool / TVL if onchain query was run

Clarify data is informational; no investment advice.

## Out of Scope

- Mint/redeem / Ripio app account flows
- Treating CMC symbol search as authoritative for wFiat
- Non-Ripio “ARS”/“BRL” tokens with different addresses
- Full Uniswap/CoinGecko schema docs (use sibling skills)

## Reference

Per-token detail: [references/tokens.md](references/tokens.md)
