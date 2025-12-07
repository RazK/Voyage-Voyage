# Implementation Log

This document tracks meaningful changes to the Voyage Voyage project.

## 2025-12-07

### Milestone 1: Backend Skeleton Setup

**PR:** #7

**Summary:** Implemented foundational backend structure with FastAPI, database configuration, and development tooling.

**Changes:**
- Created FastAPI application with `/api/health` endpoint
- Set up project structure (app/, models/, services/, core/)
- Configured Alembic for database migrations
- Added Docker Compose for local PostgreSQL (port 5433)
- Created Dockerfile using `pip install -e .` from pyproject.toml
- Configured environment variables with `.env.example`
- Fixed database URL credentials to match docker-compose.yml (voyage:voyage)
- Set port to 5433 to avoid conflicts with existing PostgreSQL

**Impacted Areas:**
- Backend structure (`backend/app/`)
- Database configuration (`backend/app/core/`, `backend/alembic/`)
- Development environment (`backend/docker-compose.yml`, `backend/Dockerfile`)
- Documentation (`README.md`, `backend/README.md`)

**Testing:**
- Health endpoint: `curl http://localhost:8000/api/health`
- Database connection: `python3 backend/test_db_connection.py`
- All database operations verified (create, insert, query, drop)
- Docker build and container imports tested

**Status:** ✅ Complete - Merged

---

## 2025-12-07

### Milestone 2: OAuth + Google Photos Picker API

**PR:** TBD

**Summary:** Implemented Google OAuth 2.0 authentication with JWT tokens and Google Photos Picker API integration for user photo selection.

**Changes:**
- Implemented Google OAuth 2.0 flow (`/api/auth/google/start`, `/api/auth/google/callback`, `/api/auth/me`)
- Added JWT token generation and validation
- Implemented AES-GCM encryption for refresh token storage
- Created User and OAuthCredential database models
- Migrated database schema with Alembic
- Integrated Google Photos Picker API (`/api/photos/picker/session`, session status, items endpoints)
- Configured OAuth scopes for Picker API and app-created content access
- Removed deprecated `/api/albums` endpoint (replaced by Picker API)
- Added full-resolution photo download support (baseUrl with `=d` parameter)

**Impacted Areas:**
- Authentication (`backend/app/api/auth.py`, `backend/app/core/oauth.py`, `backend/app/core/jwt.py`)
- Database models (`backend/app/models/user.py`, `backend/app/models/oauth_credential.py`)
- Picker API service (`backend/app/services/picker_api.py`)
- API endpoints (`backend/app/api/picker.py`)
- Core utilities (`backend/app/core/encryption.py`, `backend/app/core/dependencies.py`)
- Database migrations (`backend/alembic/versions/`)
- Documentation (`docs/api.md`, `docs/PHOTOS_API_CHANGES.md`, `docs/KNOWN_ISSUES.md`)

**Key Decisions:**
- Pivoted from Google Photos Library API (deprecated for listing user albums) to Picker API
- OAuth scopes limited to: `photospicker.mediaitems.readonly`, `photoslibrary.appendonly`, `photoslibrary.readonly.appcreateddata`
- Refresh tokens encrypted at rest using AES-GCM
- JWT tokens for stateless session management

**Testing:**
- OAuth flow: `curl http://localhost:8000/api/auth/google/start`
- Authenticated endpoints: All require `Authorization: Bearer <token>` header
- Picker session creation: `POST /api/photos/picker/session`
- Photo retrieval: `GET /api/photos/picker/session/{id}/items`
- Full-resolution download verified

**Status:** ✅ Complete - Ready for PR


