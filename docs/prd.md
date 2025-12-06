# 📘 Voyage Voyage — Product Requirements Document (PRD)
**Version:** 1.0  
**Status:** Approved for MVP  
**Owners:** Product Lead, Tech Lead  
**Last Updated:** 2025‑12‑06

---

# 1. Product Vision

Voyage Voyage transforms a messy, chaotic Google Photos trip album into a **clean, cinematic, cohesive story**.

It automatically deduplicates, enhances, sharpens, and restyles your best photos — turning an unstructured collection into an epic experience you’re proud to share.

**Value Proposition:**  
> “Clean up my messy album and transform it into a fluent, capturing, flowing Google Photos album that makes my trip look epic.”

Key qualities:
- **Creativity:** medium  
- **Quality:** high  
- **Speed:** medium (target < 5 minutes for 100 photos)

---

# 2. Target Audience

**Primary early users:** Tech‑savvy travelers who:
- Take many photos on group trips  
- Combine everything into one shared Google Photos album  
- Want a polished, cinematic summary without manual editing

They value:
- Automation  
- High-quality enhancements  
- A sense of epic storytelling

---

# 3. User Goals

Users want to:
1. Authenticate with Google  
2. Select a Google Photos album  
3. Have Voyage Voyage process it automatically  
4. Receive a duplicated, enhanced album  
5. Browse the output  
6. Rate the final album (1–5 stars + comments)

---

# 4. User Experience Flow (MVP)

1. **User logs in via Google** (other auth optional later)  
2. **User selects a Google Photos album**  
3. Voyage Voyage performs:
   - Album import  
   - Deduplication (near duplicates only)  
   - Resolution enhancement  
   - Sharpening  
   - Tilt correction  
   - Smart cropping  
   - Hero image selection  
   - Album cover selection (maximize people count → maximize quality)  
   - Restyling hero images (anime, Ghibli styles)
   - Recreating the album in Google Photos:
       - Same name + “– By Voyage Voyage”
       - Videos re-imported as-is
       - Original album remains untouched

4. **User navigates to the output album**  
5. **User rates the album** (1–5 stars + optional comment)

---

# 5. Key Features (MVP)

### 1. Google Photos Integration
- OAuth login  
- Read albums + media  
- Create output album  
- Upload enhanced media  
- Maintain chronological ordering  
- Support up to 100 photos  
- Videos: no processing; just reimport

### 2. Photo Deduplication
- Detect near-duplicates  
- Only remove duplicates  
- Never remove unique photos  
- Quality must not worsen

### 3. Photo Enhancement
- Resolution upscaling  
- Sharpening  
- Tilt correction  
- Smart cropping  
- 95% of users should feel the result is better than original

### 4. Hero Image Selection
- Use aesthetic quality + face detection  
- Cluster identities  
- Select representative hero subset

### 5. Album Cover Selection
- Select from hero images  
- Prioritize:
  1. Number of unique people visible  
  2. Aesthetic score  

### 6. Photo Restyling
- Restyle hero images  
- One style per photo  
- Supported: anime, Ghibli

### 7. Album Output
- Duplicate album → “{name} – By Voyage Voyage”  
- Includes:
  - Enhanced images  
  - Sharpened + corrected images  
  - Restyled hero images  
  - Videos (unchanged)  
- Chronological order preserved  
- Originals remain untouched

### 8. Rating Flow
- User sees album preview  
- Rates output: 1–5 stars  
- Can include optional comment  
- Ratings stored for improvement

---

# 6. Non‑Goals (MVP)
Not included in MVP:
- Interactive map  
- Route visualization  
- Location-based photo layers  
- Video montages  
- Multi-album workflows  
- Local on-device processing  
- Paid tier or monetization  

These may return later.

---

# 7. Functional Requirements

### Authentication
- Google OAuth 2.0  
- Store encrypted refresh tokens  
- Must support long-lived access

### Photo Pipeline
- Album import → transformation → output album  
- Persist job states  
- Logs for debugging  
- Graceful fallback (use original image if enhancement fails)  
- Total processing time < 5 minutes per 100 photos

### Pipeline Stages
1. Import album  
2. Deduplicate  
3. Enhance  
4. Sharpen  
5. Tilt correction  
6. Crop  
7. Hero selection  
8. Album cover selection  
9. Restyle heroes  
10. Upload output album

### Logging
- Stage-based progress  
- Error logs without private data  
- Timing metrics per step  

---

# 8. Performance Requirements
- Full pipeline for 100 images in < 5 minutes  
- Parallelize external API calls  
- Restyle only heroes to save time  
- External enhancement APIs allowed  

---

# 9. Quality Requirements
- Output album must **never** be worse than input  
- Dedup must not remove non-duplicates  
- Enhancement must succeed visually 95% of time  
- All processed images must upload; fallback = original  

---

# 10. User Story Summary

### Users want:
- Easy Google authentication  
- Automatic cleaning + enhancement  
- Best photos selected automatically  
- A beautiful new album generated  
- Ability to rate the results  

### Example User Stories:
1. *“As a user, I want duplicates removed so my album feels clean.”*  
2. *“As a user, I want sharper, clearer photos so the memories feel epic.”*  
3. *“As a user, I want the hero images to represent everyone on the trip.”*  
4. *“As a user, I want restyled images for social sharing.”*  
5. *“As a user, I want to rate the result so the system can improve.”*

---

# 11. Acceptance Criteria (MVP)
A feature is “done” when:
- It matches PRD  
- It matches the technical specification  
- It passes manual curl/UI tests  
- It doesn’t degrade album quality  
- It handles typical Google Photos trip albums reliably  

---

# 12. Open Questions (Future)
- User-controlled style selection  
- Ordering hero images  
- Return of video montage generation  
- Subscription-based monetization  

---

# ✨ End of PRD
This file defines product intent and MVP boundaries for Voyage Voyage.
