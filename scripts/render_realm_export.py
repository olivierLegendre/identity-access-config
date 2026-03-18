#!/usr/bin/env python3
"""Render Keycloak realm export from the repository template and environment variables."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

TOKEN_RE = re.compile(r"\$\{([A-Z0-9_]+)\}")


def substitute(value: Any, env: dict[str, str], missing: set[str]) -> Any:
    if isinstance(value, dict):
        return {k: substitute(v, env, missing) for k, v in value.items()}
    if isinstance(value, list):
        return [substitute(v, env, missing) for v in value]
    if isinstance(value, str):
        def repl(match: re.Match[str]) -> str:
            key = match.group(1)
            if key not in env:
                missing.add(key)
                return match.group(0)
            return env[key]

        return TOKEN_RE.sub(repl, value)
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--template",
        default="keycloak/templates/realm-export.template.json",
        help="Path to realm export JSON template",
    )
    parser.add_argument(
        "--out",
        default="keycloak/generated/realm-export.local.json",
        help="Output path for rendered realm export",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    template_path = Path(args.template)
    out_path = Path(args.out)

    data = json.loads(template_path.read_text(encoding="utf-8"))
    env = dict(os.environ)
    missing: set[str] = set()
    rendered = substitute(data, env, missing)

    if missing:
        missing_csv = ", ".join(sorted(missing))
        raise SystemExit(f"missing required environment variable(s): {missing_csv}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(rendered, indent=2) + "\n", encoding="utf-8")
    print(f"rendered {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
