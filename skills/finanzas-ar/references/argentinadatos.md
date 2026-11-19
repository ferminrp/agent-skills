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
| /finanzas/tasas/depositos30Dias | fecha, valor (decimal) |
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

```
curl -s https://api.argentinadatos.com/v1/finanzas/indices/inflacion | jq '.[-12:]'
```
