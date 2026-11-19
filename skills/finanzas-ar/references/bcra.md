# BCRA APIs (REST) — v2
Base: https://api.bcra.gob.ar · Auth: none · Catalog: https://www.bcra.gob.ar/en/central-bank-api-catalog/
SSL quirk: the cert chain has historically failed on some clients (missing intermediate). Strict curl worked on 2026-10-28; if it fails use `curl -k` or Python `verify=False`. Envelope: {status, metadata.resultset{count,offset,limit}, results} or {status, errorMessages}.

## Estadísticas monetarias v4.0 (verified)
- /estadisticas/v4.0/Monetarias — catalog: idVariable, descripcion, categoria, ... (1610 vars; paginate limit/offset)
- /estadisticas/v4.0/Monetarias/{idVariable}?desde=YYYY-MM-DD&hasta=&limit=&offset= — results[{idVariable, detalle[{fecha, valor}]}]. id 1 = reservas internacionales.
- v3.0 returns HTTP 410 "deprecado" — do not use.

## Estadísticas cambiarias v1.0 (verified)
- /estadisticascambiarias/v1.0/Maestros/Divisas — codigo, denominacion
- /estadisticascambiarias/v1.0/Cotizaciones[?fecha=YYYY-MM-DD] — results{fecha, detalle[{codigoMoneda, descripcion, tipoPase, tipoCotizacion}]}
- /estadisticascambiarias/v1.0/Cotizaciones/{moneda}?fechadesde=&fechahasta=&limit=&offset= — limit must be 10–1000 (else HTTP 400); results[{fecha, detalle[]}]

## Cheques v1.0 (verified)
- /cheques/v1.0/entidades — codigoEntidad, denominacion
- /cheques/v1.0/denunciados/{codigoEntidad}/{numeroCheque} — numeroCheque, denunciado, fechaProcesamiento, denominacionEntidad, detalles

## Central de Deudores v1.0 (responded; 404 "No se encontró datos" = no data for that CUIT; checked 2026-10-28 with dummy CUIT only)
- /centraldedeudores/v1.0/Deudas/{cuit}
- /centraldedeudores/v1.0/Deudas/Historicas/{cuit}
- /centraldedeudores/v1.0/Deudas/ChequesRechazados/{cuit}
Personal data: only query a CUIT the user gives you.

```
curl -s "https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/1?desde=2026-10-01&limit=5"
```
