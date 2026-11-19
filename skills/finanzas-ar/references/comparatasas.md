# comparatasas (REST/markdown) — v2
Site: https://comparatasas.ar (Nuxt, open source: github.com/enzonotario/comparatasas.ar). No API of its own: the frontend calls **ArgentinaDatos** directly from the browser.
Data base: https://api.argentinadatos.com/v1/finanzas · Auth: none · Rate limit not published (be gentle; /fci/fondos is ~30 MB).
All below verified 2026-10-28 (HTTP 200) unless marked.

## Data endpoints the frontend uses (primary)
| Endpoint | Page | Key fields |
|---|---|---|
| /fci/comparatasas | /fondos (curated list; 55 classes on 2026-10-28) | fechaActualizacion, fondos[]{nombre, administradora, tipoRenta ("Mercado de Dinero","Renta Fija","Renta Mixta","Renta Variable","Retorno Total"), moneda ("Peso Argentino"/"Dolar Estadounidense"), horizonte, patrimonio, honorarios, inversionMinima, plazoLiquidacionDias, rendimientos{valorCuotaparte, variacionDiariaPct, ultimos7Dias, unMes, noventaDias, enElAnio, doceMeses, tnaEstimada (% , from unMes), tnaEstimadaDias, tnaEstimadaPeriodo}} (no slug field) |
| /fci/fondos | full CNV universe (~30 MB, avoid) | same shape |
| /fci/fondos/{slug} | /fondos/{slug} | one fund, same fields (slug = sitemap path, e.g. balanz-capital-money-market-clase-a) |
| /fci/fondos/{slug}/historico | fund chart | fondoId, claseId, nombre, fechaActualizacion, historico[]{fecha, valorCuotaparte, patrimonio, retornoDiario, retornoAcumulado} (~770 KB) |
| /fci/otros/ultimo | / cuentas remuneradas | fondo, tna, tea (decimals), tope, fecha, condiciones, plazoMinDias |
| /fci/otros/{slug}/ (lowercase, e.g. belo) | /cuentas-billeteras/{slug} | history rows: tna, tea, tope, fecha, condiciones |
| /cuentas-remuneradas-usd/ | /usd | entidad, tasa (decimal), tope |
| /tasas/plazoFijo | /plazos-fijos | entidad, tnaClientes, tnaNoClientes (decimals), tasas[] |
| /tasas/plazoFijoPrecancelable , /tasas/plazoFijoUvaPagoPeriodico | /plazos-fijos UVA | entidad, enlace, tasas[] |
| /letras | /lecaps | fechaActualizacion, letras[]{ticker, precioArs, tnaPorcentaje, teaPorcentaje, temPorcentaje, fechaVencimiento} |
| /bonos-cer | /bonos-cer | bonos[]{ticker, precioArs, tirPorcentaje, fechaVencimiento, volumen} |
| /cauciones/{ars\|usd} | /cauciones | plazo (days), tasaActual (%), tasaMinDia, tasaMaxDia, montoContado, fechaOperacion. (/cauciones alone = 404) |
| /rendimientos | /criptomonedas | entidad, rendimientos[{moneda, apy (%), fecha}] |
| /criptopesos/ | /criptopesos | token, entidad, tna |
| /fal/ | /fal | alternativas[] (fondos de ahorro previsional) |
| /remesas | /remesas | remesas[]{compania, costos...} |
| /creditos/prestamosPersonales/ , /creditos/hipotecariosUva/ | préstamos | entidad, tna, tea, cftTea |
| /creditos/prestamosPersonalesBcra/ | préstamos | codigoEntidad, entidad, producto, teaMax, cftTeaMax, metadata (~2.3k rows) |
| /brokers/comisiones/ , /cobros/comisiones/ | comisiones | fechaActualizacion, comisiones[]{entidad, producto, ...; brokers: tasa, comisionMinima; cobros: arancel, medioPago} |
| /rem/ultimo | metodología/REM | BCRA REM rows: indicador, periodo, mediana, promedio, percentil* |

## Site-hosted static JSON
| URL | Fields |
|---|---|
| https://comparatasas.ar/api/fci/nominal-tna.json | generatedAt, bySlug{slug:{tna, tea, retorno30d, estimate}} (decimals; has outliers, prefer tnaEstimada above) |
| https://comparatasas.ar/api/analytics/*.json | site click analytics (in repo; not useful) |

## Markdown / llms
- /llms.txt: index only (no data). /llms-full.txt: 404.
- `Accept: text/markdown` works only on /, /about, /contact, /privacy, /metodologia, /sumarse (descriptive text, no rates). Data pages return HTML. Pages redirect 308 to trailing slash.

## Example: top peso money market by TNA
```
curl -s https://api.argentinadatos.com/v1/finanzas/fci/comparatasas | jq -r '[.fondos[]|select(.tipoRenta=="Mercado de Dinero" and (.moneda|test("Peso")))]|sort_by(-.rendimientos.tnaEstimada)|.[:5][]|"\(.nombre)\t\(.rendimientos.tnaEstimada)%"'
```
(2026-10-28: Vinci Compass Liquidez F 20.85%, Vinci D 20.60%, Allaria Ahorro E 19.95%.)
Best cuenta remunerada: `curl -s https://api.argentinadatos.com/v1/finanzas/fci/otros/ultimo | jq 'sort_by(-.tna)[:5]'`. Best LECAP TEA: `curl -s https://api.argentinadatos.com/v1/finanzas/letras | jq '.letras|sort_by(-.teaPorcentaje)'`.
