---
name: dataroma-superinvestors
description: Consult hedge fund and superinvestor portfolios and recent moves from DataRoma using defuddle.md markdown pages. Use when the user asks for holdings, portfolio composition, 13F-style updates, activity, buys, sells, manager movements, or comparisons between investors from DataRoma.
---

# DataRoma Superinvestors via Markdown

Consult DataRoma through defuddle markdown pages and return clean, agent-friendly summaries.

## Core URLs

- Index of active managers: `https://defuddle.md/https://dataroma.com/m/home.php`
- Holdings by manager code: `https://defuddle.md/https://dataroma.com/m/holdings.php?m={managerCode}`
- Activity (all): `https://defuddle.md/https://dataroma.com/m/m_activity.php?m={managerCode}&typ=a`
- Activity (buys): `https://defuddle.md/https://dataroma.com/m/m_activity.php?m={managerCode}&typ=b`
- Activity (sells): `https://defuddle.md/https://dataroma.com/m/m_activity.php?m={managerCode}&typ=s`

For URL templates, parsing expectations, and examples, read `references/endpoints.md`.

## Workflow

1. Fetch manager index from `home.php` via defuddle.
2. Resolve the requested manager and extract the `m=` code from the holdings link.
3. Fetch holdings for that manager.
4. Fetch activity with `typ=a`, and optionally `typ=b` or `typ=s` if user asks specifically.
5. Return a concise markdown report prioritizing holdings quality and recent moves.

## Output Contract

Use this structure by default:

1. `Manager Snapshot`
   - Manager name
   - Period
   - Portfolio date
   - Number of stocks
   - Portfolio value
2. `Top Holdings`
   - 8-15 rows prioritized by `% of Portfolio`
   - Columns: `Ticker | Company | % Portfolio | Recent Activity | Shares | Reported Price | Value`
3. `Recent Movements`
   - Group notable rows by `Add`, `Reduce`, `Buy`, `Sell`
   - Include `share change` and `% change to portfolio` when available
4. `Quick Take`
   - 2-5 bullets with actionable interpretation (concentration, largest adds/reduces, unusual moves)
5. `Sources`
   - Include DataRoma original URLs and the defuddle URL used

## Data Quality and Fallback Rules

- If manager name is ambiguous or not found, offer 3-5 close candidates from the index and ask user to choose.
- If activity markdown is noisy or incomplete, prioritize holdings and state the limitation explicitly.
- Preserve original DataRoma links for traceability.
- Treat this as informational market data; avoid financial advice language.
- If a field is missing, show `N/A` instead of inferring values.
