# 🚀 Voyage Voyage — Implementation Plan (MVP)
**Version:** 1.0  
**Status:** Draft  
**Owners:** Tech Lead  
**Last Updated:** 2025-12-06

---

## Overview

This document outlines the step-by-step implementation plan for Voyage Voyage MVP, organized into 11 milestones. Each milestone builds on previous work and includes clear acceptance criteria.

**This plan is the blueprint/map** — it shows the big picture, dependencies, and how pieces fit together. It should have **low change frequency** — humans update it when strategy shifts.

**GitHub Issues are the work tickets** — each milestone should be broken down into concrete, bounded GitHub issues that agents actually work from.

**Key Principles:**
- This plan defines milestones and their relationships
- GitHub issues break down milestones into implementable tasks
- Agents work from GitHub issues (which reference this plan)
- Work on one milestone at a time
- Complete and test each milestone before moving to the next
- Update `docs/implementation-log.md` after each merged PR
- Keep PRs small and focused (100-300 lines of diff)

---

## Milestone 1: Repo + Skeleton

**Goal:** Set up the basic repository structure, development environment, and foundational code.

### Tasks

1. **Initialize repository structure**
   - Create `backend/` directory with FastAPI skeleton
   - Create `frontend/` directory (placeholder for future)
   - Set up `docs/` structure (already exists)
   - Create `ops/` directory for operational docs
   - Add `.gitignore` for Python, Node, and secrets

2. **Backend skeleton**
   - Initialize FastAPI app with basic structure
   - Set up project structure:
     - `backend/app/` (main application)
     - `backend/app/api/` (API routes)
     - `backend/app/core/` (config, security)
     - `backend/app/models/` (database models)
     - `backend/app/services/` (business logic)
   - Create `main.py` entry point
   - Add basic health check endpoint: `GET /api/health`

3. **Development environment**
   - Create `requirements.txt` with core dependencies:
     - `fastapi`
     - `uvicorn`
     - `sqlalchemy`
     - `alembic` (for migrations)
     - `pydantic`
     - `python-dotenv`
   - Create `docker-compose.yml` for local Postgres
   - Create `.env.example` with all required variables (from technical-spec.md)
   - Add `README.md` with setup instructions

4. **Database setup**
   - Initialize Alembic for migrations
   - Create initial migration structure
   - Set up database connection configuration

### Acceptance Criteria

- [ ] Repository has clear directory structure
- [ ] `GET /api/health` returns `{"status": "ok", "time": "..."}`
- [ ] Docker Compose starts Postgres locally
- [ ] `.env.example` includes all variables from technical-spec.md
- [ ] README explains how to run the backend locally
- [ ] Code follows PEP8 and has basic type hints

### Dependencies

- None (foundational milestone)

---

## Milestone 2: OAuth + Albums List

**Goal:** Implement Google OAuth authentication and list user's Google Photos albums.

### Tasks

1. **OAuth configuration**
   - Add Google OAuth client configuration
   - Implement `GET /api/auth/google/start` endpoint
   - Generate OAuth state token and store in session/cookie
   - Return redirect URL to Google

2. **OAuth callback**
   - Implement `GET /api/auth/google/callback` endpoint
   - Exchange authorization code for tokens
   - Store refresh token (encrypted) in database
   - Create or update user record
   - Generate session/JWT token for client
   - Return user info + token

3. **User authentication**
   - Implement `GET /api/auth/me` endpoint
   - Add authentication middleware/dependency
   - Validate tokens and extract user context

4. **Database models**
   - Create `users` table (id, google_user_id, email, created_at)
   - Create `oauth_credentials` table (user_id, provider, refresh_token, expires_at, scopes, updated_at)
   - Add Alembic migration

5. **Google Photos integration (read)**
   - Set up Google Photos API client
   - Implement token refresh logic
   - Implement `GET /api/albums` endpoint
   - Fetch albums from Google Photos API
   - Handle pagination with `nextPageToken`
   - Return album list with: id, title, mediaItemCount, productUrl

6. **Token encryption**
   - Implement AES-GCM encryption for refresh tokens
   - Store encryption key in environment variable
   - Never log tokens or PII

### Acceptance Criteria

