# Gallo Fintech (MCP) — v1
URL: POST https://data.gallofintech.com/api/mcp · MCP (streamable-http) · Auth: **requires a PAID Gallo Fintech account** (data.gallofintech.com) and its MCP auth; connect it as an MCP connector (56 tools). Some tools need higher plans (Pro / Pro+). If not connected or the plan lacks a tool, use the routing fallback.
Coverage: BYMA live book (bonds, equities, CEDEARs), LECAP curve, cauciones, dollar futures (ROFEX/A3) with implied rate, CCL/MEP implícito, ONs, FCI ranking/history, bond cashflows, KPIs (dólar, riesgo país, inflación, plazo fijo, UVA, BTC, commodities), macro, BCRA reserves, US equities data (FMP: quotes, intraday, technicals, earnings, dividends, insider, 13F, IPOs, M&A).
Verified live 2026-11-04 (~13:21 Buenos Aires, rueda abierta): get_kpis, get_puntas, get_curve_lecap, get_fci_ranking, list_futuros, get_bono_payments, get_table(licitaciones_proximas). Others listed from tools/list, **unverified**.

Tools (verified):
- get_kpis {metrics[]: dolar_oficial|dolar_mep|dolar_ccl|dolar_blue|riesgo_pais|inflacion|merval_change|tasa_plazo_fijo|futuros_spot|futuros_tasa_promedio|avg_ccl|avg_mep|btc_price|eth_price|oro|petroleo|soja|uva} — UI block `{blocks[{type:"kpis", data[{label, value (string, e.g. "$1570"), sub (compra or date), color}]}]}`. No timestamp for dollar values; riesgo país/inflación carry a date in `sub` (riesgo país 2026-11-03, inflación 2026-09-30). Plazo fijo = best bank TNA (named in `sub`).
- get_puntas {symbols[1..20]} — {quotes[{symbol, price, changePercentage, currency, bid, ask, bids[5]{price,size}, asks[5], fetchedAt (UTC)}], bymaBookLayerOk, book{level, marketOpen}}. L2 depth needs Pro+ and open market (`book.reason` otherwise). Real-time (fetchedAt = call time).
- get_curve_lecap {} — bar_chart block: data[{name: ticker, value: TEM %}], unit "% TEM". No prices/dates.
- get_fci_ranking {category?: mercadoDinero|rentaFija|rentaVariable|rentaMixta|otros, limit? ≤2000} — {data[{fondo, tipoRenta, vcp, fecha, ret7d, ret30d, ret90d, retYTD, dataPoints, flag}], total, methodology, fetchedAt}. Returns in % (not annualized), sorted by ret30d; null = insufficient history or VCP jump.
- list_futuros {} — {data[{symbol "DLR/NOV26", price, settlement, bid, ask, volume, daysToExpiry, tasaImplicita (% TNA), devaluacionMensual (%)}]}.
- get_bono_payments {ticker?} — {payments[{date, ticker, currency, interest, amort, total, cat, desc}]} per 100 VN, includes past payments.
- get_table {dataset: top_gainers|top_losers|top_volume|all_stocks|bonds|cedears|dolares|futuros|ccl_implicito|predicciones|eco_calendar|licitaciones_proximas|licitaciones_resultados|letras_activas|crypto|commodities|correlaciones|opciones, limit?, symbol? (opciones)} — table block {columns[], rows[]}. licitaciones_proximas returned a "no hay próximas licitaciones" message row.

Tools (unverified): list_bonos, list_ons, list_letras, list_cauciones, get_curve_cauciones, list_ccl_implicito, list_fcis, get_fci_history {fund}, get_riesgo_pais, get_bcra_reservas, get_economia, get_market_session {market}, get_trades {symbol}, get_line_chart / compare_symbols / get_technicals {symbol, period, market ar|us}, get_quote, get_intraday(_prices), get_aftermarket, get_earnings, get_dividendos, get_splits, get_ipos, get_m_and_a, get_insider, get_institutional, get_esg, get_global_market, get_sectors_heatmap, get_bar_chart, search_instruments, get_predicciones (heuristic, not advice). Pro-only: get_g_score, get_news_sentiment, get_screener, get_portfolio_analysis; Pro+: recomendar_orden.
Never call (write/account tools): create_alerta, delete_alerta, place_paper_order, cancel_paper_order, get_my_portfolio / get_portfolio_analysis (user's IEB broker data) unless the user asks.

Quirks: many tools return UI "blocks" with values as formatted strings; parse carefully. Some sub-sources are ArgentinaDatos/BCRA/FMP (state Gallo + underlying source). Calls can hang; a batch of 12 parallel calls timed out (~15 s) — call a few at a time.
```
curl -s https://data.gallofintech.com/api/mcp -H 'Authorization: Bearer <gallo token>' -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
 -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_puntas","arguments":{"symbols":["AL30"]}}}'
```
