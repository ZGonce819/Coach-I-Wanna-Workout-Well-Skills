"""Bounded, opt-in local coaching memory. Uses only the Python standard library."""

import argparse
from datetime import date, datetime, timezone
import json
import os
from pathlib import Path
import re
import sqlite3
import sys


MAX_RECORDS = 100
MAX_EVENTS = 20
MAX_HISTORY = 20
FIELDS = {
    "user": {"goal", "age_band", "experience", "schedule", "equipment",
             "preferences", "constraints", "height_cm", "weight_kg", "medical_context"},
    "plan": {"training", "nutrition", "mobility", "recovery"},
}


def storage_path():
    override = os.environ.get("WORKOUT_MEMORY_DIR")
    base = Path(override).expanduser() if override else (
        Path(os.environ["LOCALAPPDATA"]) / "CoachI WannaWorkout" if os.name == "nt"
        and os.environ.get("LOCALAPPDATA") else Path.home() / ".local/share/coach-i-wanna-workout"
    )
    if not base.is_absolute():
        raise ValueError("WORKOUT_MEMORY_DIR must be an absolute private directory")
    base = base.resolve()
    repository = Path(__file__).resolve().parents[2]
    if base == repository or repository in base.parents:
        raise ValueError("Memory must stay outside the skill repository")
    for ancestor in (base, *base.parents):
        if (ancestor / ".git").exists():
            raise ValueError("Memory must stay outside Git repositories")
    if any(part.lower() in {"public", "dropbox"} or part.lower().startswith("onedrive")
           for part in base.parts):
        raise ValueError("Use a private directory outside public or synced folders")
    return base / "memory.sqlite3"


def connect(path, create=False):
    if not path.exists() and not create:
        return None
    if create:
        path.parent.mkdir(parents=True, exist_ok=True)
        if os.name != "nt":
            path.parent.chmod(0o700)
    connection = sqlite3.connect(path, timeout=10, isolation_level=None)
    connection.execute("PRAGMA secure_delete=ON")
    connection.executescript("""
        CREATE TABLE IF NOT EXISTS settings (id INTEGER PRIMARY KEY CHECK(id=1),
            consent INTEGER NOT NULL, state TEXT NOT NULL);
        INSERT OR IGNORE INTO settings VALUES (1, 0, 'disabled');
        CREATE TABLE IF NOT EXISTS records (
            scope TEXT NOT NULL, field TEXT NOT NULL, body TEXT NOT NULL,
            PRIMARY KEY (scope, field));
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT, snapshot TEXT NOT NULL);
    """)
    if os.name != "nt":
        path.chmod(0o600)
    return connection


def read_records(connection):
    return [json.loads(row[0]) for row in connection.execute(
        "SELECT body FROM records ORDER BY scope, field")]


def state(connection):
    if connection is None:
        return {"consent": False, "state": "disabled", "records": 0}
    consent, mode = connection.execute("SELECT consent, state FROM settings WHERE id=1").fetchone()
    return {"consent": bool(consent), "state": mode,
            "records": connection.execute("SELECT COUNT(*) FROM records").fetchone()[0]}


def require_active(connection):
    current = state(connection)
    if not current["consent"] or current["state"] != "active":
        raise ValueError("Memory is not active; explicit consent and resume are required")


def validate_record(record):
    required = {"scope", "field", "value", "source_type", "source_ref", "occurred_at"}
    if not isinstance(record, dict) or set(record) != required:
        raise ValueError("Each record must contain exactly scope, field, value, source_type, source_ref, occurred_at")
    scope, field = record["scope"], record["field"]
    if not isinstance(scope, str) or not isinstance(field, str):
        raise ValueError("Scope and field must be strings")
    if scope not in {"user", "plan", "event"}:
        raise ValueError("Unknown scope")
    if scope in FIELDS and field not in FIELDS[scope]:
        raise ValueError("Unknown profile or plan field")
    if scope == "event" and not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,63}", field):
        raise ValueError("Event field must be a stable lowercase identifier")
    sources = {"user_report"} if scope == "user" else (
        {"user_report", "coach_plan"} if scope == "plan" else {"user_report", "measurement"})
    if record["source_type"] not in sources:
        raise ValueError("Source is not allowed for this scope; inference is not a user fact")
    if not isinstance(record["source_ref"], str) or not 1 <= len(record["source_ref"]) <= 200:
        raise ValueError("Source reference must contain 1-200 characters")
    if not isinstance(record["occurred_at"], str):
        raise ValueError("Use a YYYY-MM-DD observation date")
    date.fromisoformat(record["occurred_at"])
    if len(record["occurred_at"]) != 10:
        raise ValueError("Use a YYYY-MM-DD observation date")
    if record["value"] is None or not isinstance(record["value"], (str, int, float, bool, list, dict)):
        raise ValueError("Value must be a non-null JSON value")
    encoded = json.dumps(record["value"], ensure_ascii=False, allow_nan=False)
    limit = 6000 if scope == "plan" else 1000 if scope == "user" else 600
    if len(encoded) > limit:
        raise ValueError("Record is too large; store a concise summary")
    return record


def snapshot(connection):
    connection.execute("INSERT INTO history(snapshot) VALUES (?)",
                       (json.dumps(read_records(connection), ensure_ascii=False),))
    connection.execute("DELETE FROM history WHERE id NOT IN (SELECT id FROM history ORDER BY id DESC LIMIT ?)",
                       (MAX_HISTORY,))


def insert_record(connection, record):
    connection.execute("INSERT OR REPLACE INTO records VALUES (?, ?, ?)",
                       (record["scope"], record["field"], json.dumps(record, ensure_ascii=False)))


