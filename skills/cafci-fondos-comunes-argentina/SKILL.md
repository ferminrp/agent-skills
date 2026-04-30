---
name: cafci-fondos-comunes-argentina
description: >
  Consulta informacion publica de fondos comunes de inversion en Argentina via
  CAFCI, combinando catalogo JSON (fondos, clases, IDs y honorarios/fees),
  planilla diaria XLSX (patrimonio, valor cuotaparte, variaciones, market share)
  y ficha markdown por fondo (rendimientos por periodo). Usar cuando el usuario
  pida fondos comunes en Argentina, busqueda de fondo por nombre, fees/comisiones
  de un fondo, top fondos por patrimonio en una categoria, rendimientos por
  periodo, o mencione CAFCI.
---

# CAFCI Fondos Comunes Argentina

Skill para consultar información pública de fondos comunes de inversión en Argentina combinando tres fuentes oficiales de CAFCI. La API REST anterior (`api.pub.cafci.org.ar/tipo-renta`, `/fondo/...`, `/estadisticas/...`) fue **discontinuada en 2026-04** (HTTP 403 desde CloudFront edge). Estas tres fuentes la reemplazan.

## Fuentes de datos

| # | Endpoint | Para qué sirve | Formato | Tamaño |
|---|---|---|---|---|
| 1 | `https://estadisticas.cafci.org.ar/consulta-de-fondos.json` | Catálogo: fondos + clases + IDs + **honorarios/fees** + metadata | JSON | ~2.7 MB |
| 2 | `https://api.pub.cafci.org.ar/pb_get` | Snapshot diario: vcp, patrimonio, market share, variaciones | XLSX | ~900 KB |
| 3 | `https://defuddle.md/https://estadisticas.cafci.org.ar/fondos/{fondoId}?clase={claseId}` | Ficha individual: rendimientos por período (7d/1m/90d/180d/YTD/12m) | Markdown | ~2 KB |

Sin auth, sin token. Sólo `/pb_get` requiere headers de browser para no devolver 403.

## Setup inicial (una vez por día)

```bash
DATE=$(date +%F)
TMP="${TMPDIR:-/tmp}"
SKILL_DIR="${SKILL_DIR:-/Users/ripio/Documents/Github/agent-skills/skills/cafci-fondos-comunes-argentina}"

CATALOG="${TMP}/cafci-catalog-${DATE}.json"
DAILY_XLSX="${TMP}/cafci-daily-${DATE}.xlsx"
DAILY="${TMP}/cafci-daily-${DATE}.json"

# 1. Catálogo (1134 fondos, 4549 clases, fees, IDs, metadata)
[ -s "$CATALOG" ] || \
  curl -s "https://estadisticas.cafci.org.ar/consulta-de-fondos.json" -o "$CATALOG"

# 2. Snapshot diario (XLSX requiere headers)
[ -s "$DAILY_XLSX" ] || \
  curl -s "https://api.pub.cafci.org.ar/pb_get" \
    -H "origin: https://www.cafci.org.ar" \
    -H "referer: https://www.cafci.org.ar/" \
    -H "user-agent: Mozilla/5.0" \
    -o "$DAILY_XLSX"

# 3. Parsear XLSX a JSON normalizado
[ -s "$DAILY" ] || \
  python3 "${SKILL_DIR}/parse_cafci.py" "$DAILY_XLSX" > "$DAILY"
```

`parse_cafci.py` requiere `openpyxl` (`pip3 install openpyxl`).

## Operaciones comunes

### 1) Listar tipos de renta (catálogo de categorías)

```bash
jq '.filtros.tipo_renta' "$CATALOG"
# [{"id":2,"nombre":"Renta Variable"}, {"id":3,"nombre":"Renta Fija"}, ...]
```

### 2) Buscar fondo por nombre + listar clases con fees

```bash
jq '.fondos[]
    | select(.nombre | ascii_downcase | contains("ahorro"))
    | {id, nombre,
       tipo_renta: .tipo_renta.nombre,
       sociedad_gerente: .sociedad_gerente.nombre,
       clases: [.clases[] | {id, nombre,
                             fee_gerente: .honorarios.administracion_gerente,
                             fee_depositaria: .honorarios.administracion_depositaria,
                             ingreso: .honorarios.ingreso,
                             rescate: .honorarios.rescate}]}' "$CATALOG"
```

### 3) Listar fondos activos por tipo de renta

