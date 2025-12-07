# Google Photos API Changes - 2025 Migration Guide

## What Changed

Google made significant changes to the Photos Library API in **March/April 2025**:

1. **Removed Scopes:**
   - `photoslibrary.readonly` - Can no longer list user's existing albums
   - `photoslibrary.sharing` - Removed
   - `photoslibrary` - Can no longer list user's existing albums

2. **New Limitations:**
   - Library API now **only works with content created by your app**
   - Cannot browse/read arbitrary user albums from their existing library
   - Cannot list all albums in user's Google Photos account

3. **New Approach Required:**
   - **Google Photos Picker API** - Users explicitly select photos/albums to share
   - Library API - For creating/editing albums that your app creates

## Solution: Use Picker API

### Architecture Change

**Old Approach (No Longer Works):**
1. User authenticates with OAuth
2. App lists all user's albums via Library API
3. User selects album to process

**New Approach (Required):**
1. User authenticates with OAuth
2. App creates a Picker session
3. User selects photos/albums via Google Photos Picker UI
4. App retrieves selected items via Picker API
5. App processes selected items
6. App can create curated album via Library API (using app-created scopes)

### Required Scopes

**For Picker API:**
- No additional OAuth scopes needed (uses existing OAuth)
- Picker API uses session-based authentication

**For Library API (creating curated albums):**
- `photoslibrary.appendonly` - Create albums and upload photos
- `photoslibrary.readonly.appcreateddata` - Read app-created albums (optional)
- `photoslibrary.edit.appcreateddata` - Edit app-created albums (optional)

### Implementation Steps

1. **Picker API Integration:**
   - `POST https://photospicker.googleapis.com/v1/sessions` - Create picker session
   - Get `pickerUri` from response
   - User visits `pickerUri` to select photos
   - Poll session status until `mediaItemsSet == true`
   - Retrieve selected items via `GET /v1/mediaItems`

2. **Library API (Output):**
   - Use `photoslibrary.appendonly` to create curated album
   - Upload processed photos to the new album
   - Only read/edit albums created by your app

## References

- [Google Photos Picker API](https://developers.google.com/photos/picker/guides/get-started-picker)
- [Photos Library API Updates](https://developers.google.com/photos/support/updates)
- [Authorization Scopes](https://developers.google.com/photos/library/legacy/guides/authorization)

## Migration Impact on Voyage Voyage

**Milestone 2 Changes Required:**
- Cannot list user's existing albums
- Must implement Picker API for photo selection
- UX changes: "Select photos" instead of "Select album from list"

**What Stays the Same:**
- OAuth authentication flow
- Token encryption and storage
- Core processing pipeline
- Album creation (via Library API with app-created scopes)

