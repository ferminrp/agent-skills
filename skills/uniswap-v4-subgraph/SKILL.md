---
name: uniswap-v4-subgraph
description: >
  Query Uniswap v4 analytics via The Graph subgraph GraphQL API: poolManager
  metrics, pool state, swaps, tokens, positions, and day/hour aggregates.
  Use when the user asks for Uniswap v4 pools, liquidity, volume, TVL, recent
  swaps, hooks, positions by NFT tokenId, poolDayData, or mentions "Uniswap v4
  subgraph", "The Graph Uniswap v4", or v4 PoolManager queries.
---

# Uniswap v4 Subgraph

Query Uniswap v4 onchain-indexed data through The Graph decentralized network
GraphQL API. Hosted service endpoints are deprecated; use the gateway URL with
a Studio API key.

For expanded query examples and entity field tables, read
`references/v4-queries.md`.

## API Overview

- **Protocol**: GraphQL over HTTPS (POST)
- **Mainnet explorer**: [DiYPVdygkfjDWhbxGSqAQxwBKmfKnkWQojqeM2rkLb3G](https://thegraph.com/explorer/subgraphs/DiYPVdygkfjDWhbxGSqAQxwBKmfKnkWQojqeM2rkLb3G?view=Query&chain=arbitrum-one)
- **GraphQL endpoint template**:
  `https://gateway.thegraph.com/api/<THEGRAPH_API_KEY>/subgraphs/id/DiYPVdygkfjDWhbxGSqAQxwBKmfKnkWQojqeM2rkLb3G`
- **Auth**: API key from [The Graph Studio](https://thegraph.com/studio/apikeys/)
- **Schema / code**: [Uniswap/v4-subgraph](https://github.com/Uniswap/v4-subgraph)
- **Docs**: [v4 Queries](https://developers.uniswap.org/docs/ecosystem/subgraphs/concepts/v4/queries), [v4 Query Examples](https://developers.uniswap.org/docs/ecosystem/subgraphs/guides/v4-query-examples), [Subgraphs Overview](https://developers.uniswap.org/docs/ecosystem/subgraphs/overview)

### Auth setup

```bash
export THEGRAPH_API_KEY="..."
# key from https://thegraph.com/studio/apikeys/
```

Never hardcode the key. Prefer `$THEGRAPH_API_KEY` from the environment.

### Reliability note

Public explorer links and gateway IDs in Uniswap docs are **example community
deployments**, not guaranteed official Uniswap Labs production indexers. Before
relying on data: confirm the deployment is actively indexed, schema matches
expectations, and chain/contracts align. For production, prefer deploying from
the official [v4-subgraph](https://github.com/Uniswap/v4-subgraph) repo.

## Key Differences from v3

- Query global metrics from `poolManager`, not `factory`.
- Pool `id` is a **bytes32 hash** of the pool key (tokens, fee, tick spacing,
  hooks) — not a deployed pool contract address.
- Pool entities include `hooks` (hook contract address, if any).
- Positions track `subscriptions`, `unsubscriptions`, and `transfers` (not the
  v3 mint/burn/collect position model).

## PoolManager IDs

Ethereum mainnet (and docs examples) use:

`0x000000000004444c5dc75cb358380d2e3de08a90`

Other chains use **different** PoolManager addresses. Resolve them from
[v4 Deployments](https://developers.uniswap.org/docs/protocols/v4/deployments)
or `networks.json` in the subgraph repo. Always lowercase hex IDs in queries
when the deployment expects checksum-insensitive IDs.

## Core Entities

| Entity | Use for |
|--------|---------|
| `PoolManager` | Protocol-wide pool count, tx count, volume, TVL, fees |
| `Pool` | Liquidity, sqrtPrice, tick, feeTier, hooks, volume |
| `Token` | Symbol/name/decimals and aggregates across v4 pools |
| `Swap` | Individual swaps (amounts, sender, timestamp) |
| `Position` | NFT `tokenId` positions + subscribe/transfer events |
| `PoolDayData` / `PoolHourData` | Pool time-series |
| `TokenDayData` / `TokenHourData` | Token time-series |
| `ModifyLiquidity` | Liquidity add/remove events |

## Common Queries

### Protocol metrics

```graphql
{
  poolManager(id: "0x000000000004444c5dc75cb358380d2e3de08a90") {
    poolCount
    txCount
    totalVolumeUSD
    totalVolumeETH
    totalValueLockedUSD
  }
}
```

### Pool state

```graphql
{
  pool(id: "0x21c67e77068de97969ba93d4aab21826d33ca12bb9f565d8496e8fda8a82ca27") {
    token0 { symbol id decimals }
    token1 { symbol id decimals }
    feeTier
    liquidity
    sqrtPrice
    tick
    hooks
    volumeUSD
    totalValueLockedUSD
  }
}
```

### Most liquid pools

```graphql
{
  pools(first: 100, orderBy: liquidity, orderDirection: desc) {
    id
    token0 { symbol }
    token1 { symbol }
    feeTier
    liquidity
    volumeUSD
    hooks
  }
}
```

### Recent swaps in a pool

```graphql
{
  swaps(
    first: 20
    orderBy: timestamp
    orderDirection: desc
    where: { pool: "0x21c67e77068de97969ba93d4aab21826d33ca12bb9f565d8496e8fda8a82ca27" }
  ) {
    sender
    origin
    amount0
    amount1
    amountUSD
    timestamp
  }
}
```

### Token aggregates

```graphql
{
  token(id: "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984") {
    symbol
    name
    decimals
    volumeUSD
    poolCount
    totalValueLockedUSD
  }
}
```

### Position by NFT tokenId

```graphql
{
  position(id: "3") {
    id
    tokenId
    owner
    subscriptions { id }
    unsubscriptions { id }
    transfers { id }
  }
}
```

### Pool daily series

```graphql
{
  poolDayDatas(
    first: 10
    orderBy: date
    where: {
      pool: "0x21c67e77068de97969ba93d4aab21826d33ca12bb9f565d8496e8fda8a82ca27"
      date_gt: 1735689600
    }
  ) {
    date
    liquidity
    sqrtPrice
    token0Price
    token1Price
    volumeToken0
    volumeToken1
  }
}
```

### Historical (time-travel) at a block

```graphql
{
  poolManager(
    id: "0x000000000004444c5dc75cb358380d2e3de08a90"
    block: { number: 22451931 }
  ) {
    poolCount
    totalVolumeUSD
  }
}
```

## How to Call (curl)

```bash
ENDPOINT="https://gateway.thegraph.com/api/${THEGRAPH_API_KEY}/subgraphs/id/DiYPVdygkfjDWhbxGSqAQxwBKmfKnkWQojqeM2rkLb3G"

curl -s "$ENDPOINT" \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ poolManager(id: \"0x000000000004444c5dc75cb358380d2e3de08a90\") { poolCount txCount totalVolumeUSD } }"}' \
  | jq '.'
```

Alternate auth style used by some clients:

```bash
curl -s "https://gateway.thegraph.com/api/subgraphs/id/DiYPVdygkfjDWhbxGSqAQxwBKmfKnkWQojqeM2rkLb3G" \
  -H "Authorization: Bearer ${THEGRAPH_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ pools(first: 5, orderBy: liquidity, orderDirection: desc) { id liquidity } }"}' \
  | jq '.'
```

## Pagination

The Graph caps results at **1000** per request. Use `first` + `skip`:

```graphql
{
  pools(first: 1000, skip: 0, orderBy: liquidity, orderDirection: desc) {
    id
  }
}
```

Increment `skip` by 1000 until fewer than 1000 rows return.

## Workflow

1. Confirm intent: global metrics, pool state, swaps, token, position, or day data.
2. Ensure `$THEGRAPH_API_KEY` is set; if missing, ask the user to create one in Studio.
3. Pick the correct subgraph deployment for the chain (mainnet ID above; discover others in The Graph Explorer).
4. Use the chain-correct `poolManager` id and pool **bytes32** ids (not v3 pool addresses).
5. POST GraphQL with `curl` and parse with `jq`.
6. If more than 1000 rows are needed, paginate with `skip`.
7. Present a short snapshot first (counts, top pools, latest swaps), then detail.
8. Treat data as informational; do not give investment advice.

## Error Handling

- **Missing / invalid API key** (`401`/`403`): remind user to set `THEGRAPH_API_KEY` from Studio.
- **GraphQL `errors` array**: show message; usually bad field, bad id, or schema mismatch.
- **Empty `data` / null entity**: wrong chain deployment, wrong PoolManager id, or unknown pool/token id.
- **Timeouts / 429**: backoff and retry 1–2 times; avoid tight polling loops.
- **Stale or inconsistent TVL**: public deployments can lag or disagree with app.uniswap.org; state the source deployment id used.

## Presenting Results

- Global: `poolCount`, `txCount`, `totalVolumeUSD`, `totalValueLockedUSD`.
- Pools: pair symbols, `feeTier`, `liquidity`, `volumeUSD`, `hooks`.
- Swaps: amounts, `amountUSD`, `timestamp`, `sender`/`origin`.
- Positions: `tokenId`, `owner`, subscription/transfer counts.
- Always cite chain + subgraph id when summarizing.

## Out of Scope

This skill does not cover in v1:

- Uniswap v2 / v3 subgraphs (separate deployments)
- Onchain contract calls / SDK swaps (Universal Router, Permit2)
- Private Uniswap Labs indexers used by the official app
- Deploying or maintaining a subgraph (point to the GitHub repo only)

## Reference

Expanded examples and entity tables: [references/v4-queries.md](references/v4-queries.md)