```bash
# tipo_renta.id 4 = Mercado de Dinero (ver paso 1 para el mapeo)
jq '.fondos[]
    | select(.tipo_renta.id == 4 and .estado == 1)
    | {id, nombre, sociedad_gerente: .sociedad_gerente.nombre, codigo_cnv}' "$CATALOG"
```

### 4) Top N por patrimonio en una categoría (usa DAILY)

```bash
# OJO: las categorías de DAILY combinan tipo_renta + moneda + región como string.
jq '[.fondos[] | select(.categoria == "Mercado de Dinero Peso Argentina")]
    | sort_by(.patrimonio) | reverse | .[0:10]
    | .[] | {nombre, patrimonio, market_share, variacion_dia_pct, variacion_mes_pct}' "$DAILY"
```

### 5) Ficha completa de un fondo+clase (combina las 3 fuentes)

```bash
FONDO_ID=1717
CLASE_ID=5772

# (a) Metadata + fees desde CATALOG
jq --argjson fid $FONDO_ID --argjson cid $CLASE_ID '
  .fondos[] | select(.id == $fid)
  | {id, nombre, codigo_cnv, objetivo, inicio, dias_liquidacion,
     sociedad_gerente: .sociedad_gerente.nombre,
     sociedad_depositaria: .sociedad_depositaria.nombre,
     tipo_renta: .tipo_renta.nombre, region: .region.nombre,
     horizonte: .horizonte.nombre, duration: .duration.nombre,
     clase: (.clases[] | select(.id == $cid)
             | {id, nombre, inversion_minima, honorarios,
                ticker_bloomberg, ticker_isin})}' "$CATALOG"

# (b) Rendimientos por período + valor cuotaparte (defuddle markdown)
curl -s "https://defuddle.md/https://estadisticas.cafci.org.ar/fondos/${FONDO_ID}?clase=${CLASE_ID}"

# (c) Snapshot diario por nombre exacto de la clase
CLASE_NOMBRE=$(jq -r --argjson fid $FONDO_ID --argjson cid $CLASE_ID \
  '.fondos[] | select(.id == $fid) | .clases[] | select(.id == $cid) | .nombre' "$CATALOG")
jq --arg n "$CLASE_NOMBRE" '.fondos[] | select(.nombre == $n)' "$DAILY"
```

### 6) Resolver fondoId/claseId desde un nombre

```bash
jq -r '.fondos[]
       | select(.nombre | ascii_downcase | contains("ieb estrategico"))
       | "\(.id)\t\(.nombre)\t" + ([.clases[] | "\(.id)=\(.nombre)"] | join(" | "))' "$CATALOG"
```

## Workflows recomendados

### A) Top N por patrimonio en categoría con fees

1. Top N desde `$DAILY` filtrando `categoria` (XLSX usa "Mercado de Dinero Peso Argentina", "Renta Fija Peso Argentina", etc).
2. Para cada `nombre` resultante, buscar la clase en `$CATALOG` por `clases[].nombre` exacto.
3. Joinear patrimonio + variaciones (DAILY) con fees + sociedad gerente (CATALOG).

### B) Ficha "todo en uno"

1. `(fondoId, claseId)` desde catálogo (paso 6).
2. Tres queries en paralelo: CATALOG (metadata + fees), DAILY (patrimonio actual + variaciones), defuddle (rendimientos por período).
3. Resumen accionable: nombre, sociedad gerente/depositaria, tipo de renta, **fees**, patrimonio, rendimientos.

### C) Si el usuario no especifica clase

- Mostrar las clases disponibles en `$CATALOG` y pedir cuál.
- Si hay una sola, continuar automáticamente.

## Mapeo de campos

### CATALOG (`/consulta-de-fondos.json`)

```
.generated_at        — timestamp
.total_fondos        — 1134
.total_clases        — 4549
.filtros             — catálogos: tipo_renta, region, horizonte, duration,
                       benchmark, moneda, sociedad_gerente, tipo_dinero,
                       tipo_renta_mixta (todos arrays de {id, nombre})
.fondos[]            — array de fondos
  .id, .nombre, .codigo_cnv, .estado (1=activo), .objetivo, .tipo_dinero,
  .valuacion, .dias_liquidacion, .inicio (YYYY-MM-DD), .mm_puro, .mm_indice,
  .sociedad_gerente {id, nombre}, .sociedad_depositaria {id, nombre},
  .moneda {id, nombre}, .tipo_renta {id, nombre}, .tipo_renta_mixta,
  .region {id, nombre}, .duration {id, nombre},
  .benchmark {id, nombre}, .horizonte {id, nombre}
  .clases[]
    .id, .nombre, .moneda {id, nombre}, .inversion_minima,
    .suscripcion, .liquidez, .rg384, .log_abierto,
    .ticker_bloomberg, .ticker_isin
    .honorarios.{ingreso, rescate, transferencia,
                 administracion_gerente, administracion_depositaria,
                 gasto_ordinario_gestion}     — strings, % anual
```

