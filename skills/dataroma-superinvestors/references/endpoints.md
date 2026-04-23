# DataRoma + Defuddle Endpoints

## URL Templates

- Home (active superinvestors list):
  - `https://defuddle.md/https://dataroma.com/m/home.php`
- Holdings (portfolio composition):
  - `https://defuddle.md/https://dataroma.com/m/holdings.php?m={managerCode}`
- Activity all:
  - `https://defuddle.md/https://dataroma.com/m/m_activity.php?m={managerCode}&typ=a`
- Activity buys:
  - `https://defuddle.md/https://dataroma.com/m/m_activity.php?m={managerCode}&typ=b`
- Activity sells:
  - `https://defuddle.md/https://dataroma.com/m/m_activity.php?m={managerCode}&typ=s`

Optional URL fragments such as `#google_vignette` can be ignored for parsing.

## Example Manager Codes

- `tp` -> Daniel Loeb / Third Point
- `MAVFX` -> David Katz / Matrix Asset Advisors

Examples:

- `https://defuddle.md/https://dataroma.com/m/holdings.php?m=tp`
- `https://defuddle.md/https://dataroma.com/m/holdings.php?m=MAVFX`
- `https://defuddle.md/https://dataroma.com/m/m_activity.php?m=tp&typ=a`

## Expected Markdown Parsing (Holdings)

Typical header block:

- Manager identity
- `Period`
- `Portfolio date`
- `No. of stocks`
- `Portfolio value`

Typical holdings table columns:

- `Stock` (often `TICKER - Company`)
- `% of Portfolio`
- `Recent Activity`
- `Shares`
- `Reported Price`
- `Value`
- sometimes `Current Price`, `+/- Reported Price`, `52 Week Low`, `52 Week High`

Recommended extraction priority:

1. Manager metadata block
2. Holdings table (top by `% of Portfolio`)
3. Optional sector analysis

## Expected Markdown Parsing (Activity)

Typical activity table columns:

- `Stock`
- `Activity` (`Add`, `Reduce`, `Buy`, `Sell`)
- `Share change`
- `% change to portfolio`
- quarter markers (for example `Q4 2025`)

Known caveat:

- Activity markdown can be less clean than holdings. If rows are partial or malformed, extract what is reliable and disclose limitations.

## Suggested Selection Logic

1. If user provides `managerCode`, use it directly.
2. If user provides a manager name, resolve it by scanning home list links and matching name text.
3. If multiple candidates match, show short disambiguation list with `name + managerCode + updated date`.

## Suggested Response Sections

- `Manager Snapshot`
- `Top Holdings`
- `Recent Movements`
- `Quick Take`
- `Sources`
