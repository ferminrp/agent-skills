# ArgentinaDatos (REST) — v2
Base: https://api.argentinadatos.com/v1 · Auth: none · Docs: https://argentinadatos.com/docs. Rate limit not published.
All below verified 2026-10-28 (HTTP 200).

| Endpoint | Fields |
|---|---|
| /cotizaciones/dolares | history all casas: casa, compra, venta, fecha |
| /cotizaciones/dolares/{casa} (blue, oficial, bolsa, contadoconliqui, mayorista, cripto, tarjeta) | same; /{casa}/{YYYY/MM/DD} → single {casa, compra, venta, fecha} |
| /finanzas/indices/inflacion | monthly IPC %: fecha, valor |
| /finanzas/indices/inflacionInteranual | YoY %: fecha, valor |
| /finanzas/indices/uva | fecha, valor |
| /finanzas/indices/riesgo-pais , /riesgo-pais/ultimo | fecha, valor (bps) |
| /finanzas/tasas/plazoFijo | entidad, logo, tnaClientes, tnaNoClientes, enlace, tasas[] |
| /finanzas/tasas/depositos30Dias | fecha, valor (TNA; **unit changes**, see below) |
| /finanzas/rendimientos | entidad, rendimientos[{moneda, apy, fecha}] (crypto/wallet yields) |
| /finanzas/fci/{mercadoDinero,rentaVariable,rentaFija,rentaMixta}/{ultimo,penultimo} | fondo, horizonte, fecha, vcp, ccp, patrimonio |
| /finanzas/fci/otros/ultimo | fondo, tna, tea, tope, fecha, condiciones, plazoMinDias (wallet accounts) |
| /finanzas/fci/{tipo}/{YYYY/MM/DD} | same as /ultimo for that date |
| /finanzas/creditos/hipotecariosUva | entidad, nombreComercial, tna, metadata |
| /feriados/{año} | fecha, tipo, nombre |
| /eventos/presidenciales | fecha, tipo, evento |
| /senado/senadores, /senado/actas, /diputados/diputados, /diputados/actas | congress data |
| /estado | {estado} |

All verified 2026-10-28, including the dated routes.

**depositos30Dias unit** (verified 2026-11-19): decimal up to 2025-01-21 (`0.3039` = 30.39 %), percentage from 2025-01-22 (`30.34`). Also 15 isolated days in 2024-08/2025-01 already in %. Decimals reach 1.30 (TNA > 100 % in 2023-24), so `valor > 1` is not a safe test; percentages never go below ~19. Normalize with `if valor > 5 then valor/100 else valor` (→ decimal).
`/fci/{tipo}/ultimo` mixes funds with stale `fecha` (years old) with the latest day: keep only rows with the max `fecha` (or within a few days of it).

```
curl -s https://api.argentinadatos.com/v1/finanzas/indices/inflacion | jq '.[-12:]'
```
