# Project Accounts

This document tracks all accounts involved in the Voyage Voyage project.

## Google Accounts

### Development/Project Setup
- **Project Owner**: `raz@yosigal.com`
  - Google Cloud Project: `voyage-voyage-480501`
  - OAuth credentials created with this account
  - Used for gcloud CLI authentication

### Test User
- **Test User Email**: `raz@yosigal.com`
  - Used for OAuth flow testing
  - Has access to Google Photos albums for testing

## OAuth Configuration
- **Client ID**: Set via `GOOGLE_CLIENT_ID` environment variable (see `.env.example`)
- **Client Secret**: Set via `GOOGLE_CLIENT_SECRET` environment variable (see `.env.example`)
- **Redirect URI**: `http://localhost:8000/api/auth/google/callback` (configured in Google Cloud Console)
- **Project ID**: `voyage-voyage-480501`

## Notes
- OAuth consent screen should include `raz@yosigal.com` as a test user
- Google Photos Library API must be enabled for this project
- All development and testing uses `raz@yosigal.com` account

