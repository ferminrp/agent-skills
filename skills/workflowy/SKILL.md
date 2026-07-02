---
name: workflowy
description: >
  Read and write a Workflowy outline via its official REST API.
  Use when the user asks to access, list, read, export, create,
  update, move, complete/uncomplete, or delete Workflowy bullets/nodes,
  discover shortcuts/targets, or mentions "workflowy". No native MCP
  connector exists — call the API over HTTP (curl) with a Bearer API key.
---

# Workflowy API

Access a Workflowy outline through its official REST API. There is no MCP connector; use `curl`.

**Detailed reference:** `references/api-reference.md` (load on demand for full parameter tables and schemas).

## Authentication

Every request needs the header `Authorization: Bearer <API_KEY>`.

- **Never hardcode the key** in this skill or in scripts. Read it at call time from the environment variable `$WORKFLOWY_API_KEY`.
- If `$WORKFLOWY_API_KEY` is unset, ask the user for their key (or tell them to `export WORKFLOWY_API_KEY=...`). A key is generated at https://workflowy.com/api-key and does not expire.
- Base URL: `https://workflowy.com/api/v1`.

## Rate limits

- **`GET /nodes-export`:** 1 request per minute (large response). Prefer this over walking the tree level by level when you need most of the outline.
- **All other endpoints:** no documented rate limit; still avoid tight polling loops.

## Node model

### Standard node (list, retrieve, create/update responses)

```json
{
  "id": "874e6591-350f-4dbb-0f92-5310e59369d3",
  "name": "AI Messages",
  "note": null,
  "parent_id": null,
  "priority": 25,
  "data": { "layoutMode": "bullets" },
  "createdAt": 1757675725,
  "modifiedAt": 1757675725,
  "completedAt": null
}
```

Completion state is tracked by `completedAt` (Unix seconds, or `null` if not completed). There is **no** `completed` field in standard responses.

### Export node (`GET /nodes-export` only)

Same fields as above, plus `"completed": false`. Use export when you need a boolean completion flag alongside the full flat list.

`parent_id: null` means a root-level bullet. Timestamps are Unix seconds.

## Sorting and hierarchy

`GET /nodes` and `GET /nodes-export` return nodes **unordered**. Sort siblings by `priority` (lower = first) and rebuild the tree using `parent_id`.

## `parent_id` / target values

`parent_id` (on create, list, move) and `:id` (on retrieve) accept:

- Full node ID or 12-character short ID from a Workflowy URL
- Workflowy URL (e.g. `https://workflowy.com/#/d8754237b505`)
- User-defined **shortcut keys** (e.g. `"home"`, `"rd"`) — discover with `GET /targets`
- `"None"` — root outline
- `"inbox"` — built-in inbox
- `"calendar"`, `"today"`, `"tomorrow"`, `"next_week"`
- Calendar dates: `"YYYY"`, `"YYYY-MM"`, `"YYYY-MM-DD"`

To list root-level bullets, use `parent_id=None`.

### Calendar targets

| Operation | Behavior |
|-----------|----------|
| Create / Move | Calendar nodes are created on demand if missing |
| List (`GET /nodes`) | Calendar targets return **404** if the node does not exist yet — create or move into it first |
| Retrieve (`GET /nodes/:id`) | Resolves existing calendar nodes only; does not create missing ones |

## Targets (shortcuts)

`GET /targets` returns system targets (`inbox`, etc.) and user-defined shortcuts.

```json
{
  "targets": [
    { "key": "home", "type": "shortcut", "name": "My Home Page" },
    { "key": "inbox", "type": "system", "name": "Inbox" }
  ]
}
```

- `key` — use as `parent_id` or path `:id`
- `type` — `"shortcut"` (user-defined) or `"system"` (built-in)
- `name` — node title; `null` for system targets whose node has not been created yet

## Markdown in `name` (create / update)

The API parses markdown in `name` on `POST /nodes` and `POST /nodes/:id`:

- **Multiline:** first line becomes the node; lines separated by `\n\n` become child nodes (`\n` alone is joined into a space).
- **Inline styles:** `**bold**`, `*italic*`, `~~strike~~`, `` `code` ``, `[text](url)`, `[YYYY-MM-DD]`, `[YYYY-MM-DD HH:MM]`.
- **Layout prefixes:** `#` → h1, `##` → h2, `###` → h3, `- [ ]` / `- [x]` → todo, ` ``` ` → code-block, `>` → quote-block. Alternatively pass `layoutMode` explicitly.

## Finding content (no search endpoint)

There is no search API. Options:

1. **`GET /nodes-export`** — one call for everything (1 req/min limit), then filter client-side.
2. **`GET /nodes`** — walk children level by level when you know the parent; more calls but no export rate limit.

## Endpoints

All paths are under `https://workflowy.com/api/v1`.

