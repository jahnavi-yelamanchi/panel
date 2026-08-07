# Panel

Visual search and recommendations for licensed comics and manga.

This repository starts with the rights-aware ingestion foundation. No comic media
is accepted without a partner manifest that defines how and where it may be used.

## Workspace

- `apps/api`: FastAPI catalog and ingestion service
- `infra`: Terraform for AWS and EKS
- `data`: DVC registry metadata and dataset policies

## Local setup

```sh
uv sync --all-groups
uv run uvicorn panel_api.main:app --app-dir apps/api --reload
```

Copy `.env.example` to `.env` before starting services that use external
infrastructure.

