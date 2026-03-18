# Keycloak Bootstrap Runbook (Wave 1)

This runbook defines the reproducible baseline for Wave 1 IAM setup.

## 1. Prepare environment

```bash
cd /home/olivier/work/iot_services/identity-access-config
cp .env.keycloak.example .env.keycloak
# edit .env.keycloak for your environment
set -a
source .env.keycloak
set +a
```

## 2. Render realm export

```bash
cd /home/olivier/work/iot_services/identity-access-config
./scripts/render_realm_export.py \
  --template keycloak/templates/realm-export.template.json \
  --out keycloak/generated/realm-export.local.json

./scripts/validate_realm_export.py \
  --realm-export keycloak/generated/realm-export.local.json
```

Expected result: `realm export validation: PASS`.

## 3. Start local Keycloak and import baseline

```bash
cd /home/olivier/work/iot_services/identity-access-config
set -a
source .env.keycloak
set +a

docker rm -f "${KEYCLOAK_CONTAINER}" >/dev/null 2>&1 || true

docker run -d \
  --name "${KEYCLOAK_CONTAINER}" \
  -p "${KEYCLOAK_HTTP_PORT}:8080" \
  -e KEYCLOAK_ADMIN="${KEYCLOAK_ADMIN}" \
  -e KEYCLOAK_ADMIN_PASSWORD="${KEYCLOAK_ADMIN_PASSWORD}" \
  -v "$PWD/keycloak/generated:/opt/keycloak/data/import" \
  quay.io/keycloak/keycloak:26.0.7 \
  start-dev --import-realm
```

After startup, sign in at `http://localhost:${KEYCLOAK_HTTP_PORT}` and verify realm `${KEYCLOAK_REALM}` exists.

## 4. Baseline controls covered

1. Required human realm roles exist: `viewer`, `operator`, `approver`, `scenario_publisher`, `site_admin`, `org_admin`.
2. Required clients exist:
- `operator-ui`
- `reference-api-service`
- `device-ingestion-service`
- `channel-policy-router`
- `automation-scenario-service`
3. Site and organization claims are mapped via default client scopes (`iot-site`, `iot-organization`).

## 5. Notes

1. Do not commit `.env.keycloak`.
2. Keep generated realm files under `keycloak/generated/` for local verification; promote immutable export artifacts only when intentionally versioning a baseline release.
3. Client secrets are generated/managed in Keycloak or vault-backed automation, not stored in this repo.
