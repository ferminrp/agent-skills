#!/usr/bin/env bash
# Idempotent: creates ~/.finanzas-ar/venv, installs yfinance matplotlib scipy+pandas, runs a test fetch.
set -euo pipefail
HOME_DIR="${FINANZAS_AR_HOME:-$HOME/.finanzas-ar}"; VENV="$HOME_DIR/venv"
HERE="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$HOME_DIR"
[ -x "$VENV/bin/python" ] || python3 -m venv "$VENV"
"$VENV/bin/python" -m pip install -q --upgrade pip
"$VENV/bin/python" -c "import yfinance, pandas, matplotlib, scipy" 2>/dev/null || "$VENV/bin/pip" install -q yfinance pandas matplotlib scipy
cp "$HERE/scripts/yf_quote.py" "$HOME_DIR/yf_quote.py"
echo "yfinance matplotlib scipy $("$VENV/bin/python" -c 'import yfinance;print(yfinance.__version__)')"
echo "Test fetch:"; "$VENV/bin/python" "$HOME_DIR/yf_quote.py" GGAL.BA AAPL ARS=X
