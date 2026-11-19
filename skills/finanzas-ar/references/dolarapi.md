# DolarApi (REST) — v1
Base: https://dolarapi.com/v1 · Auth: none · Docs: https://dolarapi.com/docs. Rate limit not published. Verified 2026-10-28.
Row: {moneda, casa, nombre, compra, venta, fechaActualizacion (UTC)}
- /dolares — all; /dolares/{oficial|blue|bolsa|contadoconliqui|mayorista|cripto|tarjeta}
- /cotizaciones — other currencies vs ARS; /cotizaciones/{eur|brl|clp|uyu}
- /estado — health
Other countries (GET /v1/cotizaciones, verified): cl.dolarapi.com (has ultimoCierre), uy.dolarapi.com (may be stale: on 2026-11-19 every `fechaActualizacion` was still 2026-09-21; check it before quoting), mx.dolarapi.com (fix), ve.dolarapi.com (fuente, promedio), co.dolarapi.com. br. and bo. returned 404.
```
curl -s https://dolarapi.com/v1/dolares/blue
```
