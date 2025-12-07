# 📡 Voyage Voyage — API Specification (MVP)
**Version:** 1.0  
**Status:** Draft (MVP)  
**Owners:** Tech Lead, Backend Lead **Last Updated:** 2025-12-06  

----

---
## 1. Overview

This document defines the **public REST API** for Voyage Voyage.

- Base URL (local dev): http://localhost:8000/api
- Auth: Bearer token (session/JWT) after Google login (exact auth wrapper can evolve)
- Format: JSON for requests and responses unless otherwise stated.

 All endpoints listed here **must** be kept in sync with the implementation.

----

## 2. Authentication & User Endpoints

### 2.1 GET /api/auth/google/start

Start Google OAuth flow. Returns a URL to redirect the user to.

**Request:**

- No body.
**Response 200:**
{
  "auth_url": "https://accounts.google.com/o/oauth2/v2/auth?..."
}

----

### 2.2 GET /api/auth/google/callback

Google OAuth redirect URI. Handles `code` from Google, exchanges for tokens, creates/updates user and session.

**Query parameters:**

- `code` (string, required)
- `state` (string, optional)

**Response 200**:
{
  "user": {
    "id": "uuid",
    "email": "user@example.com"
  },
  "token": "session-or-jwt-token"
}

----

### 2.3 GET /api/auth/me

Returns the current authenticated user.

**Auth:** `Authorization: Bearer <token>`

**Response 200**:
{
  "id": "uuid",
  "email": "user@example.com"
}

**Response 401**:
{
  "error": "unauthorized"
}

----

## 3. Photos Picker API

These endpoints allow users to select photos using Google Photos Picker API.

### 3.1 POST /api/photos/picker/session

Create a new Google Photos Picker session.

**Auth:** required

**Response 200**:
{
  "sessionId": "uuid",
  "pickerUri": "https://photospicker.googleapis.com/v1/..."
}

**Usage:** User should visit `pickerUri` in a browser to select photos.

----

### 3.2 GET /api/photos/picker/session/{sessionId}

Get the status of a Picker API session.

**Auth:** required

**Path params:**
- `sessionId` (string, required) – Picker session ID

**Response 200**:
{
  "sessionId": "uuid",
  "mediaItemsSet": true,
  "state": "COMPLETED"
}

**State values:** `PENDING`, `ACTIVE`, `COMPLETED`, `EXPIRED`

----

### 3.3 GET /api/photos/picker/session/{sessionId}/items

Get media items selected in a Picker API session.

**Auth:** required

**Path params:**
- `sessionId` (string, required) – Picker session ID

**Query params:**
- `page_token` (string, optional) – Token for pagination

**Response 200**:
{
  "mediaItems": [
    {
      "id": "google-photos-media-id",
      "filename": "IMG_1234.jpg",
      "mimeType": "image/jpeg",
      "mediaMetadata": {
        "width": "4000",
        "height": "3000"
      },
      "baseUrl": "https://lh3.googleusercontent.com/...=d",
      "type": "PHOTO",
      "createTime": "2025-12-07T10:30:00Z"
    }
  ],
  "nextPageToken": "token-for-next-page"
}

**Note:** `baseUrl` includes `=d` parameter for full resolution download. BaseUrl is valid for 60 minutes and requires Authorization header.

**Response 404:**
{
  "detail": "Media items not available yet. User must select photos in the picker first."
}

----

## 4. Albums (Future)

*Note: The `/api/albums` endpoint was deprecated in Milestone 2 due to Google Photos API changes. Users must use the Picker API (Section 3) to select photos.*

### 4.1 POST /api/albums/{albumId}/clone

### 4.1 POST /api/albums/{albumId}/clone

Clone an album **without processing** (Milestone 2 behavior).

- Creates a new Google Photos album with name: `{originalTitle} – By Voyage Voyage`
- Copies all items (photos + videos) as-is.
- Creates a `job` row to track the operation.

**Path params:**
- `albumId`(string, required) – Google Photos album ID

**Auth:** required

**Request body:**
{}

**Response 202**:
{
  "job_id": "uuid",
  "status": "importing_album"
}

**Errors:**
- `404` if album not found
- `401` if unauthorized with Google
- `500`  if Google API error

----

### 4.2 POST /api/albums/{albumId}/process

Trigger the **full enhancement pipeline** for the album.

Steps (conceptual):

1. Import album
2. Deduplicate
3. Enhance & sharpen
4. Tilt + crop
5. Hero selection
6. Album cover selection
7. Restyle hero images
8. Upload to new Google Photos album

**Path params:**
- `albumId`(string) – Google Photos album ID

**Auth:** required

**Request body (MVP):**
{}

**Response 202:**
{
  "job_id": "uuid",
  "status": "importing_album"
}

----

## 5. Jobs

### 5.1 GET /api/jobs/{jobId}

Fetch status of a processing job.
**Path params:**
- `jobId`(string, UUID)

