# Agent Skills

A collection of skills for AI coding agents (Claude Code, Cursor, etc.) that extend their capabilities with specialized domain knowledge and workflows.

## Available Skills

| Skill | Description |
|-------|-------------|
| [bcra-central-deudores](skills/bcra-central-deudores/) | Query Argentina's BCRA Central de Deudores API to check credit status, debt history, and rejected checks by CUIT/CUIL/CDI |
| [data912-market-data](skills/data912-market-data/) | Query Data912 market endpoints for MEP/CCL, live AR/US panels, historical OHLC by ticker, and USA options volatility analytics |
| [cotizacion-dolar-argentina](skills/cotizacion-dolar-argentina/) | Consulta cotizaciones de dolar y monedas (EUR/BRL/CLP/UYU) en Argentina usando DolarAPI |
| [crypto-prices-criptoya](skills/crypto-prices-criptoya/) | Consulta cotizaciones cripto por exchange y agregadas, y fees de retiro, usando CriptoYa API |
| [inflacion-argentina-ipc](skills/inflacion-argentina-ipc/) | Consulta la serie historica y el ultimo dato de IPC/inflacion mensual de Argentina desde Anduin API |
| [riesgo-pais-argentina](skills/riesgo-pais-argentina/) | Consulta la serie historica y el ultimo dato de riesgo pais de Argentina desde Anduin API |
| [travel-promos-argentina](skills/travel-promos-argentina/) | Consulta promociones de viajes (vuelos/hoteles/paquetes) y permite filtrarlas/rankearlas usando Anduin API |
| [cotizaciones-pix-comparapix](skills/cotizaciones-pix-comparapix/) | Consulta y compara cotizaciones Pix entre apps desde api.comparapix.ar/quotes, con recomendacion de interfaz en comparapix.ar |

## Installation

### Skills CLI (recommended)

```bash
npx skills add ferminrp/agent-skills
```

### Claude Code (local `.skill` file)

```bash
claude install-skill /path/to/skill-name.skill
```

Or install from the `.skill` file in [Releases](../../releases).

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
