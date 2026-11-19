---
name: finanzas-ar
description: Use for any Argentine financial data question — dólar (oficial, blue, MEP, CCL, cripto, tarjeta), BYMA stocks, CEDEARs, bonds, LECAPs, ONs, options, inflation, riesgo país, plazo fijo, FCI, UVA, BCRA series, reserves, cheques, dollar and crypto quotes per provider/app (where to buy), PIX rates, macro indicators, feriados, or monitoring tickers with yfinance.
---
# Finanzas AR data

Sources live in `sources/registry.json`; details per source in `references/<id>.md`. Read the reference before calling a source. All sources are free except gallo (paid); bondterminal needs a free API key (env BONDTERMINAL_API_KEY, 25 calcs + 200 read units/day) and indec a free JWT (env INDEC_API_TOKEN, else file ~/.finanzas-ar/secrets/indec_token; never print it). gallo needs a paid Gallo Fintech account (MCP connector); if not connected, use the fallback. If the key/token is unset, use the fallback.

## Routing
| Question | Best | Fallback |
|---|---|---|
| Real-time dólar per provider / where to buy or sell (banks, apps, brokers, wallets) | comparadolar `/usd` | criptoya `/dolar`, then dolarapi `/dolares` |
| Dólar headline reference (oficial/blue/MEP/CCL/cripto/tarjeta averages) | dolarapi `/dolares` | criptoya `/dolar` |
| Dólar history | argentinadatos `/cotizaciones/dolares/{casa}` | bcra cambiarias (official only) |
| Dólar history per provider | comparadolar `/usd/providers/{slug}/history` | — |
| USD per bank | comparadolar `/usd` (`isBank`) | criptoya `/bancostodos` (drop banks whose `time` is > 24 h old) |
| Other currencies vs ARS / other countries | dolarapi `/cotizaciones`, `{cl,uy,mx,ve,co}.dolarapi.com` | bcra cambiarias `Cotizaciones` |
| Real-time crypto per exchange (USDT/USDC/BTC/ETH in ARS) | criptoya `/{coin}/ars/{vol}` | comparadolar `/{usdt,usdc,btc,eth}` (second view), then dolarapi `/dolares/cripto` |
| Real-time reales con PIX / pay in Brazil | comparapix `api.comparapix.ar/quotes` or comparapix MCP | criptoya `/usdt/brl/100` |
| BYMA stocks, bonds, LECAPs, ONs, options live | data912 `/live/*` | yfinance `.BA` |
| Implied MEP/CCL per ticker | data912 `/live/mep`, `/live/ccl` | cedears MCP, then gallo `list_ccl_implicito` (paid) |
| CEDEAR ratio, premium, fair price | cedears MCP `get_cedear` / cedears.csv | data912 `/live/arg_cedears` |
| Earnings calendar | cedears MCP `earnings` | — |
| Price history / OHLC | data912 `/historical/*` | yfinance |
| Option IV / chain | data912 `/eod/*` | — |
| Inflation (IPC nivel general) | indec `/ipc_nacional` `region=eq.Nacional&codigo=eq.0&tipo_de_indicador=eq.v_m` (token) | argentinadatos `/finanzas/indices/inflacion`, then monitorargy MCP |
| UVA, riesgo país | argentinadatos `/finanzas/indices/*` | monitorargy MCP |
| Plazo fijo, FCI, wallet yields, UVA mortgages | argentinadatos `/finanzas/tasas`, `/fci`, `/rendimientos`, `/creditos` | — |
| Reserves, base monetaria, BCRA rates | bcra `estadisticas/v4.0/Monetarias` | monitorargy MCP |
| Macro (EMAE, salarios, empleo, fiscal), release calendar | monitorargy MCP | bcra |
| IPC oficial con aperturas (región, división, núcleo/regulados, bienes/servicios) | indec `/ipc_nacional` (token) | argentinadatos `/finanzas/indices/inflacion` (nivel general only), then monitorargy MCP |
| Canasta básica CBA/CBT (pobreza/indigencia línea), canasta de crianza | indec `/valorizacion_canastas_cba_cbt`, `/canasta-crianza` (token) | monitorargy MCP |
| Pobreza e indigencia (EPH) | indec `/pobreza_eph` (token) | monitorargy MCP (`pobreza`) |
| Empleo, desocupación, informalidad (EPH) | indec `/mercado_trabajo_eph` (token) | monitorargy MCP (`empleo`) |
| Índice de salarios | indec `/indice_salarios` (token) | monitorargy MCP (`salarios`) |
| EMAE nivel general y sectores, IPI manufacturero/minero | indec `/estimador-mensual-de-actividad-economica-*`, `/ipi_*` (token) | monitorargy MCP |
| Precios mayoristas, costo de la construcción, redeterminación obra pública | indec `/sipm_precios_mayoristas`, `/icc_precios_construccion`, `/redeterminacion_precios_contratos_obras_publicas` (token) | monitorargy MCP |
| Comercio exterior (expo/impo por país, rubro, uso) | indec `/comercio_exterior_*` (token; decode with `/comercio_exterior_nomenclaturas`) | monitorargy MCP (`comercio_exterior`) |
| Población (proyecciones 2022–2040, departamentos) | indec `/proyecciones_poblacion_*`, `/estimaciones_poblacion_departamento_2022_2035` (token) | — |
| BYMA real-time book (bid/ask, 5-level L2) for bonds, equities, CEDEARs | gallo `get_puntas` (paid) | data912 `/live/*` (delayed) |
| Dollar futures (ROFEX) with implied rate / devaluación mensual | gallo `list_futuros` (paid) | — |
| LECAP curve (TEM per ticker) | comparatasas `/letras` | gallo `get_curve_lecap` (paid) |
| FCI ranking by 7d/30d/90d/YTD return | comparatasas `/fci/comparatasas` | gallo `get_fci_ranking` (paid) |
| Quick KPI snapshot (oficial/MEP/CCL, riesgo país, inflación, best plazo fijo TNA) | dolarapi + argentinadatos | gallo `get_kpis` (paid) |
| Cheque denunciado / deudores (user's own CUIT) | bcra cheques / centraldedeudores | — |
| Feriados | argentinadatos `/feriados/{año}` | — |
| Best FCI / money market by TNA | comparatasas `/fci/comparatasas` (`rendimientos.tnaEstimada`) | argentinadatos `/fci/mercadoDinero/ultimo` (keep only rows with the latest `fecha`) |
| Best cuenta remunerada / billetera, USD accounts | comparatasas `/fci/otros/ultimo`, `/cuentas-remuneradas-usd/` | — |
| LECAPs, bonos CER, cauciones (rates/TIR) | comparatasas `/letras`, `/bonos-cer`, `/cauciones/{ars|usd}` | data912 |
| Crypto yields, criptopesos | comparatasas `/rendimientos`, `/criptopesos/` | criptoya |
| Watchlist / quick quote any ticker | yfinance `yf_quote.py` | data912 |
| Bond TIR, duration, convexity, spreads (hard-dollar AL/GD, ONs) | bondterminal `/bonds/{id}/analytics` | data912 `/live/arg_bonds` (price only) + comparatasas `/bonos-cer` (CER TIR) |
| Bond cashflows (cupones/amortizaciones) | bondterminal `/bonds/{id}/cashflows` | gallo `get_bono_payments` (paid) |
| Price → TIR / TIR → price what-if | bondterminal `POST /calculate` | — |
| Bond prices (watchlist, analytics) | bondterminal `POST /bonds/batch` | data912 `/live/*` |
| Bond yield/spread history | bondterminal `/bonds/{id}/history` (10 read units) | data912 `/historical/*` (price only) |
| US Treasury curve | bondterminal `/treasury-curve` (keyless) | — |
| Prediction-market odds (elecciones AR, eventos) by slug | polymarket Gamma `/events?slug=` (`outcomePrices`, JSON string) | polymarket CLOB `/midpoint?token_id=` |
| Prediction-market probability history | polymarket CLOB `/prices-history?market={token_id}` | polymarket Data `/v2/prices-history?token_id=` |
| Logos of providers (banks, exchanges, brokers, wallets, fintechs) or flags for visuals | loguitos `/api/logos?q={name}` (`google_domain`; flags `category=banderas` → `svgUrl`) | initials / plain name badge (never an invented logo) |

## Rules
- Whenever you build visual pieces (dashboards, Pages, charts, cards, tables with icons) that need provider logos (exchanges, banks, brokers, wallets, fintechs), get them from the loguitos API (`references/loguitos.md`); if none, use initials or plain text, never an invented logo.
- Every polymarket.com link you show (chat, Pages, alerts, recipes) carries `via=oraculo.ar` (`?via=oraculo.ar`, or `&via=oraculo.ar` if it already has params).
- polymarket `outcomes`/`outcomePrices`/`clobTokenIds` are JSON strings; price of "Yes" = probability; read-only, never trade.
- bondterminal yields are semi-annual (S.A.), not TEA; label them.
- Charts (for X/Twitter, Pages, reports): follow `references/charts.md` and use `scripts/xchart.py` (light mode always, one accent on quiet grays, title = the takeaway, key number said once, source + Buenos Aires time footer, check at 390 px with `phone_sheet`). Needs matplotlib in ~/.finanzas-ar/venv.
- Always state source and its timestamp; convert UTC to Buenos Aires time.
- Real-time quotes (dólar, reales con PIX, cripto): always name the app/provider each price comes from (e.g. "Belo vía comparadolar", "Binance vía criptoya"); when several options exist, list the best few by ask (to buy) / bid (to sell) instead of a single number; cite source + Buenos Aires time; skip or flag stale quotes.
- indec: max 1000 rows per call; paginate with limit/offset ordered by the full key; `observaciones`/`*_null` carry INDEC signs (* provisorio, s secreto…). `/indice_salarios.valor` is a string with decimal comma. Only the Bearer header is needed.
- data912 is not real-time: data refreshed ~every 20 s, Cloudflare cache 30 s on `/live/*` and 1 h on `/historical/*`, `/eod/*`. BCRA v3 is deprecated (410): use v4.
- If a source fails, use the fallback and say so.
- MCP sources: POST JSON-RPC with `Accept: application/json, text/event-stream`.
- yfinance: run `setup/setup.sh` once; then `~/.finanzas-ar/venv/bin/python ~/.finanzas-ar/yf_quote.py T1 T2`.

## Source registry (versioned)
`sources/registry.json`: `schema_version`, `registry_version` (semver), and per source `{id, version, base_url, kind: rest|mcp|python, endpoints, added, verified}`.

### Add a source
1. Curl every endpoint; keep only ones from docs or that answered. Mark the rest "unverified".
2. Write `references/<id>.md` (base URL, auth, rate limit, endpoints with params and fields, example curl).
3. Add an entry to `sources/registry.json` (`version: "1"`, `added`/`verified` = today).
4. Add a routing row above.
5. Bump `registry_version` (new source = minor, removal/breaking = major, fixes = patch).
6. Add a `CHANGELOG.md` entry with the new version and date.
Changing a source's API: bump that source's `version`, update its reference, then steps 5–6.
