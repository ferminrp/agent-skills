---
name: workflowy
description: >
  Read and write a Workflowy outline via its official REST API.
  Use when the user asks to access, list, read, search, export, create,
  update, move, complete/uncomplete, or delete Workflowy bullets/nodes,
  or mentions "workflowy". No native MCP connector exists — call the
  API over HTTP (curl) with a Bearer API key.
---

# Workflowy API

Access a Workflowy outline through its official REST API. There is no MCP connector; use `curl`.

## Authentication

Every request needs the header `Authorization: Bearer <API_KEY>`.

- **Never hardcode the key** in this skill or in scripts. Read it at call time from the environment variable `$WORKFLOWY_API_KEY`.
- If `$WORKFLOWY_API_KEY` is unset, ask the user for their key (or tell them to `export WORKFLOWY_API_KEY=...`). A key is generated at https://workflowy.com/api-key and does not expire.
- Base URL: `https://workflowy.com/api/v1`.

## Rate limit

**~1 request per minute.** Be efficient:
- To read a large part of the tree, prefer `nodes-export` (one call for everything) over walking children level by level.
- Plan the calls before firing them; avoid tight polling loops.

## Node model

```json
{
  "id": "874e6591-350f-4dbb-0f92-5310e59369d3",
  "name": "AI Messages",
  "note": null,
  "parent_id": null,
  "priority": 25,
  "completed": false,
  "data": { "layoutMode": "bullets" },
  "createdAt": 1757675725,
  "modifiedAt": 1757675725,
  "completedAt": null
}
```

`parent_id: null` means a root-level bullet. Timestamps are Unix seconds.

## `parent_id` / target values

`parent_id` (on create/list/move) accepts: a node ID or short ID, a Workflowy URL, `"None"` (root), `"inbox"`, `"calendar"`, `"today"`, `"tomorrow"`, `"next_week"`, or a date (`YYYY`, `YYYY-MM`, `YYYY-MM-DD`).

To list root-level bullets, use `parent_id=None`.

## Endpoints

All paths are under `https://workflowy.com/api/v1`.

| Action | Method | Path | Notes |
|--------|--------|------|-------|
| List children | GET | `/nodes` | query `parent_id` |
| Retrieve one | GET | `/nodes/:id` | returns `{"node": {...}}` |
| Export all | GET | `/nodes-export` | flat list of every node; rate-limited |
| Create | POST | `/nodes` | requires `name` |
| Update | POST | `/nodes/:id` | `name`, `note`, `layoutMode` |
| Move | POST | `/nodes/:id/move` | `parent_id`, `position` |
| Complete | POST | `/nodes/:id/complete` | — |
| Uncomplete | POST | `/nodes/:id/uncomplete` | — |
| Delete | DELETE | `/nodes/:id` | — |
| List targets | GET | `/targets` | returns `{"targets": [...]}` |

### Create parameters (POST `/nodes`)

- `name` (required, string)
- `parent_id` (optional; see values above)
- `note` (optional, string)
- `position` (optional): `"top"` or `"bottom"` (default `top`)
- `layoutMode` (optional): `"bullets"`, `"todo"`, `"h1"`, `"h2"`, `"h3"`, `"code-block"`, `"quote-block"`

Response: `{"item_id": "..."}`. Update/move/complete/delete return `{"status": "ok"}`.

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

Export the entire outline (use sparingly — rate limited):

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

Update / move / complete / delete:

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

curl -s -X DELETE "https://workflowy.com/api/v1/nodes/<ID>" \
  -H "Authorization: Bearer $WORKFLOWY_API_KEY"
```

## Tips

- Add `-w "\n[HTTP %{http_code}]\n"` to curl to surface the status code.
- Guessed hosts like `https://workflowy.com/api/bullets/...` return the marketing HTML page, not JSON. Always use the `/api/v1/...` paths above.
- Reference: https://workflowy.com/api-reference/
