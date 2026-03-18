# identity-access-config

Keycloak IAM configuration baseline for Wave 1 (Foundation And Security Baseline).

## Scope

This repository defines:
1. realm/client/role baseline for the IoT platform;
2. tenant-claim mapping scopes (`organization`, `site`);
3. reproducible render and validation scripts for realm export artifacts.

## Repository layout

- `keycloak/templates/realm-export.template.json`: canonical realm template with env placeholders.
- `scripts/render_realm_export.py`: renders a local realm export from template + environment variables.
- `scripts/validate_realm_export.py`: validates required roles and clients in rendered export.
- `docs/runbooks/keycloak-bootstrap.md`: bootstrap and import runbook.
- `.env.keycloak.example`: non-secret input example for rendering and local bootstrap commands.

## Quick start

```bash
cd /home/olivier/work/iot_services/identity-access-config
cp .env.keycloak.example .env.keycloak
set -a
source .env.keycloak
set +a

./scripts/render_realm_export.py \
  --template keycloak/templates/realm-export.template.json \
  --out keycloak/generated/realm-export.local.json

./scripts/validate_realm_export.py \
  --realm-export keycloak/generated/realm-export.local.json
```

For local Keycloak import flow, follow:
- `docs/runbooks/keycloak-bootstrap.md`