- [ ] `GET /api/auth/google/start` returns `{"auth_url": "..."}`
- [ ] OAuth callback creates user and returns token
- [ ] `GET /api/auth/me` returns current user when authenticated
- [ ] `GET /api/auth/me` returns 401 when not authenticated
- [ ] `GET /api/albums` lists user's Google Photos albums
- [ ] Refresh tokens are encrypted at rest
- [ ] Manual test: complete OAuth flow and list albums via curl

### Dependencies

- Milestone 1 (repo + skeleton)

---

## Milestone 3: Album Clone

**Goal:** Implement basic album cloning without processing (Milestone 2 behavior from PRD).

### Tasks

1. **Database models**
   - Create `jobs` table (id, user_id, google_album_id, output_album_id, status, error_message, input_photo_count, output_photo_count, started_at, completed_at)
   - Create `photos` table (id, job_id, original_media_item_id, processed_media_item_id, is_duplicate, is_hero, is_album_cover, aesthetic_score, people_coverage_score, created_at)
   - Add Alembic migration

2. **Clone endpoint**
   - Implement `POST /api/albums/{albumId}/clone` endpoint
   - Validate album exists and user has access
   - Create job record with status `importing_album`
   - Fetch all media items from source album
   - Create new Google Photos album: `{originalTitle} – By Voyage Voyage`
   - Copy all media items (photos + videos) as-is to new album
   - Update job status to `completed`
   - Store output_album_id in job

3. **Job status endpoint**
   - Implement `GET /api/jobs/{jobId}` endpoint
   - Return job status, stage, progress
   - Validate job belongs to user

4. **Background processing (basic)**
   - Implement simple in-process worker for clone operation
   - Update job status at each stage
   - Handle errors gracefully

### Acceptance Criteria

- [ ] `POST /api/albums/{albumId}/clone` returns `{"job_id": "...", "status": "importing_album"}`
- [ ] Clone creates new album with correct name format
- [ ] All media items (photos + videos) are copied
- [ ] `GET /api/jobs/{jobId}` returns current job status
- [ ] Job status progresses: `importing_album` → `completed`
- [ ] Manual test: clone an album and verify output in Google Photos

### Dependencies

- Milestone 2 (OAuth + albums list)

---

## Milestone 4: Rating Flow

**Goal:** Allow users to rate completed albums.

### Tasks

1. **Database model**
   - Create `ratings` table (id, job_id, user_id, stars, comment, created_at)
   - Add Alembic migration

2. **Rating endpoints**
   - Implement `POST /api/albums/{jobId}/rating` endpoint
   - Validate stars (1-5), comment length (max 2000 chars)
   - Validate job exists and belongs to user
   - Store rating in database
   - Implement `GET /api/albums/{jobId}/rating` endpoint
   - Return existing rating or 404 if not found

3. **Validation**
   - Ensure job is completed before allowing rating
   - Prevent duplicate ratings (update existing if needed)

### Acceptance Criteria

- [ ] `POST /api/albums/{jobId}/rating` accepts stars (1-5) and optional comment
- [ ] Rating is stored and associated with job
- [ ] `GET /api/albums/{jobId}/rating` returns existing rating
- [ ] Returns 400 for invalid stars
- [ ] Returns 404 if job not found
- [ ] Manual test: create rating and retrieve it via curl

### Dependencies

- Milestone 3 (album clone)

---

## Milestone 5: Deduplication

**Goal:** Detect and remove near-duplicate photos from albums.

### Tasks

1. **Deduplication logic**
   - Implement image embedding extraction (using CLIP or similar)
   - Calculate similarity scores between images
   - Identify near-duplicates (threshold configurable)
   - Select best version (highest resolution or quality)
   - Mark duplicates in `photos` table (`is_duplicate = True`)

2. **Debug endpoint**
   - Implement `POST /api/debug/dedupe` endpoint
   - Accept list of media_item_ids
   - Return `keep` and `duplicates` arrays
   - Useful for testing and validation

3. **Integration with clone**
   - Add deduplication step to clone pipeline
   - Update job status to `deduping_photos`
   - Skip duplicate photos when creating output album
   - Update `output_photo_count` in job

4. **Quality checks**
   - Ensure no unique photos are removed
   - Log deduplication decisions
   - Fallback: if dedup fails, include all photos