### DAILY (XLSX → JSON via `parse_cafci.py`)

```
.fecha_reporte       — YYYY-MM-DD del último día hábil publicado
.categorias[]        — 27 strings: "Renta Variable Peso Argentina", etc
                       (combina tipo_renta + moneda + región)
.fondos[]            — 4052 clases con datos diarios
  .nombre            — nombre completo de la clase (ej "Galileo Acciones - Clase A")
  .categoria         — categoría XLSX
  .moneda            — ARS / USD / USB
  .region            — Arg / Lat / Glo
  .horizonte         — Cor / Med / Largo / Flex
  .fecha             — fecha del valor cuotaparte
  .vcp_actual        — valor cuotaparte hoy
  .vcp_anterior      — valor cuotaparte día hábil anterior
  .variacion_dia_pct — % vs día anterior
  .vcp_reexp_pesos   — vcp re-expresado en pesos (= vcp_actual para ARS)
  .variacion_mes_pct — % vs último día del mes anterior
  .variacion_ytd_pct — % vs cierre del año anterior
  .variacion_12m_pct — % vs hace 12 meses
  .cantidad_cuotapartes
  .patrimonio        — patrimonio neto en moneda del fondo
  .market_share      — % del total
  .depositaria       — nombre de la sociedad depositaria
  .codigo_cnv        — código CNV
```

### defuddle.md (ficha individual)

Markdown con tablas:
- **Rendimiento histórico**: Valor Cuotaparte + 7 días, 1 mes, 90 días, 180 días, En el año, 12 meses.
- **Valores al [fecha]**: patrimonio bajo administración, valor cuotaparte.
- **Composición de Cartera**: sólo la fecha (la composición real no se sirve estática).
- **Honorarios y Comisiones**: gerente, depositaria, ingreso, egreso, transferencia, gastos ordinarios, comisión de éxito.
- **Datos del Fondo**: Administradora, Depositaria, Tipo de Renta, Tipo de DD, Región, Benchmark, Horizonte, Duration, Moneda, Código CNV.
- **Inversión mínima** (con moneda).
- **Plazo de Liquidación**.

## Limitaciones conocidas

- **Composición de cartera real**: no disponible públicamente (defuddle muestra el bloque pero la composición se carga vía JS).
- **Series temporales arbitrarias**: el snapshot diario sólo expone día actual + ayer + mes anterior + fin de año + año pasado. No hay endpoint público de histórico libre.
- **API REST anterior** (`api.pub.cafci.org.ar/tipo-renta`, `/fondo/...`, `/estadisticas/informacion/diaria/...`): caída desde 2026-04 (HTTP 403 deliberado en CloudFront). No usar ni intentar reactivar.
- **CATALOG vs DAILY**: CATALOG cuenta fondos únicos (1134), DAILY cuenta clases (4052). Para joinear, usar `clases[].nombre` (CATALOG) ↔ `fondos[].nombre` (DAILY) — son strings exactos.
- **Tipo de renta**: en CATALOG es solo "Renta Variable"; en DAILY es "Renta Variable Peso Argentina" (con moneda+región). No son intercambiables como filtro.

## Manejo de errores

- `403 "Route not allowed"` en `api.pub.cafci.org.ar`: faltan los headers `origin`, `referer`, `user-agent`.
- `total_fondos == 0` en CATALOG: probablemente bajó la API; reintentar.
- Fondo en CATALOG sin match en DAILY: revisar `.estado` (debe ser 1) y nombre exacto de la clase.
- defuddle.md timeout: reintentar 1 vez con espera breve.

## Presentación de resultados

- Empezar con un resumen corto y accionable.
- Para listados/top N: incluir patrimonio, market share, variación día y fees clave (gerente).
- Para ficha: incluir nombre, sociedad gerente/depositaria, tipo de renta, fees completos, patrimonio actual, rendimiento del último mes y año.
- Si los datos del día aún no se publicaron (fin de semana / feriado): aclarar fecha del último reporte.
