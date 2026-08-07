# LMS SCIM Service

A mock LMS SCIM 2.0 service implemented with FastAPI. 
This service exposes a small SCIM-compatible API for LMS the following:
- users
- role resources
- training catalogs
- organizational scopes
- reporting access

## Features

- FastAPI application with automatic OpenAPI and Swagger UI
- SCIM endpoints for users, resource types, roles, and entitlements
- Bearer token authentication for all SCIM routes
- Pagination and filtering support on the Users endpoint

## Requirements

- Python 3.13+
- `fastapi`
- `uvicorn`
- `.env` file containing `SCIM_TOKEN`

## Run the application

From the project root, start the server with:

```bash
python -m uvicorn main:app --reload --port 8000
```

Once the server is running, you can access:

- Service root: http://localhost:8000/
- SCIM Users endpoint: http://localhost:8000/scim/v2/Users
- Swagger UI: http://localhost:8000/docs

## Authentication

The application loads the bearer token from `.env` using the `SCIM_TOKEN` environment variable.

All SCIM endpoints require a bearer token in the `Authorization` header.

Header example:

```text
Authorization: Bearer <your-scim-token>
```

For local testing, set the token value in `.env` as:

```text
SCIM_TOKEN=<your-scim-token>
```

To generate a token, use the following command:
```python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Using Swagger UI

1. Open http://localhost:8000/docs
2. Click the `Authorize` button in the top-right
3. Enter the token value
4. Click `Authorize`, then close the dialog
5. Explore the available SCIM endpoints directly from the docs

## Endpoints

- `GET /` - Health/status response
- `GET /scim/v2/Users` - List users
- `GET /scim/v2/Users/{user_id}` - Get a specific user
- `GET /scim/v2/ResourceTypes` - List SCIM resource types
- `GET /scim/v2/Roles` - List LMS roles
- `GET /scim/v2/TrainingCatalogs` - List training catalog entitlements
- `GET /scim/v2/OrganizationalScopes` - List organizational scope entitlements
- `GET /scim/v2/ReportingAccess` - List reporting access entitlements

## Local usage examples

List all users:

```bash
curl -H "Authorization: Bearer <SCIM_TOKEN>" http://localhost:8000/scim/v2/Users
```

Filter users by username:

```bash
curl -G -H "Authorization: Bearer <SCIM_TOKEN>" \
  --data-urlencode 'filter=userName eq "alice.adams@example.com"' \
  http://localhost:8000/scim/v2/Users
```

Get a specific user:

```bash
curl -H "Authorization: Bearer <SCIM_TOKEN>" http://localhost:8000/scim/v2/Users/1001
```

To stop the server, press `Ctrl+C` in the terminal.

## Usage with Okta

Okta cannot reach http://localhost:8000 on your workstation.

Expose it using Cloudflare Tunnel:
```base
cloudflared tunnel --url http://localhost:8000
```

This will return a URL that resembles:
```bash
https://random-name.trycloudflare.com
```

Your new SCIM base URL becomes:
```bash
https://random-name.trycloudflare.com/scim/v2
```

This gives Okta a publicly available endpoint while FastAPI runs locally.
