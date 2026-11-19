# yfinance (python) — v2
Local: ~/.finanzas-ar/venv (run setup/setup.sh). `~/.finanzas-ar/venv/bin/python ~/.finanzas-ar/yf_quote.py GGAL.BA YPF AAPL.BA ARS=X`
Output JSON: ticker, price, prev_close, change_pct, currency, time. BYMA tickers end in .BA (ARS). Unofficial Yahoo scraping; may break or rate-limit.
Verified 2026-10-28 with GGAL.BA AAPL ARS=X YPF AAPL.BA (setup test now uses GGAL.BA AAPL ARS=X). Note: ^MERV returned no data on 2026-10-28 (Yahoo gap) — use data912 for Merval constituents.
