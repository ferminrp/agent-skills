# Changelog
## 1.8.0 — 2026-11-04
- Added chart style: references/charts.md (guidelines for presentable X/Twitter charts, light mode, adapted from stageshow) and scripts/xchart.py helper (figure/label/stat/finish/phone_sheet). New rule in SKILL.md.

## 1.7.0 — 2026-11-04
- Added gallo (v1): Gallo Fintech MCP https://data.gallofintech.com/api/mcp (56 tools; paid account required, some tools Pro/Pro+). Verified live 2026-11-04: get_kpis, get_puntas (BYMA L2 book, real-time), get_curve_lecap, get_fci_ranking, list_futuros (implied rate), get_bono_payments, get_table. Rest unverified. Write/account tools (alerts, paper trading, broker portfolio) not to be called unprompted.
- Routing: gallo primary for BYMA real-time book and dollar futures; fallback for LECAP curve, FCI ranking, KPI snapshot, bond cashflows, implied CCL. Priority real-time sources (comparadolar, comparapix, criptoya) unchanged.

## 1.6.1 — 2026-11-02
- indec verified with a real token: all 19 endpoints return data (200; 206 with `Prefer: count=exact`). references/indec.md rewritten with real fields, latest periods (precios/comercio 202609; EMAE/IPI/salarios 202608; EPH 2T-2026; pobreza 1S-2026), filter values (region, nivel, tipo_de_indicador, serie, codigo), and quirks (1000-row cap, hyphenated paths, capitalized columns, `*_null` twin columns, salarios valor as comma string). "From OpenAPI / sin probar" caveats removed.
- Token lookup: env INDEC_API_TOKEN, else ~/.finanzas-ar/secrets/indec_token; documented how to get a free token; keyless fallback unchanged.
- Routing: IPC nivel general now indec first (argentinadatos/monitorargy fallback).

## 1.6.0 — 2026-11-02
- Added indec (v1): Catálogo API-INDEC (BETA), PostgREST at https://api.indec.gob.ar/v1, OpenAPI 3.1 at GET /v1/ (no auth). 19 GET endpoints: IPC, CBA/CBT, canasta de crianza, SIPM, ICC, redeterminación obra pública, índice de salarios, EPH mercado de trabajo y pobreza, EMAE nivel general y sectores, IPI manufacturero y minero, expo/impo de bienes + nomenclaturas, proyecciones/estimaciones de población. Free JWT required (register + OTP in portal; env INDEC_API_TOKEN). Verified 2026-11-02: spec 200, all 19 paths 401 without token, CORS *, no rate-limit headers; response fields from OpenAPI (not tested with token).
- Routing: indec first for IPC with aperturas, canastas, pobreza, EPH, salarios, EMAE/IPI, precios mayoristas/ICC, comercio exterior, población; argentinadatos/monitorargy as keyless fallbacks. Headline inflation stays on argentinadatos.

## 1.5.0 — 2026-10-28
- Added comparadolar (v1): real-time USD quotes per provider (29 banks/apps/brokers/wallets; bid/ask, usdType Oficial/MEP/CCL/Cripto, isBank, is24x7, stale) plus USDT/USDC/BTC/ETH per exchange and per-provider history. Public, no auth, cache 60 s. Verified live 2026-10-28: /usd, /usd/providers, /usd/providers/{slug}/history, /usdt, /btc, /usdt/providers/{slug}/history, /health; /usdc, /eth from OpenAPI.
- Routing: real-time dólar per provider → comparadolar first (criptoya, then dolarapi); reales con PIX → comparapix first; crypto per exchange → criptoya first, comparadolar second view. dolarapi stays for headline reference values, argentinadatos for history; new row for per-provider history.
- Rule: name the app/provider of every real-time price, list the best few options, cite source + Buenos Aires time.
## 1.4.0 — 2026-10-28
- Added loguitos (v1): Argentine provider logos and flags, public, no auth. GET https://loguitos.app/api/logos (q, domain, category, limit ≤200, offset); returns Google/DDG favicon URLs and flag SVGs. No size/format/dark params. Verified live 2026-10-28 (Galicia, Mercado Pago, Binance, Ripio, BBVA, AR flag).
- Rule: visual pieces (dashboards, Pages, charts) that need provider logos use loguitos; if missing, initials or plain text, never an invented logo. Routing row for logos.
- Polymarket: every polymarket.com link shown (chat, Pages, alerts, recipes) carries `via=oraculo.ar` (`?`/`&`). Updated references/polymarket.md (Links section), SKILL.md rule, and the getting-started Polymarket recipe alert link (that recipe is not part of this skill; the rule lives in references/polymarket.md "Links (attribution)" and SKILL.md).
## 1.3.0 — 2026-10-28
- Added polymarket (v1): public prediction-market reads, no auth. Gamma (events/markets by slug, public-search), CLOB (midpoint, price, spread, last-trade-price, book, batch midpoints/prices, prices-history), Data API (v2/prices-history, oi, holders, trades). All dry-run live 2026-10-28.
- Notes: outcomes/outcomePrices/clobTokenIds are JSON strings; CLOB history `market` = token id; Cloudflare IP throttling (Gamma /events 500 req/10s, CLOB /prices-history 1,000/10s).
- Routing rows for prediction-market odds and history; example event argentina-presidential-election-winner.

## 1.2.0 — 2026-10-28
- Added bondterminal (v1): Argentine/EM bond analytics (TIR/YTM S.A., duration, convexity, G/Z spread, cashflows, history, price↔yield calculator, riesgo país). First source that needs auth: free self-serve API key in env BONDTERMINAL_API_KEY (Bearer); free tier 25 calculations + 200 read units/day, 100 req/min.
- Keyless verified: /treasury-curve (200) and MCP bondterminal_riesgo_pais. Other endpoints from OpenAPI 1.3.0 (402 x402 / 401 without key); data912 remains the price fallback.
- Routing rows for bond TIR, cashflows, calculator, history, Treasury curve. Rules: auth note, S.A. yield caveat.

## 1.1.1 — 2026-10-28
- Dry-run of every endpoint/tool; all answered. Doc fixes only:
- argentinadatos v2: dated routes (/cotizaciones/dolares/{casa}/{Y/M/D}, /fci/{tipo}/{Y/M/D}) verified; extra plazoFijo/otros fields.
- comparatasas v2: moneda "Peso Argentino" (was "Peso Argentina", broke filters); historico fields; /fci/otros/{slug}/ and prestamosPersonalesBcra verified; comisiones/REM fields; full URLs in examples.
- bcra v2: cambiarias /Cotizaciones/{moneda} limit must be 10–1000.
- cedears v2: MCP response shapes, yahooSymbol; /api now 404.
- monitorargy v2: real field names (fuente, ultimaFecha, ultimoValor, puntos), resolucion 1m.
- yfinance v2: setup test no longer uses ^MERV; script silences pandas warnings.
## 1.1.0 — 2026-10-28
- Added comparatasas (FCI ranking, cuentas remuneradas, plazo fijo, LECAPs, cauciones, bonos CER, crypto yields via the ArgentinaDatos endpoints its frontend calls).
## 1.0.0 — 2026-10-28
- Initial sources: data912, cedears, comparapix, argentinadatos, dolarapi, monitorargy, bcra, criptoya, yfinance.
- Registry schema_version 1.0.
