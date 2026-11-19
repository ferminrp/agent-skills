# cedears.com (REST files + MCP) — v2
Auth: none. Discovery: https://cedears.com/llms.txt, https://cedears.com/.well-known/mcp.json. Rate limit not published.
Verified 2026-10-28.

## Files (GET)
- https://cedears.com/cedears.json — catalog: Cedears, Name, Market, Ratio, TickerOriginal, yahooSymbol, tags, yfinanceFetchedAt (no live price)
- https://cedears.com/cedears.csv — live table: Ticker, Empresa, Mercado, Ratio, Ticker original, Precio ARS, Var. %, Volumen, Precio US, Precio MEP, Precio CCL, Precio justo USD, Prima %, Tags
- https://cedears.com/cedears.md — same as CSV in Markdown

## MCP: POST https://cedears.com/mcp (streamable-http JSON-RPC; GET returns info JSON)
Tools (from tools/list):
- list_cedears {query?, tag?, limit? (default 50, max 500)} — {count, total, columns, rows[]}: rows with live BYMA prices, MEP/CCL, premium
- get_cedear {ticker} — {found, row:{Ticker, Empresa, Mercado, Ratio, Ticker original, Precio ARS, Var. %, Precio US, Precio MEP, Precio CCL, Precio justo USD, Prima %, Tags}}
- earnings {day? | start?, end?} (max 31 days) — {start, end, window, days[{date, items[{cedear, name, market, tickerOriginal, earningsTime, isDateConfirmed}]}]}

```
curl -s https://cedears.com/mcp -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
 -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_cedear","arguments":{"ticker":"AAPL"}}}'
```
No separate REST API (/api and /api/docs → 404).
