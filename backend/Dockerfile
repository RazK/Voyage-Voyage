FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for PostgreSQL
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files and install package (this installs dependencies from pyproject.toml)
# Build context should be backend/ directory: docker build -t voyage-voyage:latest .
COPY pyproject.toml ./
COPY app/ ./app/

# Install the package and its dependencies from pyproject.toml
RUN pip install --no-cache-dir -e .

# Copy Alembic configuration files
COPY alembic.ini ./
COPY alembic/ ./alembic/

# Expose port
EXPOSE 8000

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

