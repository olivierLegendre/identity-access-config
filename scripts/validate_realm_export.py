#!/usr/bin/env python3
"""Validate required clients and roles in a rendered Keycloak realm export."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_REALM_ROLES = {
    "viewer",
    "operator",
    "approver",
    "scenario_publisher",
    "site_admin",
    "org_admin",
}

REQUIRED_CLIENTS = {
    "operator-ui",
    "reference-api-service",
    "device-ingestion-service",
    "channel-policy-router",
    "automation-scenario-service",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--realm-export",
        default="keycloak/generated/realm-export.local.json",
        help="Path to rendered realm export",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = json.loads(Path(args.realm_export).read_text(encoding="utf-8"))

    roles = {
        role.get("name")
        for role in payload.get("roles", {}).get("realm", [])
        if isinstance(role, dict)
    }
    clients = {
        client.get("clientId")
        for client in payload.get("clients", [])
        if isinstance(client, dict)
    }

    missing_roles = sorted(REQUIRED_REALM_ROLES - roles)
    missing_clients = sorted(REQUIRED_CLIENTS - clients)

    if missing_roles or missing_clients:
        if missing_roles:
            print(f"missing realm roles: {', '.join(missing_roles)}")
        if missing_clients:
            print(f"missing clients: {', '.join(missing_clients)}")
        return 1

    print("realm export validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
