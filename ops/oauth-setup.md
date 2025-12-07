# Google OAuth Setup (5 minutes)

## Quick Steps

1. **Go to**: https://console.cloud.google.com/

2. **Create/Select Project**: Click project dropdown → "New Project" → Name: "Voyage Voyage" → Create

3. **Enable API**: 
   - APIs & Services → Library
   - Search "Google Photos Library API" → Enable

4. **Create OAuth Credentials**:
   - APIs & Services → Credentials → "Create Credentials" → "OAuth client ID"
   - Application type: "Web application"
   - Name: "Voyage Voyage Local"
   - **Authorized redirect URIs**: `http://localhost:8000/api/auth/google/callback`
   - Create

5. **Copy Credentials**:
   - Copy "Client ID" → Paste in `.env` as `GOOGLE_CLIENT_ID=`
   - Copy "Client secret" → Paste in `.env` as `GOOGLE_CLIENT_SECRET=`

6. **Save .env** and you're done!

## Testing

After setup:
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

Then test: `curl http://localhost:8000/api/auth/google/start`

