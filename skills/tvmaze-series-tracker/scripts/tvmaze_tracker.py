#!/usr/bin/env python3
"""TVmaze favorites tracker for AI agents (stdlib only).

API: https://api.tvmaze.com  (CC BY-SA — credit TVmaze)

Env:
  TVMAZE_STATE_DIR   default: ./.tvmaze-state
  TVMAZE_TZ_OFFSET   hours from UTC for "today" (default: -3)
  TVMAZE_USER_AGENT  HTTP User-Agent

Commands:
  search <query> [--limit N]
  show <id>
  list | add <id> [--nick ...] | remove <key>
  today [--date YYYY-MM-DD]
  upcoming [--days N]
  check [--date YYYY-MM-DD] [--force]   # cron: silent if nothing new
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from html import unescape
from pathlib import Path
from typing import Any

BASE = "https://api.tvmaze.com"


def _env_state_dir() -> Path:
    return Path(os.environ.get("TVMAZE_STATE_DIR") or "./.tvmaze-state").expanduser()


def _env_tz() -> timezone:
    try:
        hours = float(os.environ.get("TVMAZE_TZ_OFFSET", "-3"))
    except ValueError:
        hours = -3.0
    return timezone(timedelta(hours=hours))


def _ua() -> str:
    return os.environ.get("TVMAZE_USER_AGENT") or "agent-skills-tvmaze-tracker/1.0"


def _paths() -> tuple[Path, Path, Path]:
    d = _env_state_dir()
    return d, d / "shows.json", d / "alerts.json"


def _strip_html(s: str | None) -> str:
    if not s:
        return ""
    t = re.sub(r"(?is)<br\s*/?>", "\n", s)
    t = re.sub(r"(?is)</p>", "\n", t)
    t = re.sub(r"(?is)<[^>]+>", "", t)
    t = unescape(t)
    return re.sub(r"\s+\n", "\n", t).strip()


def _get(path: str, params: dict | None = None, retries: int = 3) -> Any:
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    req = urllib.request.Request(url, headers={"User-Agent": _ua(), "Accept": "application/json"})
    last_err: Exception | None = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode()
                return json.loads(raw) if raw else None
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code == 429:
                time.sleep(2 + attempt * 2)
                continue
            if e.code == 404:
                return None
            raise
        except Exception as e:  # noqa: BLE001
            last_err = e
            time.sleep(1 + attempt)
    raise SystemExit(f"TVmaze request failed: {path} ({last_err})")


def load_shows() -> dict:
    state_dir, shows_path, _ = _paths()
    state_dir.mkdir(parents=True, exist_ok=True)
    if not shows_path.exists():
        data = {"version": 1, "shows": [], "updated_at": None}
        save_shows(data)
        return data
    return json.loads(shows_path.read_text())


def save_shows(data: dict) -> None:
    state_dir, shows_path, _ = _paths()
    state_dir.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = datetime.now(_env_tz()).isoformat()
    tmp = shows_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    tmp.replace(shows_path)


def load_alert_state() -> dict:
    _, _, alert_path = _paths()
    if not alert_path.exists():
        return {"notified_episode_ids": {}, "last_run": None}
    return json.loads(alert_path.read_text())


def save_alert_state(data: dict) -> None:
    state_dir, _, alert_path = _paths()
    state_dir.mkdir(parents=True, exist_ok=True)
    tmp = alert_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    tmp.replace(alert_path)


def today_local() -> date:
    return datetime.now(_env_tz()).date()


def search_shows(query: str, limit: int = 8) -> list[dict]:
    rows = _get("/search/shows", {"q": query}) or []
    out = []
    for row in rows[:limit]:
        s = row.get("show") or {}
        img = s.get("image") or {}
        out.append(
            {
                "score": row.get("score"),
                "id": s.get("id"),
                "name": s.get("name"),
                "premiered": s.get("premiered"),
                "status": s.get("status"),
                "type": s.get("type"),
                "language": s.get("language"),
                "genres": s.get("genres") or [],
                "network": (s.get("network") or {}).get("name")
                or (s.get("webChannel") or {}).get("name"),
                "image_medium": img.get("medium"),
                "image_original": img.get("original"),
                "summary": _strip_html(s.get("summary")),
                "url": s.get("url"),
                "officialSite": s.get("officialSite"),
            }
        )
    return out


def fetch_show(show_id: int) -> dict | None:
    s = _get(f"/shows/{show_id}")
    if not s:
        return None
    img = s.get("image") or {}
    return {
        "id": s.get("id"),
        "name": s.get("name"),
        "premiered": s.get("premiered"),
        "status": s.get("status"),
        "type": s.get("type"),
        "language": s.get("language"),
        "genres": s.get("genres") or [],
        "network": (s.get("network") or {}).get("name")
        or (s.get("webChannel") or {}).get("name"),
        "image_medium": img.get("medium"),
        "image_original": img.get("original"),
        "summary": _strip_html(s.get("summary")),
        "url": s.get("url"),
        "officialSite": s.get("officialSite"),
        "runtime": s.get("runtime") or s.get("averageRuntime"),
    }


def fetch_episodes(show_id: int, specials: bool = False) -> list[dict]:
    params = {"specials": "1"} if specials else None
    eps = _get(f"/shows/{show_id}/episodes", params) or []
    out = []
    for e in eps:
        out.append(
            {
                "id": e.get("id"),
                "name": e.get("name"),
                "season": e.get("season"),
                "number": e.get("number"),
                "airdate": e.get("airdate") or None,
                "airtime": e.get("airtime") or None,
                "airstamp": e.get("airstamp") or None,
                "runtime": e.get("runtime"),
                "summary": _strip_html(e.get("summary")),
                "url": e.get("url"),
            }
        )
    return out


def ep_code(ep: dict) -> str:
    s, n = ep.get("season"), ep.get("number")
    if s is None:
        return "S??"
    if n is None:
        return f"S{int(s):02d} special"
    return f"S{int(s):02d}E{int(n):02d}"


def add_show(show_id: int, nick: str | None = None) -> dict:
    data = load_shows()
    for s in data["shows"]:
        if int(s["id"]) == int(show_id):
            return {"status": "exists", "show": s}
    detail = fetch_show(show_id)
    if not detail:
        raise SystemExit(f"Show id {show_id} not found on TVmaze")
    entry = {
        "id": detail["id"],
        "name": detail["name"],
        "nick": nick or detail["name"],
        "status": detail.get("status"),
        "network": detail.get("network"),
        "image_medium": detail.get("image_medium"),
        "url": detail.get("url"),
        "added_at": datetime.now(_env_tz()).isoformat(),
    }
    data["shows"].append(entry)
    data["shows"].sort(key=lambda x: (x.get("nick") or x.get("name") or "").lower())
    save_shows(data)
    return {"status": "added", "show": entry}


def remove_show(key: str) -> dict:
    data = load_shows()
    key_l = key.strip().lower()
    kept, removed = [], None
    for s in data["shows"]:
        if (
            str(s["id"]) == key
            or (s.get("nick") or "").lower() == key_l
            or (s.get("name") or "").lower() == key_l
        ):
            removed = s
        else:
            kept.append(s)
    if not removed:
        return {"status": "not_found", "key": key}
    data["shows"] = kept
    save_shows(data)
    return {"status": "removed", "show": removed}


def episodes_on_date(show_id: int, day: date, specials: bool = False) -> list[dict]:
    day_s = day.isoformat()
    return [e for e in fetch_episodes(show_id, specials=specials) if e.get("airdate") == day_s]


def collect_for_date(day: date, shows: list[dict] | None = None) -> list[dict]:
    data_shows = shows if shows is not None else load_shows()["shows"]
    hits = []
    for s in data_shows:
        sid = int(s["id"])
        time.sleep(0.15)
        for e in episodes_on_date(sid, day):
            hits.append({"show": s, "episode": e})
    hits.sort(key=lambda h: (h["episode"].get("airtime") or "99:99", h["show"].get("nick") or ""))
    return hits


def _local_time_label(ep: dict) -> str:
    if ep.get("airtime"):
        return f" · {ep['airtime']}"
    if ep.get("airstamp"):
        try:
            dt = datetime.fromisoformat(ep["airstamp"].replace("Z", "+00:00")).astimezone(_env_tz())
            return f" · {dt.strftime('%H:%M')}"
        except Exception:
            return ""
    return ""


def format_alert(day: date, hits: list[dict]) -> str:
    if not hits:
        return ""
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    months = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    head = f"TV shows today — {weekdays[day.weekday()]} {day.day} {months[day.month]}"
    lines = [head, ""]
    for h in hits:
        sh, ep = h["show"], h["episode"]
        name = sh.get("nick") or sh.get("name")
        net = sh.get("network") or ""
        code = ep_code(ep)
        title = ep.get("name") or "Episode"
        when = _local_time_label(ep)
        extra = f" ({net})" if net else ""
        lines.append(f"• **{name}**{extra} — {code} _{title}_{when}")
        if ep.get("url"):
            lines.append(f"  {ep['url']}")
    lines += ["", "_Source: TVmaze_"]
    return "\n".join(lines).strip() + "\n"


def format_upcoming(days: int = 14) -> str:
    data = load_shows()
    if not data["shows"]:
        return "No tracked shows. Add one after confirming the TVmaze match."
    start = today_local()
    end = start + timedelta(days=days)
    rows: list[tuple[str, str, str, str]] = []
    for s in data["shows"]:
        time.sleep(0.15)
        for e in fetch_episodes(int(s["id"])):
            ad = e.get("airdate")
            if not ad:
                continue
            if start.isoformat() <= ad <= end.isoformat():
                rows.append(
                    (
                        ad,
                        s.get("nick") or s.get("name") or "",
                        ep_code(e),
                        e.get("name") or "",
                    )
                )
    rows.sort()
    if not rows:
        return f"Nothing in the next {days} days among tracked shows."
    lines = [f"Upcoming episodes ({days}d)", ""]
    cur = None
    for ad, name, code, title in rows:
        if ad != cur:
            cur = ad
            y, m, d = ad.split("-")
            lines.append(f"**{y}-{m}-{d}**")
        lines.append(f"• {name} — {code} _{title}_")
    lines += ["", "_Source: TVmaze_"]
    return "\n".join(lines)


def cmd_check(args: argparse.Namespace) -> int:
    day = date.fromisoformat(args.date) if args.date else today_local()
    data = load_shows()
    if not data["shows"]:
        return 0

    hits = collect_for_date(day, data["shows"])
    st = load_alert_state()
    notified: dict = st.setdefault("notified_episode_ids", {})
    cutoff = (day - timedelta(days=60)).isoformat()
    notified = {k: v for k, v in notified.items() if isinstance(v, str) and v >= cutoff}
    st["notified_episode_ids"] = notified

    if not hits:
        st["last_run"] = datetime.now(_env_tz()).isoformat()
        st["last_date"] = day.isoformat()
        st["last_count"] = 0
        save_alert_state(st)
        return 0

    fresh = []
    for h in hits:
        eid = str(h["episode"]["id"])
        if eid in notified and not args.force:
            continue
        fresh.append(h)
        notified[eid] = day.isoformat()

    st["last_run"] = datetime.now(_env_tz()).isoformat()
    st["last_date"] = day.isoformat()
    st["last_count"] = len(fresh)
    save_alert_state(st)

    if not fresh:
        return 0

    sys.stdout.write(format_alert(day, fresh))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="TVmaze favorites tracker for agents")
    sub = p.add_subparsers(dest="cmd", required=True)

    ps = sub.add_parser("search")
    ps.add_argument("query")
    ps.add_argument("--limit", type=int, default=5)

    psh = sub.add_parser("show")
    psh.add_argument("id", type=int)

    sub.add_parser("list")

    pa = sub.add_parser("add")
    pa.add_argument("id", type=int)
    pa.add_argument("--nick")

    pr = sub.add_parser("remove")
    pr.add_argument("key")

    pt = sub.add_parser("today")
    pt.add_argument("--date")

    pu = sub.add_parser("upcoming")
    pu.add_argument("--days", type=int, default=14)

    pc = sub.add_parser("check")
    pc.add_argument("--date")
    pc.add_argument("--force", action="store_true")

    args = p.parse_args(argv)

    if args.cmd == "search":
        print(json.dumps(search_shows(args.query, args.limit), ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "show":
        detail = fetch_show(args.id)
        if not detail:
            print(json.dumps({"error": "not_found"}))
            return 1
        eps = fetch_episodes(args.id)
        today = today_local().isoformat()
        upcoming = [e for e in eps if e.get("airdate") and e["airdate"] >= today][:8]
        past = [e for e in eps if e.get("airdate") and e["airdate"] < today][-3:]
        print(json.dumps({"show": detail, "recent": past, "upcoming": upcoming}, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "list":
        print(json.dumps(load_shows(), ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "add":
        print(json.dumps(add_show(args.id, args.nick), ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "remove":
        print(json.dumps(remove_show(args.key), ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "today":
        day = date.fromisoformat(args.date) if args.date else today_local()
        hits = collect_for_date(day)
        msg = format_alert(day, hits)
        if msg:
            sys.stdout.write(msg)
        else:
            print(f"No episodes from tracked shows on {day.isoformat()}.")
        return 0

    if args.cmd == "upcoming":
        sys.stdout.write(format_upcoming(args.days) + "\n")
        return 0

    if args.cmd == "check":
        return cmd_check(args)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
