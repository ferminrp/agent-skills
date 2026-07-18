# Uniswap v4 Subgraph — Queries and Entities Reference

Derived from official Uniswap docs (v4 Queries, v4 Query Examples, Subgraphs
Overview) and the [v4-subgraph schema](https://github.com/Uniswap/v4-subgraph/blob/main/schema.graphql).

## Endpoint

| Item | Value |
|------|-------|
| Network | The Graph decentralized gateway |
| Mainnet subgraph id | `DiYPVdygkfjDWhbxGSqAQxwBKmfKnkWQojqeM2rkLb3G` |
| URL | `https://gateway.thegraph.com/api/<API_KEY>/subgraphs/id/DiYPVdygkfjDWhbxGSqAQxwBKmfKnkWQojqeM2rkLb3G` |
| Explorer | https://thegraph.com/explorer/subgraphs/DiYPVdygkfjDWhbxGSqAQxwBKmfKnkWQojqeM2rkLb3G |
| API keys | https://thegraph.com/studio/apikeys/ |
| Source | https://github.com/Uniswap/v4-subgraph |

Hosted service endpoints are deprecated. Discover other chain deployments via
[The Graph Explorer](https://thegraph.com/explorer).

> Public endpoints in docs are example deployments and may not be maintained by
> Uniswap Labs. Confirm indexing status and schema before production use.

## v4 vs v3 (subgraph)

| Topic | v3 | v4 |
|-------|----|----|
| Global entity | `factory` | `poolManager` |
| Pool identity | Pool contract address | bytes32 pool id (hash of pool key) |
| Hooks | N/A | `Pool.hooks` |
| Position events | mint / burn / collect | subscriptions / unsubscriptions / transfers |
| Liquidity events | Mint / Burn entities | `ModifyLiquidity` |

Mainnet PoolManager id used in docs:

`0x000000000004444c5dc75cb358380d2e3de08a90`

Other chains: see [Deployments](https://developers.uniswap.org/docs/protocols/v4/deployments)
and `networks.json` in the subgraph repo.

## Core entity fields (summary)

### PoolManager

`id`, `poolCount`, `txCount`, `totalVolumeUSD`, `totalVolumeETH`,
`totalFeesUSD`, `totalFeesETH`, `untrackedVolumeUSD`, `totalValueLockedUSD`,
`totalValueLockedETH`, `totalValueLockedUSDUntracked`,
`totalValueLockedETHUntracked`, `owner`

### Token

`id`, `symbol`, `name`, `decimals`, `totalSupply`, `volume`, `volumeUSD`,
`untrackedVolumeUSD`, `feesUSD`, `txCount`, `poolCount`, `totalValueLocked`,
`totalValueLockedUSD`, `totalValueLockedUSDUntracked`, `derivedETH`,
`whitelistPools`

### Pool

`id` (bytes32), `createdAtTimestamp`, `createdAtBlockNumber`, `token0`,
`token1`, `feeTier`, `liquidity`, `sqrtPrice`, `token0Price`, `token1Price`,
`tick`, `tickSpacing`, `observationIndex`, `volumeToken0`, `volumeToken1`,
`volumeUSD`, `untrackedVolumeUSD`, `feesUSD`, `txCount`, collected fee fields,
TVL fields, `isExternalLiquidity`, `hooks`, `liquidityProviderCount`

### Swap

`id` (`txHash#index` in docs; schema may use `#` separator), `transaction`,
`timestamp`, `pool`, `token0`, `token1`, `sender`, `origin`, `amount0`,
`amount1`, `amountUSD`, `sqrtPriceX96`, `tick`, `logIndex`

### Position

`id` / `tokenId`, `owner`, `origin`, `createdAtTimestamp`, `subscriptions`,
`unsubscriptions`, `transfers`

### ModifyLiquidity

`id`, `transaction`, `timestamp`, `pool`, `token0`, `token1`, `sender`,
`origin`, `amount`, `amount0`, `amount1`, `amountUSD`, `tickLower`,
`tickUpper`, `logIndex`

## Query catalog

### Global — current

```graphql
{
  poolManager(id: "0x000000000004444c5dc75cb358380d2e3de08a90") {
    poolCount
    txCount
    totalVolumeUSD
    totalVolumeETH
  }
}
```

### Global — at block

```graphql
{
  poolManager(
    id: "0x000000000004444c5dc75cb358380d2e3de08a90"
    block: { number: 22451931 }
  ) {
    poolCount
    txCount
    totalVolumeUSD
    totalVolumeETH
  }
}
```

### Single pool

```graphql
{
  pool(id: "0x21c67e77068de97969ba93d4aab21826d33ca12bb9f565d8496e8fda8a82ca27") {
    tick
    token0 { symbol id decimals }
    token1 { symbol id decimals }
    feeTier
    sqrtPrice
    liquidity
  }
}
```

### Pools with skip

```graphql
{
  pools(first: 10, skip: 1000) {
    id
    token0 { id symbol }
    token1 { id symbol }
  }
}
```

### Most liquid pools

```graphql
{
  pools(first: 1000, orderBy: liquidity, orderDirection: desc) {
    id
  }
}
```

### Pool day data

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

### Single swap

```graphql
{
  swap(id: "0x0000329e0d864d8e7c93627b76f6b5b99bd776cb18d9f8829e7da469f563e7d4-212") {
    sender
    amount0
    amount1
    transaction { id blockNumber gasUsed gasPrice }
    timestamp
    token0 { id symbol }
    token1 { id symbol }
  }
}
```

### Recent swaps in a pool

```graphql
{
  swaps(
    orderBy: timestamp
    orderDirection: desc
    where: {
      pool: "0x21c67e77068de97969ba93d4aab21826d33ca12bb9f565d8496e8fda8a82ca27"
    }
  ) {
    pool {
      token0 { id symbol }
      token1 { id symbol }
    }
    sender
    amount0
    amount1
  }
}
```

### Token

```graphql
{
  token(id: "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984") {
    symbol
    name
    decimals
    volumeUSD
    poolCount
  }
}
```

### Token day data

```graphql
{
  tokenDayDatas(
    first: 10
    where: { token: "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984" }
    orderBy: date
    orderDirection: asc
  ) {
    date
    token { id symbol }
    volumeUSD
  }
}
```

### Position

```graphql
{
  position(id: 3) {
    id
    subscriptions { id }
    unsubscriptions { id }
    transfers { id }
  }
}
```

## Pagination rules

- Max `first`: **1000**
- Use `skip` in steps of 1000 until a page returns fewer than 1000 items
- Prefer `orderBy` for stable iteration

## curl template

```bash
export THEGRAPH_API_KEY="..."
ENDPOINT="https://gateway.thegraph.com/api/${THEGRAPH_API_KEY}/subgraphs/id/DiYPVdygkfjDWhbxGSqAQxwBKmfKnkWQojqeM2rkLb3G"

curl -s "$ENDPOINT" \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ pools(first: 5, orderBy: liquidity, orderDirection: desc) { id liquidity volumeUSD } }"}' \
  | jq '.'
```

## Official docs

- https://developers.uniswap.org/docs/ecosystem/subgraphs/concepts/v4/queries
- https://developers.uniswap.org/docs/ecosystem/subgraphs/guides/v4-query-examples
- https://developers.uniswap.org/docs/ecosystem/subgraphs/concepts/v4/entities
- https://developers.uniswap.org/docs/ecosystem/subgraphs/overview
- https://developers.uniswap.org/docs/protocols/v4/deployments
