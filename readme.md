# Agent Skills

A collection of skills for AI coding agents (Claude Code, Cursor, etc.) that extend their capabilities with specialized domain knowledge and workflows.

## Available Skills

| Skill | Description |
|-------|-------------|
| [bcra-central-deudores](skills/bcra-central-deudores/) | Query Argentina's BCRA Central de Deudores API to check credit status, debt history, and rejected checks by CUIT/CUIL/CDI |
| [data912-market-data](skills/data912-market-data/) | Query Data912 market endpoints for MEP/CCL, live AR/US panels, historical OHLC by ticker, and USA options volatility analytics |
| [cotizacion-dolar-argentina](skills/cotizacion-dolar-argentina/) | Consulta cotizaciones de dolar y monedas (EUR/BRL/CLP/UYU) en Argentina usando DolarAPI |
| [crypto-prices-criptoya](skills/crypto-prices-criptoya/) | Consulta cotizaciones cripto por exchange y agregadas, y fees de retiro, usando CriptoYa API |
| [coingecko-and-coinmarketcap-apis](skills/coingecko-and-coinmarketcap-apis/) | Consulta precios, markets, histórico y datos DEX keyless de CoinGecko/GeckoTerminal y CoinMarketCap |
| [cotizaciones-pix-comparapix](skills/cotizaciones-pix-comparapix/) | Consulta y compara cotizaciones Pix entre apps desde api.comparapix.ar/quotes, con recomendacion de interfaz en comparapix.ar |
| [finanzas-ar](skills/finanzas-ar/) | Route Argentine financial data questions (dólar variants, BYMA, CEDEARs, bonds, LECAPs, crypto per exchange, PIX, inflation, UVA, riesgo país, BCRA, FCI, etc.) via a question→source→fallback table, versioned registry, and per-source references |
| [writing-well](skills/writing-well/) | Audit and improve writing quality with a 7-check framework for clarity, concision, evidence, jargon, and flow, including severity-ranked findings and a full rewrite suggestion |
| [product-shaping](skills/product-shaping/) | Guided process for shaping product ideas and specs by surfacing unknowns through research, brainstorm, prototypes, and interviews before anything gets built |
| [tvmaze-series-tracker](skills/tvmaze-series-tracker/) | Track favorite TV shows via TVmaze: confirm-before-add (poster + synopsis), list/upcoming, silent daily air-day alerts |
| [feature-video](skills/feature-video/) | Ship a 30–60 s feature demo MP4 from real Playwright UI captures, project brand config, and Remotion (brief → storyboard → QA contact sheet → render) |

## Installation

### Skills CLI (recommended)

```bash
npx skills add ferminrp/agent-skills
```

### Claude Code (manual copy)

Copy the skill folder into your skills directory:

```bash
# Personal (available in all your projects)
mkdir -p ~/.claude/skills
cp -r skills/skill-name ~/.claude/skills/

# Project-only (commit it with your repo)
mkdir -p .claude/skills
cp -r skills/skill-name .claude/skills/
```

### Claude.ai (upload)

Zip the skill folder so the archive contains `skill-name/SKILL.md`, then upload it in claude.ai under Settings > Capabilities (Skills section):

```bash
cd skills && zip -r ../skill-name.zip skill-name/
```

A prebuilt package for `bcra-central-deudores` is available in [`dist/`](dist/) (`.skill` files are plain zip archives; rename to `.zip` if the uploader requires it).

## Contributing

Each skill lives in its own folder under `skills/` and follows the standard skill structure:

```
skills/skill-name/
├── SKILL.md           # Required — frontmatter + instructions
├── references/        # Optional — docs loaded into context as needed
├── scripts/           # Optional — executable code
└── assets/            # Optional — files used in output
```

## License

MIT
