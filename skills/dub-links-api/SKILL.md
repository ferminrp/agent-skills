---
name: dub-links-api
description: >
  Integra endpoints de Links de Dub para crear, actualizar, eliminar,
  recuperar, listar, contar y operar en bulk sobre links cortos.
  Usar cuando el usuario pida "dub links api", "create link dub",
  "upsert link dub", "listar links", "count links", "bulk links",
  o consultas por linkId/domain+key/externalId.
---

# Dub Links API

Skill para integrar la API de Links de Dub con alcance estricto en endpoints `/links*`.

## API Overview

- **Base URL**: `https://api.dub.co`
- **Auth**: Bearer token obligatorio
- **Header**: `Authorization: Bearer <DUB_API_KEY>`
- **Response format**: JSON
- **Scope**: solo endpoints de Links
- **Docs**: `https://dub.co/docs/api-reference/endpoint/create-a-link`
- **Docs tokens (onboarding)**: `https://dub.co/docs/api-reference/tokens`
- **Snapshot local**: `references/openapi-spec.json`

## API Key Onboarding

Usar este flujo cuando el usuario aun no tenga API key:

1. Crear cuenta/workspace en Dub (si aplica).
2. Ir a la seccion de tokens del dashboard (segun docs):
   - `https://dub.co/docs/api-reference/tokens`
3. Generar una API key y exportarla en shell:
   - `export DUB_API_KEY="..."`
4. Verificar credenciales con un endpoint de Links:
   - `curl -s -H "Authorization: Bearer $DUB_API_KEY" "https://api.dub.co/links/count" | jq '.'`

Nota util de onboarding: si necesita alta inicial, se puede usar este referral:
`https://refer.dub.co/agents`

## Endpoints de Links

### 1) Create

- `POST /links`
- Crea un link en el workspace autenticado.
- Body minimo recomendado: `url`.

```bash
curl -s -X POST "https://api.dub.co/links" \
  -H "Authorization: Bearer $DUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}' | jq '.'
```

### 2) Update

- `PATCH /links/{linkId}`
- Actualiza un link existente por `linkId`.

```bash
curl -s -X PATCH "https://api.dub.co/links/{linkId}" \
  -H "Authorization: Bearer $DUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/new"}' | jq '.'
```

### 3) Upsert

- `PUT /links/upsert`
- Si existe un link con la misma URL lo devuelve/actualiza; si no, crea uno.

```bash
curl -s -X PUT "https://api.dub.co/links/upsert" \
  -H "Authorization: Bearer $DUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}' | jq '.'
```

### 4) Delete

- `DELETE /links/{linkId}`
- Elimina un link por `linkId`.

```bash
curl -s -X DELETE "https://api.dub.co/links/{linkId}" \
  -H "Authorization: Bearer $DUB_API_KEY" | jq '.'
```

### 5) Retrieve one

- `GET /links/info`
- Recupera un link por alguno de estos criterios:
  - `domain + key`
  - `linkId`
  - `externalId`

```bash
curl -s "https://api.dub.co/links/info?domain=acme.link&key=promo" \
  -H "Authorization: Bearer $DUB_API_KEY" | jq '.'
```

### 6) List

- `GET /links`
- Lista paginada con filtros.
- Query frecuentes: `domain`, `search`, `tagId`, `tagIds`, `tagNames`, `folderId`, `tenantId`, `page`, `pageSize`, `sortBy`, `sortOrder`.

```bash
curl -s "https://api.dub.co/links?page=1&pageSize=20&sortBy=createdAt&sortOrder=desc" \
  -H "Authorization: Bearer $DUB_API_KEY" | jq '.'
```

### 7) Count

- `GET /links/count`
- Devuelve cantidad de links para filtros dados.

```bash
curl -s "https://api.dub.co/links/count?domain=acme.link" \
  -H "Authorization: Bearer $DUB_API_KEY" | jq '.'
```

### 8) Bulk create

- `POST /links/bulk`
- Crea hasta 100 links.
- Body: array de objetos (cada item con `url` recomendado).

```bash
curl -s -X POST "https://api.dub.co/links/bulk" \
  -H "Authorization: Bearer $DUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '[{"url":"https://example.com/a"},{"url":"https://example.com/b"}]' | jq '.'
```

### 9) Bulk update

- `PATCH /links/bulk`
- Actualiza hasta 100 links.
- Body requiere `data`; seleccion via `linkIds` o `externalIds`.

```bash
curl -s -X PATCH "https://api.dub.co/links/bulk" \
  -H "Authorization: Bearer $DUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"linkIds":["lnk_123","lnk_456"],"data":{"archived":true}}' | jq '.'
```

### 10) Bulk delete

- `DELETE /links/bulk`
- Elimina hasta 100 links.
- Query requerida: `linkIds`.

```bash
curl -s -X DELETE "https://api.dub.co/links/bulk?linkIds=lnk_123,lnk_456" \
  -H "Authorization: Bearer $DUB_API_KEY" | jq '.'
```

## Campos clave

Campos frecuentes de respuesta (segun `LinkSchema`):

- `id`
- `domain`
- `key`
- `shortLink`
- `url`
- `createdAt`
- `updatedAt`
- `archived`
- `externalId`
- `tags`
- `folderId`

Resultados por endpoint:

- `GET /links`: array de links
- `GET /links/count`: numero
- Bulk endpoints: array/objeto segun operacion

## Workflow recomendado

1. Detectar intencion del usuario: create/update/upsert/delete/get/list/count/bulk.
2. Validar input minimo (por ejemplo `url`, `linkId`, filtros, ids bulk).
3. Ejecutar request con `curl -s` + header Bearer.
4. Parsear con `jq` y confirmar status logico de la operacion.
5. Responder primero con snapshot util:
   - `id`, `shortLink`, `url`, estado de archivo (`archived`) cuando aplique.
6. En listados, mostrar tabla corta con columnas relevantes.
7. Mantener alcance estricto en `/links*`.

## Error Handling

- **401/403**: token ausente, invalido o sin permisos.
- **404**: link no encontrado para `linkId` o criterio de `GET /links/info`.
- **422**: payload invalido (datos faltantes o formato incorrecto).
- **429**: rate limit; respetar `Retry-After` si existe.
- **Red/timeout**: reintentar hasta 2 veces con espera corta.
- **JSON inesperado**: mostrar salida minima cruda y advertir inconsistencia.

## Presenting Results

Formato recomendado:

- Resumen ejecutivo (accion + resultado).
- Tabla breve para multiples links:
  - `id | domain | key | shortLink | url | createdAt`
- En bulk:
  - total solicitado, total procesado, errores si existen.
- Aclarar que la data depende del workspace autenticado.

## Out of Scope

Esta skill no debe usar:

- Endpoints de analytics, events, conversions, partners, customers, commissions, payouts.
- Endpoints de domains, folders, tags.
- Endpoints `/tokens/*` (incluyendo `/tokens/embed/referrals`).

La pagina de tokens se usa solo para onboarding de API key, no como alcance operativo.

## OpenAPI Spec

Usar `references/openapi-spec.json` como referencia estable local para metodos, paths, parametros y schemas.