| Action | Method | Path | Notes |
|--------|--------|------|-------|
| List children | GET | `/nodes` | query `parent_id`; sort by `priority` |
| Retrieve one | GET | `/nodes/:id` | returns `{"node": {...}}`; `:id` accepts IDs, shortcuts, calendar targets |
| Export all | GET | `/nodes-export` | flat list; 1 req/min; includes `completed` |
| Create | POST | `/nodes` | requires `name` |
| Update | POST | `/nodes/:id` | `name`, `note`, `layoutMode` |
| Move | POST | `/nodes/:id/move` | `parent_id`, `position` |
| Complete | POST | `/nodes/:id/complete` | — |
| Uncomplete | POST | `/nodes/:id/uncomplete` | — |
| Delete | DELETE | `/nodes/:id` | permanent |
| List targets | GET | `/targets` | shortcuts + system targets |

### Create parameters (POST `/nodes`)

- `name` (required, string)
- `parent_id` (optional; see values above)
- `note` (optional, string)
- `position` (optional): `"top"` or `"bottom"` (default `top`)
- `layoutMode` (optional): `"bullets"`, `"todo"`, `"h1"`, `"h2"`, `"h3"`, `"code-block"`, `"quote-block"`

Response: `{"item_id": "..."}`. Update/move/complete/uncomplete/delete return `{"status": "ok"}`.

## Examples

List root-level bullets:

```bash
curl -s -G "https://workflowy.com/api/v1/nodes" \
  -H "Authorization: Bearer $WORKFLOWY_API_KEY" \
  --data-urlencode "parent_id=None"
```

List children of a specific node:

```bash
curl -s -G "https://workflowy.com/api/v1/nodes" \
  -H "Authorization: Bearer $WORKFLOWY_API_KEY" \
  --data-urlencode "parent_id=<NODE_ID>"
```

Retrieve one node (by ID, shortcut, or calendar target):

```bash
curl -s "https://workflowy.com/api/v1/nodes/today" \
  -H "Authorization: Bearer $WORKFLOWY_API_KEY"

curl -s "https://workflowy.com/api/v1/nodes/<NODE_ID>" \
  -H "Authorization: Bearer $WORKFLOWY_API_KEY"
```

List targets (discover shortcuts):

```bash
curl -s "https://workflowy.com/api/v1/targets" \
  -H "Authorization: Bearer $WORKFLOWY_API_KEY"
```

Export the entire outline (1 req/min):

```bash
curl -s "https://workflowy.com/api/v1/nodes-export" \
  -H "Authorization: Bearer $WORKFLOWY_API_KEY"
```

Create a bullet:

```bash
curl -s -X POST "https://workflowy.com/api/v1/nodes" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $WORKFLOWY_API_KEY" \
  -d '{"parent_id":"inbox","name":"Hello API","note":"optional","position":"top"}'
```

Update / move / complete / uncomplete / delete:

```bash
curl -s -X POST "https://workflowy.com/api/v1/nodes/<ID>" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $WORKFLOWY_API_KEY" \
  -d '{"name":"New title"}'

curl -s -X POST "https://workflowy.com/api/v1/nodes/<ID>/move" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $WORKFLOWY_API_KEY" \
  -d '{"parent_id":"<TARGET>","position":"bottom"}'

curl -s -X POST "https://workflowy.com/api/v1/nodes/<ID>/complete" \
  -H "Authorization: Bearer $WORKFLOWY_API_KEY"

curl -s -X POST "https://workflowy.com/api/v1/nodes/<ID>/uncomplete" \
  -H "Authorization: Bearer $WORKFLOWY_API_KEY"

curl -s -X DELETE "https://workflowy.com/api/v1/nodes/<ID>" \
  -H "Authorization: Bearer $WORKFLOWY_API_KEY"
```

## Tips

- Add `-w "\n[HTTP %{http_code}]\n"` to curl to surface the status code.
- Guessed hosts like `https://workflowy.com/api/bullets/...` return the marketing HTML page, not JSON. Always use the `/api/v1/...` paths above.
- Official docs: https://workflowy.com/api-reference/