### Acceptance Criteria

- [ ] Deduplication identifies near-duplicates correctly
- [ ] No unique photos are removed
- [ ] `POST /api/debug/dedupe` returns keep/duplicates arrays
- [ ] Clone pipeline includes deduplication step
- [ ] Job status includes `deduping_photos` stage
- [ ] Manual test: run dedupe on test set and verify results

### Dependencies

- Milestone 3 (album clone)
- External: Image embedding API or model

---

## Milestone 6: Enhance Single Photo

**Goal:** Implement enhancement pipeline for a single photo (debug endpoint).

### Tasks

1. **Enhancement service**
   - Integrate with external enhancement API (or local model)
   - Implement: super-resolution, sharpening, noise reduction
   - Download original from Google Photos
   - Process image
   - Upload enhanced version to Cloud Storage (temporary)
   - Return enhanced URL

2. **Debug endpoint**
   - Implement `POST /api/debug/enhance-single` endpoint
   - Accept `media_item_id`
   - Process single image
   - Return enhanced URL and metrics (processing_ms)

3. **Error handling**
   - Fallback to original if enhancement fails
   - Log errors without exposing secrets
   - Return meaningful error messages

4. **Cloud Storage setup**
   - Configure temporary bucket
   - Implement upload/download helpers
   - Set up cleanup policy (optional for MVP)

### Acceptance Criteria

- [ ] `POST /api/debug/enhance-single` processes a single image
- [ ] Enhanced image is uploaded to Cloud Storage
- [ ] Response includes enhanced URL and processing time
- [ ] Falls back to original on failure
- [ ] Manual test: enhance a test photo and verify quality improvement

### Dependencies

- Milestone 2 (OAuth - for accessing Google Photos)
- External: Enhancement API or model
- GCP: Cloud Storage bucket

---

## Milestone 7: Enhance Batch

**Goal:** Enhance all photos in an album batch.

### Tasks

1. **Batch enhancement**
   - Integrate enhancement into clone pipeline
   - Process photos in parallel (configurable concurrency)
   - Update job status: `enhancing_photos`
   - Track progress percentage
   - Store enhanced images in Cloud Storage

2. **Pipeline stages**
   - Add stages: `sharpening_images`, `correcting_tilts`, `cropping_images`
   - Implement tilt detection and correction
   - Implement smart cropping
   - Update job status for each stage

3. **Progress tracking**
   - Calculate and update `progress` field (0.0 to 1.0)
   - Update `output_photo_count` as photos are processed
   - Log progress at regular intervals

4. **Error handling**
   - Continue processing if individual photos fail
   - Use original image as fallback
   - Log failures but don't stop pipeline

### Acceptance Criteria

- [ ] Clone pipeline includes enhancement stages
- [ ] Photos are enhanced in parallel
- [ ] Job progress updates correctly (0.0 to 1.0)
- [ ] Tilt correction and cropping work correctly
- [ ] Failed enhancements fall back to original
- [ ] Manual test: enhance an album and verify all photos processed

### Dependencies

- Milestone 6 (enhance single)
- Milestone 5 (deduplication)

---

## Milestone 8: Hero Selection + Album Cover

**Goal:** Select best photos (hero images) and choose album cover.

### Tasks

1. **Aesthetic scoring**
   - Implement aesthetic quality scoring (using CLIP or API)
   - Calculate per-image scores
   - Store in `photos.aesthetic_score`

2. **Face detection**
   - Integrate face detection (using API or model)
   - Count unique identities per image
   - Store in `photos.people_coverage_score`
   - Cluster identities across images

3. **Hero selection**
   - Implement hero selection algorithm:
     - Rank by weighted sum: aesthetic_score + people_coverage_score + sharpness
     - Select top N% (configurable, e.g., 20%)
   - Mark selected photos: `photos.is_hero = True`
   - Update job status: `selecting_hero_images`

4. **Album cover selection**
   - Select from hero images only
   - Optimize for:
     1. Number of unique people (people_coverage_score)
     2. Aesthetic score
   - Mark cover: `photos.is_album_cover = True`
   - Update job status: `selecting_album_cover`
   - Attempt to set cover via Google Photos API (if supported)

