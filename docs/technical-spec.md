# 🛠️ Voyage Voyage — Technical Specification (MVP)
**Version:** 1.0  
**Status:** Approved  
**Owners:** Tech Lead, Product Lead  
**Last Updated:** 2025‑12‑06

---

# 1. Overview

Voyage Voyage automatically transforms a messy Google Photos album into a clean, cinematic, curated experience.

This document defines the **technical architecture**, **APIs**, **pipelines**, **data model**, **infrastructure**, and **development requirements** needed to implement the MVP.

This spec is the *engineering source of truth* and complements:
- `prd.md` (product intent)
- `api.md` (endpoint contract)
- `agent-guidelines.md` (rules for AI agents)

---

# 2. Architecture Summary

## 2.1 High-Level Diagram

[Frontend SPA] <----> [Backend API (FastAPI)] <----> [Postgres DB]

----> [Google Photos API]

---> [Enhancement APIs]


## 2.2 Technologies

- **Backend:** Python (FastAPI)
- **Infrastructure:** GCP (Cloud Run, Cloud SQL, Cloud Storage)
- **Database:** PostgreSQL
- **Auth:** Google OAuth 2.0
- **Pipelines:** Python workers (initially in-process), expandable to Cloud Run Jobs
- **Enhancement/Restyle:** External APIs + optional local models

---

# 3. Environment Setup

## 3.1 Environments
- **Local**
- **Dev** (Cloud Run)
- **Prod** (Cloud Run)

## 3.2 Cloud Resources
Environment-specific resources:
- Cloud SQL (PostgreSQL)
- Cloud Storage temporary bucket
- Cloud Run backend deployments
- OAuth credentials
- Domain & SSL (future)

## 3.3 `.env.example`

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback

DATABASE_URL=postgresql://user:pass@localhost:5432/voyage

JWT_SECRET=
TOKEN_ENCRYPTION_KEY=

ENHANCEMENT_API_KEY=
RESTYLE_API_KEY=

TEMP_BUCKET_NAME=voyage-temp-dev
GCP_PROJECT_ID=


---

# 4. Core System Components

## 4.1 Backend API (FastAPI)
Responsibilities:
- Expose REST endpoints
- Manage OAuth integration
- Start album-processing jobs
- Produce job status updates
- Provide rating API
- Surface errors & logs

## 4.2 Processing Pipeline
A multi-step job system executed by Python workers.

Pipeline steps:

1. `importing_album`
2. `deduping_photos`
3. `enhancing_photos`
4. `sharpening_images`
5. `correcting_tilts`
6. `cropping_images`
7. `selecting_hero_images`
8. `selecting_album_cover`
9. `restyling_hero_images`
10. `uploading_to_google_photos`
11. `completed`

Each stage:
- Updates job status
- Stores progress percentage
- Logs actions
- Must be able to run independently for debugging

## 4.3 Temporary Storage
During processing:
- Original files temporarily downloaded from Google Photos
- Intermediate enhanced/restyled versions stored in Cloud Storage
- Items deleted after upload unless debugging is enabled

---

# 5. Google Photos Integration

## 5.1 OAuth
Scopes required:
- `https://www.googleapis.com/auth/photoslibrary.readonly`
- `https://www.googleapis.com/auth/photoslibrary.appendonly`
- `offline` (to get refresh token)

Refresh tokens:
- Stored encrypted using AES-GCM
- Never logged
- Automatically refreshed server-side

## 5.2 Reading Data
- Fetch album metadata
- Fetch media items (photos + videos)
- For MVP: videos are passed through unchanged

## 5.3 Creating Output Album
Output album:
- Same name + ` – By Voyage Voyage`
- Chronological order preserved
- Fallback to original image if enhancement fails

## 5.4 Uploading Media
- Enhanced or restyled media uploaded via Google Photos upload token flow
- Retries on failure
- Maps processed → original → new media item IDs in DB

---

# 6. Image Processing Pipeline

(External APIs allowed)

## 6.1 Deduplication
- Identify near-duplicates using embedding similarity
- Keep highest-resolution or highest-quality version
- Never remove distinct photos

## 6.2 Enhancement
Transforms:
- Super-resolution
- Sharpening
- Noise reduction
- Color correction
- Detail improvement

Fallback:
- If enhancement fails → original is used

