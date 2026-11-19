# INDEC — Catálogo API-INDEC (REST, PostgREST) — v1
Base: https://api.indec.gob.ar/v1 · Portal: https://api.indec.gob.ar/ (BETA) · OpenAPI 3.1: `GET https://api.indec.gob.ar/v1/` (JSON, no auth; `/v1` → 301 a `/v1/`).
Verificado con token 2026-11-02: los 19 endpoints responden con datos reales (campos, filtros y último período abajo son de llamadas reales).

## Auth (token gratis)
JWT obligatorio en todo endpoint de datos; alcanza **solo** el header `Authorization: Bearer <token>` (sin apikey ni otros headers).
Dónde lo busca el agente: env `INDEC_API_TOKEN`, si no el archivo `~/.finanzas-ar/secrets/indec_token` (chmod 600). Nunca lo imprimas, loguees ni copies a archivos o respuestas:
`T="${INDEC_API_TOKEN:-$(cat ~/.finanzas-ar/secrets/indec_token 2>/dev/null)}"; curl -s -H "Authorization: Bearer $T" "https://api.indec.gob.ar/v1/ipc_nacional?order=periodo.desc&limit=2"`
Cómo sacar el tuyo (gratis): registrate en https://api.indec.gob.ar/ (email, nombre, organización) → código OTP por mail → generá el token en tu perfil (se muestra una sola vez; regenerar revoca el anterior; rol `basic`, vence a los ~6 meses). Guardalo con `umask 077; mkdir -p ~/.finanzas-ar/secrets; cat > ~/.finanzas-ar/secrets/indec_token` (pegás y Ctrl-D) o exportá `INDEC_API_TOKEN`.
Sin token: HTTP 401 `{"code":"42501","message":"permission denied for schema api"}`. **Si no hay token, usá el fallback del routing** (argentinadatos / monitorargy) y decilo.
Métodos: GET/HEAD/OPTIONS. CORS `*`. Rate limit: no documentado ni expuesto en headers.

## Parámetros comunes (PostgREST)
`select=col1,col2` · `limit` · `offset` · `order=col.desc` · filtros `col=op.valor` (eq, neq, gt, gte, lt, lte, like, ilike con `*`, `in.(a,b)`, `is.null`). Valores con espacios/acentos: URL-encodeá (`Nivel%20General`).
- **Tope 1000 filas por respuesta** (verificado: `limit=5000` devuelve 1000). Paginá con offset ordenando por la clave completa.
- `Prefer: count=exact` → total en `Content-Range: 0-0/234198` y status **206** si es parcial; sin ese header, 200.
- No hay DISTINCT: para ver valores de filtro, filtrá por un solo `periodo` y `select=` las columnas (dedupe local), o el tope de 1000 te corta la lista.
- Errores: `{code,message,details,hint}`; 400 (`42703` columna inexistente), 401 token.
- Cada columna de valor tiene una gemela `<col>_null` con el signo INDEC cuando el valor es null (`s` secreto estadístico, `///`, `...`, etc.). `observaciones` trae "* Dato provisorio" / "Dato provisorio".
- **Paths con guiones**: `/canasta-crianza`, `/estimador-mensual-de-actividad-economica-nivel-general`, `/estimador-mensual-de-actividad-economica-sectores`. El resto con guion bajo.
- **Columnas con mayúsculas**: `Periodo`, `Mes`, `Anio`, `valor_FOB`, `Peso_Neto`, `codigo_CPC_1`, `codigo_CLaNAE_2004`, `codigo_ClaNAE_2010` (ordená con `order=Periodo.desc`).
- `periodo` es texto: mensual `AAAAMM`, trimestral `AAAAqT` (`20262T`), semestral `AAAAsS` (`20261S`); población usa `fecha` (año; int en nacional, string en jurisdicción/departamento).
- Quirk: `/indice_salarios.valor` viene como **string con coma decimal** (`"10159,65"`); el resto numérico.

## Endpoints (verificado 2026-11-02; "último" = periodo más reciente, total = filas)
### Precios
- `/ipc_nacional` — último 202609, desde 201604, 234198 filas. Campos: clasificador, nivel, codigo, descripcion, periodo, anio, mes, indicador ("IPC base Dic16=100"), tipo_de_indicador, tipo_de_indicador_descripcion, region, unidad_de_medida, valor, valor_null, observaciones.
  region: Nacional, GBA, Pampeana, Noreste, Noroeste, Cuyo, Patagonia. nivel (clasificador): `Nivel General` (IPC, codigo `0`), `Categoría` (Bienes y servicios: B/S; Estacional, Núcleo y Regulados: E/N/R), `División` (COICOP Argentina 2019, codigo 01–12), `Grupo`, `Clase`, `Producto` (Precio promedio). tipo_de_indicador: Indice, v_m, v_ia, v_acum, Incidencia_m, Incidencia_ia, Incidencia_acum, Precio promedio.
  IPC general m/m: `?region=eq.Nacional&codigo=eq.0&tipo_de_indicador=eq.v_m&order=periodo.desc&limit=12`.
