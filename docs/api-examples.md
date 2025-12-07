# API Usage Examples

This document provides practical examples for using the Voyage Voyage API.

## Authentication Flow

### 1. Start OAuth Flow

```bash
curl http://localhost:8000/api/auth/google/start
```

**Response:**
```json
{
  "auth_url": "https://accounts.google.com/o/oauth2/v2/auth?...",
  "state": "random-state-token"
}
```

### 2. Visit Authorization URL

Open the `auth_url` in your browser to authenticate with Google.

### 3. OAuth Callback

After authentication, Google redirects to the callback URL. The backend returns:

```json
{
  "user": {
    "id": "8e993e9c-98a1-4b77-9da3-2e72e3e747d9",
    "email": "user@example.com"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Save the `token` for authenticated requests.**

### 4. Get Current User

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/auth/me
```

**Response:**
```json
{
  "id": "8e993e9c-98a1-4b77-9da3-2e72e3e747d9",
  "email": "user@example.com"
}
```

## Photos Picker API Flow

### 1. Create Picker Session

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/photos/picker/session
```

**Response:**
```json
{
  "sessionId": "4480bf2f-3e65-45e6-9023-1fff8991d47a",
  "pickerUri": "https://photospicker.googleapis.com/v1/..."
}
```

### 2. Open Picker URI

Open `pickerUri` in a browser. User selects photos in the Google Photos Picker interface.

### 3. Check Session Status

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/photos/picker/session/4480bf2f-3e65-45e6-9023-1fff8991d47a
```

**Response (pending):**
```json
{
  "sessionId": "4480bf2f-3e65-45e6-9023-1fff8991d47a",
  "mediaItemsSet": false,
  "state": "PENDING"
}
```

**Response (completed):**
```json
{
  "sessionId": "4480bf2f-3e65-45e6-9023-1fff8991d47a",
  "mediaItemsSet": true,
  "state": "COMPLETED"
}
```

### 4. Get Selected Photos

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/photos/picker/session/4480bf2f-3e65-45e6-9023-1fff8991d47a/items
```

**Response:**
```json
{
  "mediaItems": [
    {
      "id": "ATabc123...",
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
  "nextPageToken": null
}
```

### 5. Download Photo (Full Resolution)

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://lh3.googleusercontent.com/...=d" \
  -o photo.jpg
```

**Note:** The `baseUrl` already includes `=d` parameter for full resolution. Valid for 60 minutes.

## Complete Flow Example (Bash Script)

```bash
#!/bin/bash

API_URL="http://localhost:8000/api"
TOKEN=""

# 1. Start OAuth
echo "Starting OAuth flow..."
AUTH_RESPONSE=$(curl -s "$API_URL/auth/google/start")
AUTH_URL=$(echo $AUTH_RESPONSE | jq -r '.auth_url')

echo "Visit this URL to authenticate:"
echo "$AUTH_URL"
echo ""
echo "After authentication, paste the callback URL:"
read CALLBACK_URL

# Extract token from callback (manual step, or parse JSON response)
# For now, assume token is extracted manually
echo "Enter your JWT token:"
read TOKEN

# 2. Create picker session
echo "Creating picker session..."
SESSION_RESPONSE=$(curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  "$API_URL/photos/picker/session")
SESSION_ID=$(echo $SESSION_RESPONSE | jq -r '.sessionId')
PICKER_URI=$(echo $SESSION_RESPONSE | jq -r '.pickerUri')

echo "Open this URL to select photos:"
echo "$PICKER_URI"
echo ""
echo "Press Enter when you've selected photos..."
read

# 3. Check status
echo "Checking session status..."
curl -s -H "Authorization: Bearer $TOKEN" \
  "$API_URL/photos/picker/session/$SESSION_ID"

# 4. Get selected items
echo ""
echo "Fetching selected photos..."
curl -s -H "Authorization: Bearer $TOKEN" \
  "$API_URL/photos/picker/session/$SESSION_ID/items" | jq
```

## Error Handling

All endpoints return standard HTTP status codes:

- `200` - Success
- `400` - Bad Request (invalid parameters)
- `401` - Unauthorized (missing or invalid token)
- `404` - Not Found (session/item not found)
- `500` - Internal Server Error

Error responses follow this format:

```json
{
  "detail": "Human-readable error message"
}
```

Example:
```json
{
  "detail": "Failed to create picker session: OAuth credentials expired"
}
```

