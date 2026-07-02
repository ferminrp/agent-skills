# Workflowy API Reference (snapshot)

Source: https://workflowy.com/api-reference/ — load this file when you need full parameter tables or response shapes.

Base URL: `https://workflowy.com/api/v1`  
Auth: `Authorization: Bearer <API_KEY>`

---

## Node object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique node identifier |
| `parent_id` | string \| null | Parent node ID; `null` for root |
| `name` | string | Bullet text; supports inline HTML (`<b>`, `<i>`, `<s>`, `<code>`, `<a>`) |
| `note` | string \| null | Note below the bullet |
| `priority` | number | Sort order among siblings (lower = first) |
| `data.layoutMode` | string | `"bullets"`, `"todo"`, `"h1"`, `"h2"`, `"h3"`, `"code-block"`, `"quote-block"` |
| `createdAt` | number | Unix timestamp (seconds) |
| `modifiedAt` | number | Unix timestamp (seconds) |
| `completedAt` | number \| null | Completion timestamp; `null` if not completed |
| `completed` | boolean | **Export only** (`GET /nodes-export`) |

---

## Target object

| Field | Type | Description |
|-------|------|-------------|
| `key` | string | Identifier (e.g. `"home"`, `"inbox"`, `"today"`) |
| `type` | string | `"shortcut"` or `"system"` |
| `name` | string \| null | Node title; `null` if system target node not yet created |

---

## Target / parent_id values

Accepted by `parent_id` (create, list, move) and by `:id` (retrieve, where noted):

| Value | Meaning |
|-------|---------|
| Full node ID | e.g. `6ed4b9ca-256c-bf2e-bd70-d8754237b505` |
| Short ID | 12-char ID from Workflowy URL |
| Workflowy URL | e.g. `https://workflowy.com/#/d8754237b505` |
| Shortcut key | User-defined, e.g. `"home"`, `"rd"` |
| `"None"` | Root outline |
| `"inbox"` | Built-in inbox |
| `"calendar"` | Calendar root |
| `"today"` | Today's calendar node |
| `"tomorrow"` | Tomorrow's calendar node |
| `"next_week"` | First day of next week (per user setting) |
| `"YYYY"` | Year node |
| `"YYYY-MM"` | Month node |
| `"YYYY-MM-DD"` | Day node |

### Calendar behavior by endpoint

| Endpoint | Calendar missing? |
|----------|-------------------|
| `POST /nodes`, `POST /nodes/:id/move` | Created on demand |
| `GET /nodes` (list) | Returns 404 |
| `GET /nodes/:id` (retrieve) | Returns 404; does not create |

---

## Endpoints

### POST /nodes — Create

**Body:**

| Param | Required | Description |
|-------|----------|-------------|
| `name` | yes | Node text (markdown parsed; see below) |
| `parent_id` | no | Where to create (default root) |
| `note` | no | Note content |
| `position` | no | `"top"` (default) or `"bottom"` |
| `layoutMode` | no | Display mode (see Node object) |

**Response:** `{"item_id": "<uuid>"}`

### POST /nodes/:id — Update

**Body:** any of `name`, `note`, `layoutMode` (partial update).

**Response:** `{"status": "ok"}`

### GET /nodes/:id — Retrieve

**Path `:id`:** full ID, short ID, or calendar target (does not create missing calendar nodes).

**Response:** `{"node": { ... }}`

### GET /nodes — List children

**Query:** `parent_id` (see target values).

**Response:** `{"nodes": [ ... ]}` — unordered; sort by `priority`.

Calendar `parent_id` returns 404 if node does not exist.

### DELETE /nodes/:id — Delete

Permanent. **Response:** `{"status": "ok"}`

### POST /nodes/:id/move — Move

**Body:**

| Param | Required | Description |
|-------|----------|-------------|
| `parent_id` | no | New parent (calendar created on demand) |
| `position` | no | `"top"` (default) or `"bottom"` |

**Response:** `{"status": "ok"}`

### POST /nodes/:id/complete — Complete

**Response:** `{"status": "ok"}`

### POST /nodes/:id/uncomplete — Uncomplete

**Response:** `{"status": "ok"}`

### GET /nodes-export — Export all

Flat list of every node. Rebuild tree with `parent_id` + `priority`. Includes `completed` boolean.

**Rate limit:** 1 request per minute.

**Response:** `{"nodes": [ ... ]}`

### GET /targets — List targets

No parameters. Returns shortcuts and system targets.

**Response:** `{"targets": [ ... ]}`

---

## Markdown in `name` (create / update)

### Multiline

- First line → parent node
- Lines after `\n\n` → child nodes
- Single `\n` → joined into a space

### Inline styles

| Markdown | Result |
|----------|--------|
| `**text**` | bold |
| `*text*` | italic |
| `~~text~~` | strikethrough |
| `` `text` `` | inline code |
| `[text](url)` | hyperlink |
| `[YYYY-MM-DD]` | date |
| `[YYYY-MM-DD HH:MM]` | date with time (user timezone) |

### Layout prefixes

| Markdown | layoutMode |
|----------|------------|
| `# text` | h1 |
| `## text` | h2 |
| `### text` | h3 |
| `- text` | bullets |
| `- [ ] text` | todo (uncompleted) |
| `- [x] text` | todo (completed) |
| ` ```code``` ` | code-block |
| `> text` | quote-block |