**Auth:** required

**Response 200**:
{
  "job_id": "uuid",
  "status": "enhancing_photos",
  "stage": "enhancing_photos",
  "progress": 0.45,
  "input_photo_count": 120,
  "output_photo_count": 95,
  "google_album_id": "original-google-album-id",
  "output_album_id": "new-google-album-id-or-null-yet",
  "started_at": "2025-12-06T20:00:00Z",
  "completed_at": null,
  "error_message": null
}


**Possible `status` / `stage` values:**

- `importing_album`
- `deduping_photos`
- `enhancing_photos`
- `sharpening_images`
- `correcting_tilts`
- `cropping_images`
- `selecting_hero_images`
- `selecting_album_cover`
- `restyling_hero_images`
- `uploading_to_google_photos`
- `completed`
- `failed`

**Errors:**
- `404`  if job not found
- `403`   if job does not belong to user

----

## 6. Ratings

### 6.1 POST /api/albums/{jobId}/rating

Submit a rating for a finished (or at least completed-output) job/album.

**Path params:**
- `jobId` (UUID) – the processing job ID

**Auth:** required

**Request body:**
{
  "stars": 5,
  "comment": "Loved how it picked our best photos!"
}

Constraints:
- `stars`: integer 1-5
- `comment`: optional, max length ~2000 chars

**Response 201**:
{
  "job_id": "uuid",
  "stars": 5,
  "comment": "Loved how it picked our best photos!",
  "created_at": "2025-12-06T21:00:00Z"
}

**Errors:**

- `400`  if invalid rating (e.g., stars outside 1-5)
- `404`   if job not found
- `403`   if job does not belong to user

----

### 6.2 GET /api/albums/{jobId}/rating

Fetch an existing rating for a job, if it exists.

**Path params:**
- `jobId` (UUID)

**Auth:** required

**Response 200:**
{
  "job_id": "uuid",
  "stars": 4,
  "comment": "Great, but a few duplicates remained.",
  "created_at": "2025-12-06T21:03:11Z"
}

**Response 404:**
{
  "error": "rating_not_found"
}

----

## 7. Debug / Development Endpoints

These endpoints are meant for *internal testing and derisking*, not end users. They may be behind a feature flag or require a special internal API key in production.

### 7.1 POST /api/debug/enhance-single

Run the enhancement pipeline on a single test image.

**Auth:** required (plus internal key in prod)

**Request body options:**

Option A: Use an existing Google Photos media item ID

{
  "media_item_id": "google-photos-media-id"
}

**Option B:** (future) Uploaded image from client
For MVP we can start with Option A only.

**Response 200:**
{
  "original_media_item_id": "google-photos-media-id",
  "enhanced_url": "https://storage.googleapis.com/bucket/tmp-enhanced-123.jpg",
  "metrics": {
    "processing_ms": 842
  }
}

----

### 7.2 POST /api/debug/restyle-single

Apply a restyle to a single hero image.

**Request body:**
{
  "media_item_id": "google-photos-media-id",
  "style": "ghibli"
}

Allowed values for `style` in MVP:

- `anime`
- `ghibli`

**Response 200**:
{
  "media_item_id": "google-photos-media-id",
  "style": "ghibli",
  "restyled_url": "https://storage.googleapis.com/bucket/tmp-restyled-xyz.png",
  "metrics": {
    "processing_ms": 1450
  }
}

----

### 7.3 POST /api/debug/dedupe

Exercise deduplication logic on a small set of images.

**Request body:**
{
  "media_items": [
    { "media_item_id": "id-1" },
    { "media_item_id": "id-2" },
    { "media_item_id": "id-3" }
  ]
}

**Response 200**:
{
  "keep": [
    "id-1",
    "id-3"
  ],
  "duplicates": [
    {
      "kept": "id-1",
      "removed": ["id-2"]
    }
  ]
}

----

## 8. Health & Utility

### 8.1 GET /api/health

Simple health check.

**Response 200**:
{
  "status": "ok",
  "time": "2025-12-06T20:00:00Z"
}

----

## 9. Error Format (MVP)

To be simple, a basic error contract is sufficient:

```json
{
  "error": "short_machine_code",
  "message": "Human readable explanation"
}
```

Examples:

- {"error": "unauthorized", "message": "Missing or invalid token"}
- {"error": "album_not_found", "message": "Album does not exist or is not accessible"}
- {"error": "job_not_found", "message": "No job with that ID for this user" }

----

## 10. Versioning


For MVP:

- No URL-based versioning yet (`/api/v1`).  
- Breaking changes should be avoided.
- If a breaking change is needed, we will introduce `/api/v1` and keep `/api` as legacy or redirect.

----

## 11. Notes for Implementers

- Every endpoint must be documented here **before** or alongside implementation.
- Every PR that changes an endpoint must update this file.
- Curl examples should be added in comments or in a separate api-examples.md file if this grows too large.