def apply(connection, payload):
    records = payload if isinstance(payload, list) else [payload]
    if not 1 <= len(records) <= 50:
        raise ValueError("An update must contain 1-50 records")
    records = [validate_record(record) for record in records]
    keys = [(record["scope"], record["field"]) for record in records]
    if len(set(keys)) != len(keys):
        raise ValueError("Duplicate fields in one update")
    old = {(record["scope"], record["field"]): record for record in read_records(connection)}
    changed = [record for record in records if {
        key: value for key, value in old.get((record["scope"], record["field"]), {}).items()
        if key != "updated_at"
    } != record]
    if not changed:
        return {"changed": 0}
    new_keys = set(keys) - set(old)
    if len(old) + len(new_keys) > MAX_RECORDS:
        raise ValueError("Memory limit reached; merge or forget low-value records first")
    snapshot(connection)
    now = datetime.now(timezone.utc).isoformat()
    for record in changed:
        insert_record(connection, {**record, "updated_at": now})
    events = connection.execute("SELECT field FROM records WHERE scope='event' ORDER BY json_extract(body, '$.occurred_at') DESC, json_extract(body, '$.updated_at') DESC, field DESC").fetchall()
    for (field,) in events[MAX_EVENTS:]:
        connection.execute("DELETE FROM records WHERE scope='event' AND field=?", (field,))
    return {"changed": len(changed), "undo_available": True}


def execute(args):
    path = storage_path()
    destructive = args.command in {"enable", "clear", "revoke", "forget"}
    if destructive and not args.confirm:
        raise ValueError("This command requires explicit user authorization and --confirm")
    if args.command == "status" and not path.exists():
        return state(None)
    connection = connect(path, create=args.command == "enable")
    if connection is None:
        if args.command in {"show", "context"}:
            return {"status": state(None), "records": []}
        raise ValueError("No memory store exists; enable only after explicit consent")
    try:
        connection.execute("BEGIN IMMEDIATE")
        if args.command == "status":
            result = state(connection)
        elif args.command == "enable":
            connection.execute("UPDATE settings SET consent=1, state='active' WHERE id=1")
            result = state(connection)
        elif args.command in {"show", "context"}:
            if args.command == "context":
                require_active(connection)
            records = read_records(connection)
            if args.scope:
                records = [record for record in records if record["scope"] == args.scope]
            if args.command == "context":
                stable = [record for record in records if record["scope"] != "event"]
                events = sorted((record for record in records if record["scope"] == "event"),
                                key=lambda record: (record["occurred_at"], record["updated_at"]), reverse=True)[:8]
                selected = []
                for record in stable + events:
                    if len(json.dumps(selected + [record], ensure_ascii=False)) <= args.max_chars:
                        selected.append(record)
                result = {"status": state(connection), "records": selected,
                          "omitted": len(records) - len(selected)}
            else:
                result = {"status": state(connection), "records": records}
        elif args.command == "apply":
            require_active(connection)
            payload = json.load(sys.stdin) if args.file == "-" else json.loads(
                Path(args.file).read_text(encoding="utf-8-sig"))
            result = apply(connection, payload)
        elif args.command == "undo":
            require_active(connection)
            previous = connection.execute("SELECT id, snapshot FROM history ORDER BY id DESC LIMIT 1").fetchone()
            if previous is None:
                raise ValueError("No update available to undo")
            connection.execute("DELETE FROM records")
            for record in json.loads(previous[1]):
                insert_record(connection, record)
            connection.execute("DELETE FROM history WHERE id=?", (previous[0],))
            result = {"undone": True}
        elif args.command in {"pause", "resume"}:
            if not state(connection)["consent"]:
                raise ValueError("Explicit consent is required before resuming or pausing")
            connection.execute("UPDATE settings SET state=? WHERE id=1",
                               ("paused" if args.command == "pause" else "active",))
            result = state(connection)
        elif args.command in {"clear", "forget", "revoke"}:
            if args.command == "forget":
                count = connection.execute("DELETE FROM records WHERE scope=? AND field=?",
                                           (args.scope, args.field)).rowcount
                result = {"deleted": count}
            else:
                if args.command == "clear" or args.delete:
                    connection.execute("DELETE FROM records")
                if args.command == "revoke":
                    connection.execute("UPDATE settings SET consent=0, state='disabled' WHERE id=1")
                result = state(connection)
            connection.execute("DELETE FROM history")
        connection.commit()
        return result
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def context_budget(value):
    try:
        budget = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("Use an integer from 200 to 12000") from None
    if not 200 <= budget <= 12000:
        raise argparse.ArgumentTypeError("Use an integer from 200 to 12000")
    return budget


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("status", "undo", "pause", "resume"):
        commands.add_parser(command)
    for command in ("enable", "clear", "revoke", "forget"):
        sub = commands.add_parser(command)
        sub.add_argument("--confirm", action="store_true")
        if command == "revoke":
            sub.add_argument("--delete", action="store_true")
        if command == "forget":
            sub.add_argument("--scope", choices=("user", "plan", "event"), required=True)
            sub.add_argument("--field", required=True)
    for command in ("show", "context"):
        sub = commands.add_parser(command)
        sub.add_argument("--scope", choices=("user", "plan", "event"))
        if command == "context":
            sub.add_argument("--max-chars", type=context_budget, default=4000,
                             metavar="200..12000")
    sub = commands.add_parser("apply")
    sub.add_argument("--file", required=True, help="UTF-8 JSON file, or - for stdin")
    args = parser.parse_args()
    try:
        print(json.dumps(execute(args), ensure_ascii=False, allow_nan=False))
    except (ValueError, OSError, sqlite3.Error, TypeError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