## 6.3 Tilt & Crop
Automatic correction:
- Detect horizon angle
- Straighten up to ±15 degrees
- Crop minimally to preserve composition

## 6.4 Hero Selection
Data computed per image:
- Aesthetic score (using CLIP or an API)
- Face detection → number of unique identities
- Sharpness metric
- Exposure/contrast quality

Hero image selection:
- Rank by weighted sum
- Choose top N% (configurable)

## 6.5 Album Cover Selection
Optimize:
1. **People coverage score** (more unique faces = better)
2. **Aesthetic score**
3. Sharpness

Assign:
- Flag `is_album_cover = True`
- If Google Photos supports setting cover → attempt API call
- Otherwise mark in UI

## 6.6 Restyling
- Applied only to hero images
- Styles supported:
  - Anime
  - Ghibli
- One style per photo
- Store both original & restyled versions

---

# 7. Database Schema

## 7.1 `users`

id: UUID PK
google_user_id: text
email: text
created_at: timestamptz


## 7.2 `oauth_credentials`

user_id: UUID FK
provider: text (“google”)
refresh_token: text (encrypted)
expires_at: timestamptz
scopes: text[]
updated_at: timestamptz


## 7.3 `jobs`

id: UUID PK
user_id: UUID FK
google_album_id: text
output_album_id: text
status: text
error_message: text
input_photo_count: int
output_photo_count: int
started_at: timestamptz
completed_at: timestamptz


## 7.4 `photos`

id: UUID PK
job_id: UUID FK
original_media_item_id: text
processed_media_item_id: text
is_duplicate: bool
is_hero: bool
is_album_cover: bool
aesthetic_score: float
people_coverage_score: float
created_at: timestamptz


## 7.5 `ratings`

id: UUID PK
job_id: UUID FK
user_id: UUID FK
stars: int
comment: text
created_at: timestamptz


---

# 8. Backend API (Full contract defined in api.md)

Endpoints include:

- `/auth/google/start`
- `/auth/google/callback`
- `/auth/me`
- `/albums`
- `/albums/{albumId}/clone`
- `/albums/{albumId}/process`
- `/jobs/{jobId}`
- `/albums/{jobId}/rating`
- Debug endpoints:
  - `/debug/enhance-single`
  - `/debug/restyle-single`
  - `/debug/dedupe`

---

# 9. DevOps & Deployment

## 9.1 CI Pipeline
Triggered on PR:
- Install dependencies
- Build backend container
- Run basic lint & import checks
- Validate migrations compile

## 9.2 Deploy to Dev
Triggered on merge to main:
- Build image
- Deploy to Cloud Run (dev)
- Run migrations

## 9.3 Deploy to Prod
Triggered manually or by tag:
- Build image
- Deploy to Cloud Run (prod)
- Run migrations

## 9.4 Logs
- Print structured logs to stdout
- Cloud Logging captures all backend logs

---

# 10. Performance Requirements

- 100 images processed in **< 5 minutes**
- Parallel execution of enhancement + restyles
- Dedup runs in < 2 seconds for 100 photos
- No more than 5 retries per upload

---

# 11. Error Handling

- Each pipeline stage reports errors in `jobs.error_message`
- Errors never expose secrets
- Failures fallback gracefully to original images
- API returns:
  - `4xx` for user errors
  - `5xx` for processing failures

---

# 12. Security Requirements

- All tokens encrypted at rest
- HTTPS enforced
- No logging PII or tokens
- CSRF not required for API-only backend
- OAuth secrets stored in Secret Manager or environment variables

---

# 13. Milestones (Same as implementation plan)

1. Repo + skeleton  
2. OAuth + albums list  
3. Album clone  
4. Rating flow  
5. Dedup  
6. Enhance single  
7. Enhance batch  
8. Hero selection + album cover  
9. Restyle heroes  
10. Full pipeline  
11. MVP polish  

---

# 14. Non-Goals (MVP)

- Video montage generation  
- Interactive map  
- Multi-album workflows  
- On-device processing  
- Complex admin dashboards  

---

# 15. Glossary

**Hero images:** Best-quality images representing the trip  
**People coverage score:** Number of unique faces detected  
**Restyle:** Artistic transformation of hero images  
**Pipeline:** Ordered background processing stages  

---

# ✨ End of Technical Specification
This document defines how Voyage Voyage MVP will be built and run.
