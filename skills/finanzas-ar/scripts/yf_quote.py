#!/usr/bin/env python3
"""Usage: yf_quote.py TICKER [TICKER...]  -> JSON list {ticker, price, prev_close, change_pct, currency, time}"""
import json, sys, warnings, logging
warnings.filterwarnings("ignore"); logging.getLogger("yfinance").setLevel(logging.CRITICAL)
import yfinance as yf
warnings.simplefilter("ignore")  # yfinance/pandas re-enable warnings on import

def quote(t):
    try:
        h = yf.Ticker(t).history(period="5d", auto_adjust=False)
        if h.empty: return {"ticker": t, "error": "no data"}
        last, prev = h["Close"].iloc[-1], (h["Close"].iloc[-2] if len(h) > 1 else None)
        try: cur = yf.Ticker(t).fast_info.get("currency")
        except Exception: cur = None
        return {"ticker": t, "price": round(float(last), 4),
                "prev_close": round(float(prev), 4) if prev is not None else None,
                "change_pct": round((last / prev - 1) * 100, 2) if prev else None,
                "currency": cur, "time": str(h.index[-1])}
    except Exception as e:
        return {"ticker": t, "error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(__doc__)
    print(json.dumps([quote(t) for t in sys.argv[1:]], indent=2))
