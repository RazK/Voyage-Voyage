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
│   ├── app/         # Application code
│   ├── tests/       # Test suite
│   ├── Dockerfile   # Container configuration
│   └── pyproject.toml  # Python dependencies
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

**Current Status**: Milestone 1 - Backend Skeleton Complete

The backend skeleton is set up with FastAPI. See `backend/README.md` for backend-specific setup instructions.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Docker (optional, for containerized development)

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -e .
   ```

4. **Configure environment variables:**
   ```bash
   # From the project root:
   cp .env.example .env
   ```
   
   Edit `.env` with your actual configuration values. **Important:** Never commit real secrets to git. Only `.env.example` should be in version control - real secrets go only in `.env` or cloud configuration.

5. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```
   
   The server will start on `http://localhost:8000`

5. **Start the database (optional, for full stack):**
   ```bash
   cd backend
   docker compose up db
   ```

### Healthcheck

Verify the application is running by checking the health endpoint:

```bash
curl http://localhost:8000/api/health
```

Or open in your browser: `http://localhost:8000/api/health`

Expected response:
```json
{
  "status": "ok",
  "time": "2025-12-07T02:00:00Z"
}
```

## Implementation

Work is organized into 11 milestones. See `docs/implementation-plan.md` for details.

Agents should work from GitHub issues, which break down milestones into concrete tasks.

## License

[To be determined]

