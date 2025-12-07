# Voyage Voyage

Transform messy Google Photos trip albums into clean, cinematic, curated experiences.

## Overview

Voyage Voyage automatically:
- Deduplicates photos
- Enhances and sharpens images
- Corrects tilts and crops
- Selects hero images
- Restyles hero images (anime, Ghibli styles)
- Creates a polished output album in Google Photos

## Project Structure

```
.
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   └── services/
│   └── alembic/
├── frontend/         # Future UI (placeholder)
├── docs/            # Documentation
│   ├── prd.md                    # Product requirements
│   ├── technical-spec.md         # Technical architecture
│   ├── api.md                    # API specification
│   ├── implementation-plan.md    # Implementation milestones
│   └── agent-guidelines.md        # Rules for AI agents
└── ops/             # Operational docs and configs
```

## Documentation

- **Product Requirements**: `docs/prd.md`
- **Technical Specification**: `docs/technical-spec.md`
- **API Specification**: `docs/api.md`
- **Implementation Plan**: `docs/implementation-plan.md`
- **Agent Guidelines**: `docs/agent-guidelines.md`

## Development Status

**Current Status**: Milestone 1 (Repo + Skeleton) in progress

The FastAPI backend skeleton and local infrastructure scaffolding are now in place.

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL
- Docker and Docker Compose (for local development)

### Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in your values
3. (Recommended) Create a virtual environment: `python -m venv .venv`
4. Activate it and install dependencies: `pip install -r requirements.txt`
5. Start Postgres locally: `docker compose up db`
6. Run the backend API:
   ```bash
   uvicorn app.main:app --reload --app-dir backend
   ```
7. Verify the health endpoint:
   ```bash
   curl http://localhost:8000/api/health
   ```

## Implementation

Work is organized into 11 milestones. See `docs/implementation-plan.md` for details.

Agents should work from GitHub issues, which break down milestones into concrete tasks.

## License

[To be determined]

