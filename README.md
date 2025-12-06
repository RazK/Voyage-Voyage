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
├── backend/          # FastAPI backend (to be implemented)
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

**Current Status**: Pre-Milestone 1

The project is in the planning phase. Implementation will follow the milestones defined in `docs/implementation-plan.md`.

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL
- Docker and Docker Compose (for local development)

### Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in your values
3. Install dependencies: `pip install -r requirements.txt` (to be created)
4. Run database: `docker compose up db` (to be created)
5. Start backend: `uvicorn app.main:app --reload` (to be implemented)

## Implementation

Work is organized into 11 milestones. See `docs/implementation-plan.md` for details.

Agents should work from GitHub issues, which break down milestones into concrete tasks.

## License

[To be determined]