5. **Integration**
   - Add hero/cover selection to pipeline after enhancement
   - Store scores in database

### Acceptance Criteria

- [ ] Hero images are selected based on quality metrics
- [ ] Album cover is selected from hero images
- [ ] Cover prioritizes people count, then aesthetic score
- [ ] Job status includes `selecting_hero_images` and `selecting_album_cover`
- [ ] Scores stored in database
- [ ] Manual test: verify hero selection and cover choice

### Dependencies

- Milestone 7 (enhance batch)
- External: Face detection API or model
- External: Aesthetic scoring API or model

---

## Milestone 9: Restyle Heroes

**Goal:** Apply artistic restyling to hero images.

### Tasks

1. **Restyle service**
   - Integrate with restyle API (or local model)
   - Support styles: `anime`, `ghibli`
   - Process hero images only
   - Store restyled versions in Cloud Storage

2. **Debug endpoint**
   - Implement `POST /api/debug/restyle-single` endpoint
   - Accept `media_item_id` and `style`
   - Return restyled URL and metrics

3. **Pipeline integration**
   - Add `restyling_hero_images` stage to pipeline
   - Process only photos where `is_hero = True`
   - Apply one style per photo (can be random or configurable)
   - Update job status and progress

4. **Output album**
   - Include both original enhanced and restyled versions in output
   - Or replace hero images with restyled versions (configurable)

### Acceptance Criteria

- [ ] `POST /api/debug/restyle-single` applies style to single image
- [ ] Restyling works for `anime` and `ghibli` styles
- [ ] Pipeline restyles all hero images
- [ ] Job status includes `restyling_hero_images` stage
- [ ] Restyled images included in output album
- [ ] Manual test: restyle hero images and verify output

### Dependencies

- Milestone 8 (hero selection)
- External: Restyle API or model

---

## Milestone 10: Full Pipeline

**Goal:** Integrate all stages into complete processing pipeline.

### Tasks

1. **Process endpoint**
   - Implement `POST /api/albums/{albumId}/process` endpoint
   - Trigger full enhancement pipeline (all stages)
   - Create job and start background processing

2. **Complete pipeline orchestration**
   - Execute all stages in order:
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
   - Update job status at each stage
   - Track progress throughout

3. **Upload to Google Photos**
   - Upload all processed images to output album
   - Maintain chronological order
   - Include videos (unchanged)
   - Map processed → original → new media item IDs
   - Update `output_album_id` in job

4. **Error handling**
   - Handle failures at any stage gracefully
   - Mark job as `failed` with error message
   - Preserve partial progress where safe
   - Never expose internal errors to API

5. **Performance optimization**
   - Parallelize where possible (enhancement, restyling)
   - Optimize for < 5 minutes per 100 photos
   - Add timing metrics

### Acceptance Criteria

- [ ] `POST /api/albums/{albumId}/process` triggers full pipeline
- [ ] All 11 stages execute in order
- [ ] Job status updates correctly at each stage
- [ ] Progress updates (0.0 to 1.0)
- [ ] Output album created with all processed images
- [ ] Videos included unchanged
- [ ] Chronological order preserved
- [ ] Pipeline completes in < 5 minutes for 100 photos
- [ ] Manual test: process full album end-to-end

### Dependencies

- Milestones 5-9 (all processing stages)

---

## Milestone 11: MVP Polish

**Goal:** Final polish, documentation, and production readiness.

### Tasks

1. **Documentation**
   - Ensure `docs/api.md` matches all implemented endpoints
   - Update `docs/technical-spec.md` with any deviations
   - Complete `docs/implementation-log.md` with all milestones
   - Add curl examples for all endpoints
   - Update README with deployment instructions

2. **Error handling polish**
   - Standardize error response format
   - Add consistent error codes
   - Ensure no secrets leak in errors
   - Add user-friendly error messages

3. **Logging**
   - Add structured logging throughout
   - Include job_id, user_id (hashed), stage in logs
   - Never log tokens or PII
   - Add timing metrics for each stage

4. **Testing**
   - Manual test all endpoints
   - Test error cases (404, 401, 500)
   - Test with real Google Photos albums
   - Verify quality: output never worse than input

5. **Code quality**
   - Run linters and fix issues
   - Ensure type hints throughout
   - Remove commented code
   - Add docstrings for key functions

