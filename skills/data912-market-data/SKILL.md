---
name: data912-market-data
description: >
  Query Data912 market data endpoints for Argentina and USA instruments.
  Use when the user asks for MEP/CCL quotes, live Argentine market panels
  (stocks, options, cedears, notes, corporate debt, bonds), USA panels (ADRs, stocks),
  OHLC historical series by ticker, USA option chains, or volatility/risk metrics.
  Also use when the user mentions "Data912", "mep", "ccl", "cedears", "option chain",
  "historical bars", "OHLC", "implied volatility", "historical volatility", or
  "volatility percentiles" and expects API-backed market snapshots.
---

# Data912 Market Data

Query Data912's public market API for Argentina and USA market data snapshots, historical bars, and EOD derivatives analytics.

## API Overview

- **Base URL**: `https://data912.com`
- **Auth**: None required (public API)
- **Format**: JSON responses
- **Source note**: Data912 describes this API as educational/hobby data and explicitly not real-time.
- **Freshness/caching note**: The spec says live endpoints are "Not real time, endpoints data refreshed every 20 seconds". Responses are cached by Cloudflare: `cache-control: public, max-age=30` on `/live/*` and `max-age=3600` (1 hour) on `/historical/*` and `/eod/*`.

## Endpoint Groups

### 1. Live Market Panels

- `/live/mep` (USD MEP)
- `/live/ccl` (USD CCL)
- `/live/arg_stocks`
- `/live/arg_options`
- `/live/arg_cedears`
- `/live/arg_notes`
- `/live/arg_corp`
- `/live/arg_bonds`
- `/live/usa_adrs`
- `/live/usa_stocks`

Example:

```bash
curl -s "https://data912.com/live/arg_stocks" | jq '.[0:5]'
```

### 2. Historical OHLC

- `/historical/stocks/{ticker}`
- `/historical/cedears/{ticker}`
- `/historical/bonds/{ticker}`

Example:

```bash
curl -s "https://data912.com/historical/stocks/GGAL" | jq '.[-10:]'
```

Historical series are sorted ascending by `date` (oldest first; GGAL starts in 2001), so use `.[-10:]` for the most recent bars, not `.[0:10]`.

### 3. EOD Derivatives Analytics

- `/eod/volatilities/{ticker}`
- `/eod/option_chain/{ticker}`

Examples:

```bash
curl -s "https://data912.com/eod/volatilities/AAPL" | jq '.'
curl -s "https://data912.com/eod/option_chain/AAPL" | jq '.[0:10]'
```

### Out of Scope for This Skill

- Do not use `/contact` in this skill. Keep this skill focused on market data retrieval and interpretation.

## Key Fields

### Panel Fields (`/live/*`)

- `symbol`: instrument ticker/symbol
- `px_bid`, `q_bid`: bid price and bid size
- `px_ask`, `q_ask`: ask price and ask size
- `c`: last/close-like traded value
- `pct_change`: percentage variation
- `v`: volume
- `q_op`: operations count (when provided)

### Historical Fields (`/historical/*/{ticker}`)

- `date`: date string
- `o`, `h`, `l`, `c`: OHLC values
- `v`: volume
- `dr`: daily return
- `sa`: sigma annualized (annualized volatility, as a decimal, e.g. `0.44` = 44%)

### Volatility Metrics (`/eod/volatilities/{ticker}`)

- IV term structure: `iv_s_term`, `iv_m_term`, `iv_l_term`
- IV percentiles: `iv_*_percentile`
- HV term structure: `hv_s_term`, `hv_m_term`, `hv_l_term`
- HV percentiles: `hv_*_percentile`
- Relative-value ratios: `iv_hv_*_ratio`, `iv_fair_iv_ratio`
- Fair value reference: `fair_iv`, `fair_iv_percentile`

### Option Chain Fields (`/eod/option_chain/{ticker}`)

- Contract context: `opex`, `s_symbol`, `type`, `k`
- Market data: `bid`, `ask`, `c`, `oi`
- Greeks: `delta`, `gamma`, `theta`, `vega`, `rho`
- Valuation/probabilities: `fair_value`, `fair_iv`, `itm_prob`, `intrinsic`, `otm`
- Horizon context: `r_days`, `r_tdays`, `hv_2m`, `hv_1yr`

## Workflow

1. **Identify intent** and select endpoint group:
   - FX/panel snapshot -> `/live/*`
   - Time series/evolution -> `/historical/*/{ticker}`
   - Options/risk analytics -> `/eod/*/{ticker}`
2. **Validate required input**:
   - For historical/EOD endpoints, require a ticker symbol.
   - If ticker is missing, ask for it before querying.
3. **Fetch data with `curl -s`** and parse with `jq`.
4. **Handle empty or unknown-ticker responses**:
   - If response is `[]`, report: "No data currently available for this endpoint/ticker."
   - An unknown ticker on `/historical/*/{ticker}` returns **HTTP 200** with a JSON object instead of an array, e.g. `{"Error":"Nahh no tengo ese ticker loko"}`. Detect it with `jq 'type == "object" and has("Error")'` and report that the ticker was not found.
5. **Present an actionable summary**:
   - Start with a short snapshot.
   - Then include relevant detail fields requested by the user.
6. **Keep context clear**:
   - Remind users this is educational/non-real-time data.
   - Avoid turning output into trading advice.

## Error Handling

- **429 Too Many Requests**:
  - Most market endpoints publish `120 req/min`.
  - Back off and retry after a short delay; avoid burst loops.
- **Unknown ticker (HTTP 200 + `Error` key)**:
  - Not a 422 and not `[]`: the body is an object like `{"Error":"Nahh no tengo ese ticker loko"}`.
  - Check for an object with an `Error` key before parsing as an array; re-check the symbol and the endpoint group (stocks vs cedears vs bonds).
- **422 Validation Error**:
  - Documented in the spec for malformed path input; re-check symbol and endpoint before retrying.
- **Network/timeout failures**:
  - Retry a small number of times (for example, 2 retries with delay).
  - If still failing, return a clear failure message and the endpoint attempted.

## Presenting Results

When returning results to the user:

- Lead with a concise snapshot (what moved, where, and magnitude).
- For panel requests, compare bid/ask/last and `% change`.
- For historical requests, summarize trend windows and notable jumps.
- For vol/options requests, highlight percentiles and IV/HV relationships.
- Explicitly mention the data is educational/non-real-time.
- Do not provide financial recommendations.

## OpenAPI Spec

For the full schema and endpoint definitions, see [references/openapi-spec.json](references/openapi-spec.json).
