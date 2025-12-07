# Known Issues & Limitations

## Google Photos Library API Scope Changes (2025)

**Status:** Architecture Change Required  
**Date:** 2025-12-07  
**Milestone:** M2 (OAuth + Albums List)

### Issue
`GET /api/albums` returns 403 "Request had insufficient authentication scopes" even though:
- OAuth flow works correctly
- Tokens contain all required scopes (`photoslibrary`, `readonly`, `appendonly`)
- Photos Library API is enabled in Google Cloud Console
- OAuth consent screen is properly configured

### Root Cause
**Google changed the Photos API in March 2025.** The scopes we're using (`photoslibrary`, `photoslibrary.readonly`) were **removed** for listing user albums. The Library API now **only works with content created by your app**, not for browsing arbitrary user albums.

**Key Changes:**
- `photoslibrary.readonly` scope removed for listing existing albums
- `photoslibrary` scope removed for listing existing albums  
- Library API now only supports:
  - `photoslibrary.appendonly` - Create/upload new content
  - `photoslibrary.readonly.appcreateddata` - Read only app-created albums
  - `photoslibrary.edit.appcreateddata` - Edit only app-created albums

**New Requirement:** To access user's existing photos, must use **Google Photos Picker API** where users explicitly select which photos to share.

### Technical Details
- Token verification confirms all scopes are present
- API returns 403 despite correct scopes
- This indicates Google's backend is blocking unverified apps from accessing Photos API

### Resolution
Submit the application for Google OAuth verification:
1. **Privacy Policy** - Publicly accessible URL required
2. **Terms of Service** - Recommended
3. **App Homepage** - Public URL
4. **Branding Information** - App name, logo
5. **Scope Justification** - Detailed explanation of why `photoslibrary` scope is needed
6. **Test Account/Instructions** - May be requested for complex apps

### Timeline
- Verification typically takes **several days to weeks**
- Simple apps with complete documentation may be faster
- Complex apps requiring security review may take longer

### Workaround
Continue development using mock data/simulated API responses while waiting for verification.

### References
- [Google OAuth Verification](https://support.google.com/googleapi/answer/7454865)
- Gemini consultation confirmed verification is required for Photos Library API
- Project ID: `voyage-voyage-480501`
- OAuth Consent Screen: Testing mode, test user: `raz@yosigal.com`