6. **Configuration**
   - Centralize all configurable values
   - Document all environment variables
   - Add validation for required config

7. **Security review**
   - Verify tokens encrypted at rest
   - Ensure no secrets in code or logs
   - Review OAuth flow security
   - Check API authentication

### Acceptance Criteria

- [ ] All documentation is up to date
- [ ] All endpoints tested manually
- [ ] Error handling is consistent and secure
- [ ] Logging is structured and safe
- [ ] Code passes linters
- [ ] No secrets in codebase
- [ ] README explains deployment
- [ ] MVP ready for production deployment

### Dependencies

- Milestone 10 (full pipeline)

---

## GitHub Issues (Required for Implementation)

**This plan produces GitHub issues.** Each milestone should be broken down into 3-10 concrete GitHub issues that agents work from.

### Creating Issues from Milestones

For each milestone in this plan:

1. **Break down into issues:** Each major task or component becomes an issue
2. **Issue Title:** `M[X]: [Concrete Task]` (e.g., "M3: Implement POST /api/albums/{albumId}/clone endpoint")
3. **Issue Body Structure:**
   ```markdown
   ## Context
   Part of Milestone [X]: [Milestone Name]
   See `docs/implementation-plan.md` → Milestone [X] for full context.

   ## Task
   [Specific, bounded task from the milestone]

   ## Acceptance Criteria
   - [ ] [Specific, testable criteria]
   - [ ] [Another criteria]

   ## References
   - `docs/implementation-plan.md` → Milestone [X]
   - `docs/technical-spec.md` → [Relevant section]
   - `docs/api.md` → [Relevant endpoint]

   ## Dependencies
   - Depends on: #[previous-issue-number]
   ```

4. **Labels:** Add `milestone-[X]` and relevant labels (e.g., `backend`, `api`, `database`)
5. **Column:** Place in "Ready" when dependencies are met

### Breaking Down Large Milestones

If a milestone has many tasks, create multiple issues:
- One issue per major component (e.g., "M2: OAuth Start Endpoint", "M2: OAuth Callback", "M2: Albums List Endpoint")
- Each issue should be completable in 1-2 PRs (100-300 lines of diff)
- Issues should be independent enough to work on sequentially within the milestone

---

## Implementation Notes

### Order of Work

Work on milestones sequentially. Each issue should be:
1. **Read the GitHub issue** for the specific task
2. **Read referenced sections** in this plan and other docs
3. **Create a feature branch** (e.g., `feature/m3-clone-endpoint`)
4. **Implement** following the issue's acceptance criteria
5. **Test manually** using the acceptance criteria
6. **Document in PR description:**
   - Link to the GitHub issue (e.g., "Closes #12")
   - Reference the milestone from this plan
   - Include testing commands
7. **Reviewed by human**
8. **Merged to main**
9. **Issue closed**
10. **Logged in `docs/implementation-log.md`**

### Breaking Down Large Milestones

If a milestone is too large for one PR:
- Break into smaller PRs
- Each PR should be 100-300 lines of diff
- Complete one logical piece before moving to next
- Update documentation incrementally

### External Dependencies

Several milestones require external APIs or services:
- Enhancement API/model
- Face detection API/model
- Aesthetic scoring API/model
- Restyle API/model
- Google Photos API
- Cloud Storage

Plan integration early and have fallback options.

### Testing Strategy

For MVP:
- Manual testing is acceptable
- Include curl commands in PR descriptions
- Test with real Google Photos albums
- Verify quality improvements

### Performance Targets

- Full pipeline: < 5 minutes for 100 photos
- Deduplication: < 2 seconds for 100 photos
- Individual enhancements: < 5 seconds per photo
- Parallelize where possible

---

## Success Criteria

MVP is complete when:
- [ ] All 11 milestones implemented
- [ ] All endpoints from `api.md` working
- [ ] Full pipeline processes albums end-to-end
- [ ] Output quality meets "never worse than input" rule
- [ ] Documentation is complete and accurate
- [ ] Ready for production deployment

---

# ✨ End of Implementation Plan

This plan guides the step-by-step implementation of Voyage Voyage MVP. Update this document if milestones change or new requirements emerge.

