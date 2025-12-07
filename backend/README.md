# Voyage Voyage Backend

Backend service for transforming Google Photos trip albums into clean, cinematic, curated experiences.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Docker (optional, for containerized development)

### Setup

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   ```bash
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -e .
   ```
   
   Or if using pip directly:
   ```bash
   pip install fastapi uvicorn[standard]
   ```

4. **Configure environment variables:**
   ```bash
   # From the project root:
   cp .env.example .env
   ```
   
   Edit `.env` with your actual configuration values. **Never commit real secrets to git** - only `.env.example` should be in version control.

5. **Start the database (optional, for full stack):**
   ```bash
   docker compose up db
   ```

6. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

   The server will start on `http://localhost:8000`

## Healthcheck

Verify the application is running by checking the health endpoint:

```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "ok",
  "time": "2025-12-07T02:00:00Z"
}
```

## Development

The application uses FastAPI and can be run with uvicorn in development mode with auto-reload enabled using the `--reload` flag.

### Database Migrations

Alembic is configured for database migrations. To create a new migration:

```bash
alembic revision --autogenerate -m "description"
```

To apply migrations:

```bash
alembic upgrade head
```

## Docker

To build and run the application using Docker:

```bash
# From backend directory:
cd backend
docker build -t voyage-voyage:latest .
docker run -p 8000:8000 voyage-voyage:latest
```

**Note:** Build context should be the `backend/` directory where the Dockerfile is located.