- `/valorizacion_canastas_cba_cbt` — último 202609, desde 201604, 1638 filas. Serie larga, region solo GBA. nivel/codigo/tipo_de_indicador: Adulto equivalente (CBA|CBT con tipo CBA/CBT, v_m, v_ia; ICE), Hogar (CBA H1–H3, CBT H1–H3, tipo Hogar 1–3). Valores en pesos.
- `/canasta-crianza` — último 202609, 41 filas. anio, Mes, Periodo, bys_/cuid_/tot_ × men1, 1a3, 4a5, 6a12 (+ `_null`). Ordená por `Periodo`.
- `/sipm_precios_mayoristas` — último 202609, 234260 filas. + operativo (SIPM), indicador (IPIM, IPIB, IPP), codigo_apertura. region: Total del país. nivel: Nivel general, Sector, Origen, Categoría de Tabulación, División, Grupo, Clase. tipo: Indice (base 1993, dic-15=100), v_m, v_ia, v_acum, incidencia.
- `/icc_precios_construccion` — último 202609, 14017 filas. + indicador (ICC), codigo_apertura, codigo_CPC_1. region GBA. nivel: Nivel general, Capitulo, Ítems, Grupo, Producto. tipo: Indice (base 1993, ene-22=100), v_m, v_ia, v_acum, incidencia.
- `/redeterminacion_precios_contratos_obras_publicas` — último 202609, 236192 filas. + indicador (Obra pública), operativo (ICC…), inciso, descripcion_inciso, codigo_CPC_1, codigo_CIUU_3, origen. tipo: Indice, v_m, v_ia, v_acum.
### Salarios y trabajo
- `/indice_salarios` — último 202608, desde 201510, 3406 filas. Sin region. codigo: 0 Nivel general, 100 Total registrado, 110 Sector privado registrado, 120 Sector público, 121 Subsector público nacional, 122 provincial, 200 Total no registrado. tipo: Indice (oct-2016=100), v_m, v_ia, v_acum. `valor` string con coma.
- `/mercado_trabajo_eph` — último 20262T (2.º trim 2026), desde 20162T, 41 filas. Solo `area_geografica_nom = T_31_A` (total 31 aglomerados; `area_geografica_cod` null). Tasas: actividad, empleo, empleo_formal, empleo_informal, desocupacion, ocupacion_demandante, subocupacion(_demandante|_no_demandante).
- `/pobreza_eph` — último 20261S (1.er sem 2026), desde 20162S, 20 filas. Solo T_31_A. tasa_pobreza_hogares/personas, tasa_indigencia_hogares/personas.
### Actividad
- `/estimador-mensual-de-actividad-economica-nivel-general` — último 202608, desde 200401, 1632 filas. tipo_de_indicador_descripcion: Índice serie original | desestacionalizada | tendencia-ciclo (tipo "Índice base 2004=100"); Var % interanual serie original, Var % mensual serie desestacionalizada, Var % mensual serie tendencia-ciclo (tipo "Variación porcentual").
- `/estimador-mensual-de-actividad-economica-sectores` — último 202608, 8512 filas. codigo A… (letras CIIU), solo índice serie original base 2004.
- `/ipi_manufacturero` — último 202608, 41344 filas. serie: Serie original | Serie desestacionalizada | Serie tendencia-ciclo. tipo: Índice, Variación interanual, Variación acumulada interanual, Variación intermensual. Nivel general: `codigo_CLaNAE_2004=eq.D`.
- `/ipi_minero` — último 202608, desde 201701, 17632 filas. serie: Serie Original | Serie Desestacionalizada | Serie Tendencia-Ciclo (mayúsculas distintas al manufacturero). tipo además: Unidades físicas.
### Comercio exterior
- `/comercio_exterior_exportacion_bienes` — último 202609, desde 198601, 779536 filas. Anio, Mes, Periodo, rubro_cod, subrubro_cod, pais_cod (ISO2), valor_FOB (USD), Peso_Neto (+ `_null`, `s` = secreto).
- `/comercio_exterior_importacion_bienes` — último 202609, 390315 filas. Anio, Mes, Periodo, uso_economico_cod, gce_cod, pais_cod, valor_CIF (USD), peso_neto.
- `/comercio_exterior_nomenclaturas` — diccionario sin período: nombre_columna (gce_cod, pais_cod, rubro_cod, subrubro_cod, uso_economico_cod), codigo, codigo_descripcion. Ej. `?nombre_columna=eq.pais_cod&codigo=eq.BR` → Brasil.
### Población
- `/proyecciones_poblacion_nacional_2022_2040` — fecha 2022–2040 (int), 3838 filas. edad, sexo_cod, sexo_nom, poblacion.
- `/proyecciones_poblacion_jurisdiccion_2022_2040` — fecha "2022"–"2040" (string), 19152 filas. jurisdiccion_cod/nom, sexo_cod/nom, edad_cod/nom (quinquenal "0 a 4 años").
- `/estimaciones_poblacion_departamento_2022_2035` — fecha hasta "2035", 14784 filas. jurisdiccion_cod/nom, departamento_cod/nom, rmba ("0"/"1"), sexo_cod/nom (Mujer/Varon), poblacion.

Frescura (2026-11-02): mensuales de precios y comercio a 202609; EMAE, IPI y salarios a 202608; EPH empleo 2T-2026, pobreza 1S-2026.

```
T="${INDEC_API_TOKEN:-$(cat ~/.finanzas-ar/secrets/indec_token 2>/dev/null)}"
curl -s -H "Authorization: Bearer $T" \
 "https://api.indec.gob.ar/v1/ipc_nacional?region=eq.Nacional&codigo=eq.0&tipo_de_indicador=eq.v_m&order=periodo.desc&limit=3&select=periodo,valor"
curl -s -o /dev/null -D - -H "Authorization: Bearer $T" -H "Prefer: count=exact" \
 "https://api.indec.gob.ar/v1/pobreza_eph?limit=1" | grep -i content-range
```
