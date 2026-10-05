"""Check the installed skill against the selected regional repository (stdlib only)."""

import argparse
import json
import os
from pathlib import Path
import re
import sys
from urllib.request import Request, urlopen


SKILL_ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "cn": {
        "repository": "https://gitee.com/zgonce819/Coach-I-Wanna-Workout-Well-Skills",
        "manifest": "https://raw.giteeusercontent.com/zgonce819/Coach-I-Wanna-Workout-Well-Skills/raw/main/Coach-I-Wanna-Workout-Well-Skills/version.json",
    },
    "global": {
        "repository": "https://github.com/ZGonce819/Coach-I-Wanna-Workout-Well-Skills",
        "manifest": "https://raw.githubusercontent.com/ZGonce819/Coach-I-Wanna-Workout-Well-Skills/main/Coach-I-Wanna-Workout-Well-Skills/version.json",
    },
}


def version_key(value):
    if not isinstance(value, str) or not re.fullmatch(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", value):
        raise ValueError("Expected a version such as 1.0.0")
    return tuple(map(int, value.split(".")))


def read_version(payload):
    value = json.loads(payload)["version"]
    version_key(value)
    return value


def default_config():
    base = Path(os.environ.get("LOCALAPPDATA") or os.environ.get("XDG_CONFIG_HOME") or (Path.home() / ".config"))
    return base / "coach-i-wanna-workout-well" / "update-settings.json"


def fetch_version(url, timeout):
    request = Request(url, headers={"User-Agent": "coach-i-wanna-workout-well-version-check", "Accept": "application/json"})
    with urlopen(request, timeout=timeout) as response:
        payload = response.read(65537)
    if len(payload) > 65536:
        raise ValueError("Remote manifest exceeds size limit")
    return read_version(payload.decode("utf-8-sig"))


def check(region, timeout=4):
    result = {"status": "unavailable", "region": region, "current_version": None, "latest_version": None}
    try:
        result["current_version"] = read_version((SKILL_ROOT / "version.json").read_text(encoding="utf-8-sig"))
        if region not in SOURCES:
            result["status"] = "needs_region"
            return result
        source = SOURCES[region]
        result.update(repository_url=source["repository"], manifest_url=source["manifest"])
        latest = fetch_version(source["manifest"], timeout)
        result["latest_version"] = latest
        current_key, latest_key = version_key(result["current_version"]), version_key(latest)
        result["status"] = "update_available" if latest_key > current_key else "up_to_date" if latest_key == current_key else "local_ahead"
    except (OSError, ValueError, KeyError, TypeError) as exc:
        result["error"] = str(exc)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--region", choices=SOURCES)
    parser.add_argument("--remember-region", action="store_true")
    parser.add_argument("--config", type=Path, default=default_config())
    parser.add_argument("--timeout", type=float, default=4)
    args = parser.parse_args(argv)
    if args.timeout <= 0 or args.timeout > 30:
        parser.error("--timeout must be greater than 0 and at most 30 seconds")
    if args.remember_region and not args.region:
        parser.error("--remember-region requires --region")
    region = args.region
    config_error = None
    try:
        if args.remember_region:
            args.config.parent.mkdir(parents=True, exist_ok=True)
            args.config.write_text(json.dumps({"region": region}) + "\n", encoding="utf-8")
        elif region is None and args.config.exists():
            region = json.loads(args.config.read_text(encoding="utf-8-sig")).get("region")
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        config_error = str(exc)
    result = check(region, args.timeout)
    if config_error:
        result["config_error"] = config_error
    print(json.dumps(result, ensure_ascii=True))
    return 0 if result["status"] in ("up_to_date", "update_available", "local_ahead") else 1


if __name__ == "__main__":
    sys.exit(main())
