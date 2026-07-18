# Ripio wFiat — Token Reference

Canonical identities for Ripio wrapped LATAM fiat stablecoins (wFiat).
Verified against CoinGecko keyless API (Jul 2026).

Issuer: [Ripio — Stablecoins locales](https://www.ripio.com/es/criptos/stablecoins-locales)

## Shared properties

- **Decimals**: 18
- **Type**: wrapped / local-fiat stablecoin (Ripio)
- **Address pattern**: same contract address listed on multiple EVM chains in CoinGecko
- **Price API**: CoinGecko id (slug), not ticker alone
- **Price display**: always invert — show fiat per 1 USD (e.g. `USD/ARS`), not "1 wFiat = X USD"
- **CMC**: avoid symbol-only lookups (collision risk)

### Platforms (all six tokens)

| CoinGecko platform key | Common name |
|------------------------|-------------|
| `ethereum` | Ethereum |
| `base` | Base |
| `world-chain` | World Chain |
| `binance-smart-chain` | BNB Smart Chain |
| `polygon-pos` | Polygon |
| `xdai` | Gnosis |

Crosswalk to GeckoTerminal network ids and Uniswap app slugs: see "Chain
crosswalk" in `SKILL.md`.

### Known extra deployment not yet on CoinGecko

**Celo** — verified onchain (Jul 2026) via `eth_call` to `symbol()` on the
canonical wARS address against a public RPC (`forno.celo.org`); returns
`wARS` at the same address as every other chain. CoinGecko does not list
`celo` as a platform yet and there's no pool there as of this writing — see
"Detecting a deployment CoinGecko hasn't listed yet" in `SKILL.md` for the
verification recipe. Not added to the canonical registry table above since
CoinGecko's platform list is this skill's identity source of truth (see
Identity rules) — treat this as a heads-up, re-verify before relying on it.

## Tokens

### wARS — Argentine Peso

| Field | Value |
|-------|-------|
| Symbol | wARS |
| Fiat | ARS |
| CoinGecko id | `argentine-peso` |
| Address | `0x0dc4f92879b7670e5f4e4e6e3c801d229129d90d` |
| Page | https://www.coingecko.com/en/coins/argentine-peso |

```bash
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=argentine-peso&vs_currencies=usd,ars" | jq '.'
```

### wBRL — Brazilian real

| Field | Value |
|-------|-------|
| Symbol | wBRL |
| Fiat | BRL |
| CoinGecko id | `brazilian-real` |
| Address | `0xd76f5faf6888e24d9f04bf92a0c8b921fe4390e0` |
| Page | https://www.coingecko.com/en/coins/brazilian-real |

```bash
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=brazilian-real&vs_currencies=usd,brl" | jq '.'
```

### wMXN — Mexican Peso

| Field | Value |
|-------|-------|
| Symbol | wMXN |
| Fiat | MXN |
| CoinGecko id | `mexican-peso` |
| Address | `0x337e7456b420bd3481e7fa61fa9850343d610d34` |
| Page | https://www.coingecko.com/en/coins/mexican-peso |

```bash
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=mexican-peso&vs_currencies=usd,mxn" | jq '.'
```

### wCOP — Colombian Peso

| Field | Value |
|-------|-------|
| Symbol | wCOP |
| Fiat | COP |
| CoinGecko id | `colombian-peso` |
| Address | `0x8a1d45e102e886510e891d2ec656a708991e2d76` |
| Page | https://www.coingecko.com/en/coins/colombian-peso |

```bash
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=colombian-peso&vs_currencies=usd" | jq '.'
```

### wPEN — Peruvian Sol

| Field | Value |
|-------|-------|
| Symbol | wPEN |
| Fiat | PEN |
| CoinGecko id | `peruvian-sol` |
| Address | `0x4f34c8b3b5fb6d98da888f0fea543d4d9c9f2ebe` |
| Page | https://www.coingecko.com/en/coins/peruvian-sol |

```bash
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=peruvian-sol&vs_currencies=usd" | jq '.'
```

### wCLP — Chilean Peso

| Field | Value |
|-------|-------|
| Symbol | wCLP |
| Fiat | CLP |
| CoinGecko id | `chilean-peso` |
| Address | `0x61d450a098b6a7f69fc4b98ce68198fe59768651` |
| Page | https://www.coingecko.com/en/coins/chilean-peso |

```bash
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=chilean-peso&vs_currencies=usd" | jq '.'
```

## Batch price (all wFiat)

```bash
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=argentine-peso,brazilian-real,mexican-peso,colombian-peso,peruvian-sol,chilean-peso&vs_currencies=usd,ars,brl,mxn&include_last_updated_at=true" | jq '.'
```

Invert for presentation (fiat per 1 USD):

```bash
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=argentine-peso,brazilian-real,mexican-peso,colombian-peso,peruvian-sol,chilean-peso&vs_currencies=usd" \
  | jq 'to_entries | map({symbol: .key, pair: ("USD/" + (if .key == "argentine-peso" then "ARS" elif .key == "brazilian-real" then "BRL" elif .key == "mexican-peso" then "MXN" elif .key == "colombian-peso" then "COP" elif .key == "peruvian-sol" then "PEN" else "CLP" end)), rate: (1 / .value.usd)})'
```

## GeckoTerminal helpers

Token pools (replace `{network}` and `{address}`):

```bash
curl -s "https://api.geckoterminal.com/api/v2/networks/{network}/tokens/{address}/pools" | jq '.'
```

Examples:

```bash
# wARS on Base
curl -s "https://api.geckoterminal.com/api/v2/networks/base/tokens/0x0dc4f92879b7670e5f4e4e6e3c801d229129d90d/pools" | jq '.'

# wBRL on Ethereum
curl -s "https://api.geckoterminal.com/api/v2/networks/eth/tokens/0xd76f5faf6888e24d9f04bf92a0c8b921fe4390e0/pools" | jq '.'
```

## Uniswap v4 subgraph snippet

Use lowercase address. Mainnet gateway id:
`DiYPVdygkfjDWhbxGSqAQxwBKmfKnkWQojqeM2rkLb3G` (see skill `uniswap-v4-subgraph`).

```graphql
{
  token(id: "0x0dc4f92879b7670e5f4e4e6e3c801d229129d90d") {
    symbol
    name
    decimals
    volumeUSD
    poolCount
    totalValueLockedUSD
  }
}
```

```graphql
{
  pools(
    first: 10
    orderBy: volumeUSD
    orderDirection: desc
    where: {
      or: [
        { token0: "0x0dc4f92879b7670e5f4e4e6e3c801d229129d90d" }
        { token1: "0x0dc4f92879b7670e5f4e4e6e3c801d229129d90d" }
      ]
    }
  ) {
    id
    feeTier
    liquidity
    volumeUSD
    hooks
    token0 { symbol }
    token1 { symbol }
  }
}
```

## Quick lookup (symbol → CoinGecko id)

| Symbol | CoinGecko id |
|--------|--------------|
| wARS | argentine-peso |
| wBRL | brazilian-real |
| wMXN | mexican-peso |
| wCOP | colombian-peso |
| wPEN | peruvian-sol |
| wCLP | chilean-peso |

## Related skills

- `coingecko-and-coinmarketcap-apis` — keyless price/markets/DEX HTTP APIs
- `uniswap-v4-subgraph` — GraphQL pools/swaps/positions
- `crypto-prices-criptoya` — CEX/P2P quotes (not the wrapped token registry)
