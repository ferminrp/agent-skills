---
name: tvmaze-series-tracker
description: >-
  Track favorite TV shows with the free TVmaze API: search and human-confirm
  before adding (poster + synopsis), list/remove shows, list today's and upcoming
  episodes, and run a silent daily cron that alerts only when a tracked show airs.
  Use when the user wants series tracking, episode air-day alerts, "add this show",
  "what airs today", TVmaze, TV calendar, or favorite-shows monitoring.
---

# TVmaze series tracker

Monitor favorite TV / streaming series using the public [TVmaze API](https://www.tvmaze.com/api).
No API key. License: data is [CC BY-SA](https://creativecommons.org/licenses/by-sa/4.0/) — always credit TVmaze (link back via show/episode URLs).

## When to use

- “Add Silo / Severance to my shows”
- “What episodes air today / this week?”
- “Alert me the day a new episode drops”
- Building a personal TV watchlist + daily digest for an agent runtime (Hermes, cron, launchd, GitHub Actions, etc.)

## API overview

| Item | Value |
|------|--------|
| Base URL | `https://api.tvmaze.com` |
| Auth | None |
| Format | JSON |
| Rate limit | At least **20 requests / 10 seconds** per IP (HTTP 429 → back off a few seconds) |
| Cache | Edge cache ~60 minutes |
| User-Agent | Set a descriptive UA identifying your agent/app |

### Endpoints used by this skill

| Goal | Method | Path |
|------|--------|------|
| Search shows (preferred) | GET | `/search/shows?q={query}` |
| Single fuzzy match (risky) | GET | `/singlesearch/shows?q={query}` |
| Show detail | GET | `/shows/{id}` |
| Episode list | GET | `/shows/{id}/episodes` (`?specials=1` optional) |
| Country broadcast day | GET | `/schedule?country={CC}&date={YYYY-MM-DD}` |
| Streaming / web day | GET | `/schedule/web?date={YYYY-MM-DD}` |

**Do not use `singlesearch` to auto-add favorites** — homonyms are common. Use `/search/shows` and **human confirmation**.

Show objects include `image.medium` / `image.original` (poster), `summary` (HTML), `network` or `webChannel`, `status`, `premiered`, `url`.

Episodes include `id`, `season`, `number`, `name`, `airdate` (`YYYY-MM-DD`), `airtime`, `airstamp` (ISO-8601), `url`.

Full endpoint notes: [references/tvmaze-api.md](references/tvmaze-api.md).

## Portable script

Bundled CLI (Python 3 stdlib only — no pip deps):

```bash
python skills/tvmaze-series-tracker/scripts/tvmaze_tracker.py <command>
```

Environment (optional):

| Variable | Default | Meaning |
|----------|---------|---------|
| `TVMAZE_STATE_DIR` | `./.tvmaze-state` (cwd) | Directory for JSON state |
| `TVMAZE_TZ_OFFSET` | `-3` | Hours from UTC for “today” and local clock display (e.g. Argentina = `-3`) |
| `TVMAZE_USER_AGENT` | `agent-skills-tvmaze-tracker/1.0` | HTTP User-Agent |

State files inside `TVMAZE_STATE_DIR`:

- `shows.json` — tracked favorites (`id`, `name`, `nick`, `network`, `image_medium`, `url`, `added_at`)
- `alerts.json` — dedupe map of notified `episode.id` → air date

### Commands

```bash
# Search candidates (JSON)
python scripts/tvmaze_tracker.py search "Severance" --limit 5

# Show detail + recent/upcoming episodes
python scripts/tvmaze_tracker.py show 44933

# Favorites
python scripts/tvmaze_tracker.py list
python scripts/tvmaze_tracker.py add 44933 --nick "Severance"
python scripts/tvmaze_tracker.py remove 44933   # or nick / exact name

# Human-facing text
python scripts/tvmaze_tracker.py today              # episodes airing "today" in TVMAZE_TZ_OFFSET
python scripts/tvmaze_tracker.py today --date 2026-07-31
python scripts/tvmaze_tracker.py upcoming --days 14

# Cron entrypoint: print alert only if something airs; empty stdout if nothing
python scripts/tvmaze_tracker.py check
python scripts/tvmaze_tracker.py check --date 2026-07-31 --force
```

Copy the script into your agent’s scripts directory if the runtime requires a fixed path (e.g. Hermes `~/.hermes/scripts/`).

## Workflow: add a show (required confirmation)

1. User asks to track a title (“add Silo”).
2. Run `search "Silo" --limit 5`.
3. Pick the best score; if the name is ambiguous, prepare top 2–3.
4. Reply with a validation card **before** writing state:
   - **Title** (premiere year · status · network/webChannel · genres)
   - **Short synopsis** (strip HTML from `summary`, 2–4 lines)
   - **Poster**: download `image.original` or `image.medium` and attach, or embed the URL
   - TVmaze `url`
   - Explicit question: “Is this the one?”
5. **Only after** explicit yes / “that one” / a chosen TVmaze id:
   ```bash
   python scripts/tvmaze_tracker.py add SHOW_ID [--nick "Friendly name"]
   ```
6. Confirm with `show SHOW_ID` and mention the next known air dates (if any).

Never auto-add from a single search hit without confirmation.

### Example validation reply shape

```text
[poster image]

**Silo** (2023 · Running · Apple TV)
Drama · Science-Fiction · Mystery
id: 38052

In a ruined and toxic future, thousands live in a giant silo...

https://www.tvmaze.com/shows/38052/silo

Is this the one you want me to track?
```

## Workflow: daily air-day alert

Goal: notify the user **on days when at least one tracked show has an episode** (`airdate == today` in the configured timezone). Stay silent otherwise.

1. Schedule a daily job (example: `0 9 * * *` local morning).
2. Run `python scripts/tvmaze_tracker.py check`.
3. Delivery rules for agent/cron runtimes:
   - **Non-empty stdout** → send as the user message (markdown ok).
   - **Empty stdout** → do not message (no “nothing today” spam).
   - Prefer **no LLM** on the cron path when the script already formats the text (saves tokens, avoids drift).
4. Dedupe: `check` records each `episode.id` in `alerts.json` so the same episode is not re-alerted. Use `--force` only for tests.

### Sample alert output

```text
📺 Series today — Friday 31 Jul

• **Silo** (Apple TV) — S03E05 _Memory_ · 21:00
  https://www.tvmaze.com/episodes/...

_Source: TVmaze_
```

### Hermes / similar agent notes

- Store state under a durable path (e.g. `$HERMES_HOME/state/tvmaze/`) via `TVMAZE_STATE_DIR`.
- Register a `no_agent` cron whose script only runs `check` and prints to stdout.
- Cron `--script` flags often disallow absolute paths — place a thin wrapper next to other agent scripts.

### Other schedulers

- **cron/systemd timer**: same `check` + notify bridge only if stdout non-empty.
- **GitHub Actions**: schedule workflow; post to Slack/Discord when step output is non-empty.
- **launchd / Task Scheduler**: identical contract.

## Other user intents

| User says | Action |
|-----------|--------|
| List my shows | `list` |
| Remove X | `remove` by id, nick, or name |
| What airs today? | `today` (always prints a status line even if empty) |
| What’s coming? | `upcoming --days N` |
| Dry-run alert | `check --force` |

## Pitfalls

- **Homonyms**: e.g. multiple “Silo” entries — always confirm with poster + year + network.
- **Streaming**: `airdate` is reliable for “day it drops”; `airtime` may be null — script falls back to `airstamp` converted with `TVMAZE_TZ_OFFSET`.
- **Missing future eps**: TVmaze may not have next-season dates yet → `upcoming` empty is normal; keep the show tracked.
- **Specials**: default episode list omits specials; use API `specials=1` only if the user wants them (extend script if needed).
- **Timezone**: “today” is defined by `TVMAZE_TZ_OFFSET`, not the host UTC date alone.
- **Rate limits**: small gaps between per-show episode fetches; on 429 sleep and retry.
- **Attribution**: keep “Source: TVmaze” (or equivalent) on user-facing digests.

## Quick curl cheatsheet

```bash
curl -sS -A "my-agent/1.0" "https://api.tvmaze.com/search/shows?q=Severance"
curl -sS -A "my-agent/1.0" "https://api.tvmaze.com/shows/44933"
curl -sS -A "my-agent/1.0" "https://api.tvmaze.com/shows/44933/episodes"
curl -sS -A "my-agent/1.0" "https://api.tvmaze.com/schedule/web?date=2026-07-31"
```

## Related

- Official docs: https://www.tvmaze.com/api
- This skill’s API digest: [references/tvmaze-api.md](references/tvmaze-api.md)
- Script: [scripts/tvmaze_tracker.py](scripts/tvmaze_tracker.py)
