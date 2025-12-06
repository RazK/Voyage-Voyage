# Agent Guidelines — Voyage Voyage

Version: 1.0
Status: Draft (MVP implementation)
Owners: Tech Lead

---

## 1. Purpose

This document defines **how AI coding agents must work** in the Voyage Voyage GitHub repository.

The goals:

- Ship a working MVP quickly.
- Keep the codebase **stable**, **readable**, and **easy-to-review**.
- Make it easy for humans to understand and intervene at any time.

If anything here conflicts with `prd.md` or `technical-spec.md`, those documents win. Ask a human to clarify by opening a GitHub issue comment.

---

## 2. Scope

These rules apply to:

- Any AI agent creating, editing, or deleting code or docs in the `voyage-voyage` repo.
- Any automation that opens PRs, commits, or comments on issues.

They do **not** apply to:

- Human-only experiments outside this repo.
- Local playground scripts not committed to source control.

---

## 3. How to Work on This Repo

### 3.1 High-Level Workflow

1. Pick a **single GitHub issue** from the "Ready" or "In Progress" column (work on issues sequentially within each milestone).

2. Read the issue description and all referenced documents:
   - The issue body
   - `docs/implementation-plan.md` (referenced milestone section)
   - `docs/technical-spec.md` (relevant sections)
   - `docs/api.md` (if implementing an endpoint)
   - `docs/prd.md` (for product context)

3. Create a **feature branch** off `main`.
   - Use a descriptive name:
     - `feature/<short-summary>`
     - `bugfix/<short-summary>`
     - `chore/<short-summary>`

4. Make **small, focused changes** that only address that issue.

5. Run the relevant **local tests / curl checks**.

6. Update documentation if needed.

7. Open a **Pull Request** with a clear description and checklist.

8. Wait for **human review**. Do not merge.


### 3.2 What You Must NOT Do

- Do **not** push directly to `main`.
- Do **not** modify multiple unrelated subsystems in one PR.
- Do **not** introduce new external dependencies without mentioning them in the PR description and relevant docs.
- Do **not** commit secrets or tokens.
- Do **not** refactor large sections of code unless the issue explicitly requests it.
- Do **not** work on issues from later milestones until earlier milestone issues are complete.

---

## 4. Repository Layout (MVP)

You should assume the repo looks roughly like this:

- `backend/` – FastAPI backend, main API, pipelines.
- `frontend/` – future UI (may be empty initially).
- `docs/` – product + tech docs (`prd.md`, `technical-spec.md`, `api.md`, `agent-guidelines.md`, etc.).
- `ops/` ― operational docs and configs (`accounts-and-keys.md`, deployment notes, etc.).
- `.github/` ― CI workflows (if present).
- `.env.example` ― env var template (no secrets).

If the layout differs slightly, follow existing patterns and ask via issue comment if needed.


---

## 5. Branching & Commits

Agents must work on *quality* feature branches and well-structured commits.

### 5.1 Branch Naming

Use descriptive branch names based on the issue:

- `feature/<short-summary>`
- `bugfix/<short-summary>`
- `chore/<short-summary>`

Examples:

- `feature/oauth-callback`
- `feature/clone-album-endpoint`
- `bugfix/job-status-update`
- `chore/add-pre-commit-config`


### 5.2 Commits

- Prefer *multiple small commits* over one giant commit.
- Commit messages should be imperative and descriptive:

  - → "add clone album endpoint"
  - → "fix job status enum"
  - → "misc changes"
  - → "WIP"

- Do **not** rewrite commit history unless requested.


---

## 6. Pull Requests

PRs are the place where humans view your code. You must make them as easy to review as possible.

### 6.1 PR Size

- Target: *100-300 lines of diff* per PR (excluding generated files).
- If a change grows larger, consider *splitting it* into smaller PRs.


### 6.2 Required PR Sections

Every PR description must include:

1. **Summary**
   - What you changed and why.

2. **Issue Link**

   - `Closes #<issue-number>` or `Related to #<issue-number>`
   - Reference the milestone from `docs/implementation-plan.md` (e.g., "Part of Milestone 1: Repo + Skeleton")

3. **Implementation Details**

   - Brief, bullet-point overview of key changes.
   - Mention any new dependencies.

4. **Testing**

   - List manual tests and exact commands (e.g., `curl`).
    - Examples:
      - `curl http://localhost:8000/api/health`
      - `curl http://localhost:8000/api/albums`

5. **Checklist**

   - `- [ ] Code compiles`
   - `- [ ] Manual tests added/runs documented`
   - `- [ ] No secrets added`
   - `- [ ] Docs updated (if needed)`


### 6.3 What Not to Include in a PR

- Large commented-out blocks of code.
- Unused helpers or utilities.
- Experimental scripts not referenced by any issue.


---

## 7. Coding Standards

If code doesn't match existing patterns in this repo, you should align to them instead of introducing new style.

### 7.1 Backend (Python / FastAPI)

- Follow PEP8 style where possible.
- Prefer **type hints** for function signatures and key data structures.
- Use pydantic models for request/response schemas.
- Keep functions short and focused.

Error handling:

- Never swallow exceptions silently.
- Log errors with context but **never log tokens, emails, or PII**.


### 7.2 Configuration

- All configurable values (timeouts, thresholds, limits) must be:

  - Centralized (e.g., `config.py` or settings module).
- Documented in code comments or `docs/`.


### 7.3 Logging

- Prefer structured logs (key-value style) where possible.
- Include:
  - `job_id`
  - `user_id` (if relevant, hashed or redacted when needed)
  - `stage` (pipeline stage)

- Do **not** log:

  - Access tokens
  - Refresh tokens
  - Raw image URLs from private albums


---

## 8. Tests & Manual Verification

### 8.1 Minimum Requirement

For MVP, **manual tests** are acceptable and expected.

For each PR:

- Add at least one **manual verification step**.
- Include exact commands in the PR description.

Examples:

- `docker compose up backend db`
- `curl http://localhost:8000/api/health`
- `curl -H "Authorization: Bearer <token>" http://localhost:8000/api/albums`


### 8.2 When Adding New Endpoints

- Add at least one example request/response to ``docs/api.md``.
- Ensure the endpoint returns:
  - Proper HTTP status codes (20x, 44x, 55x).
- A consistent error shape when failing.


---

## 9. Working with Docs

### 9.1 Documents You Must Respect

- `docs/prd.md` ― product requirements.
- `docs/technical-spec.md` — technical architecture.
- `docs/api.md` — endpoint definitions.
- `docs/implementation-plan.md` — blueprint/map showing milestones and dependencies.

If your change **contradicts** these, do **not** proceed without:

- Documenting the conflict in your PR description, or
- Asking a human to clarify via GitHub discussion/comment.

### 9.2 Updating Docs

Any time you:

- Add or change an endpoint — update ``docs/api.md``.
- Change system behavior ― consider updating ``docs/technical-spec.md``.
- Add a new milestone or adjust sequence — update `docs/implementation-plan.md`.

Docs should never drift far from reality.


---

## 10. Handling Secrets & Credentials

### 10.1 Absolute Rules

- **Never** commit:
  - API keys
  - OAuth client secrets
  - Refresh tokens
  - Real `.env` files

- Only commit:
  - `.env.example` with placeholders.
  - Documentation about *where* secrets live and *how* to configure them.


### 10.2 Using `ops/accounts-and-keys.md`

This file may list:

- Account names
- Key locations
- GCP project IDs
- Service names

It must **not** contain:

- Actual secret values
- Private keys

When in doubt, leave a `TODO` comment and let a human fill in values.


---

## 11. Issue Selection & Scope

### 11.1 Picking Work

- Only work on issues in:
  - `Ready` column
  - `In Progress` column (if assigned to you or explicitly available)

- Work on issues sequentially within each milestone (don't skip ahead to later milestones).

- Do **not**:

  - Create new issues without a human's request.
  - Change labels or priorities.
  - Work on issues from later milestones until earlier milestone issues are complete.


### 11.2 Staying Inside Scope

For each issue:

- Stick to the issue description and acceptance criteria.
- Read all referenced documents (plan, tech spec, API docs) for context.
- If you discover related bugs or refactors:
  - Mention them in the PR description.
  - Optionally add a comment in the issue.
  - Do **not** fix everything in one PR unless it is clearly safe and small.
  - Consider if the fix belongs in the current issue or should be a separate issue.


---

## 12. Implementation Log

`docs/implementation-log.md` is a running log of meaningful changes.

For each merged PR, add an entry like:

- Date
- PR number and title
- Short summary
- Impacted areas
- How to test (short)

Example:

- `2025-12-07 – #12 add /api/albums – backend, Google Photos integration – curl /api/albums`

Agents should update this file as part of their PRs.


---

## 13. Error Handling & Resilience

When adding or modifying pipeline steps:

- Update job status fields consistently.
- On failure:
  - Mark the job as `failed` (or similar agreed status).
  - Preserve partial progress where safe.
  - Avoid infinite retry loops.
- Provide actionable error messages for humans in logs.

API responses:

- Should not leak internal error traces.
- Should include a stable `error.code` and human-readable `error.message`.


---

## 14. Quality & "Never Worse Than Input" Rule

For any change that touches:

- Image enhancement
- Deduplication
- Restyling
- Hero selection
- Album cover selection

You must preserve the core rule:

 > The output album must **never be worse** than the input album.


If there is any doubt:

- Add conservative checks.
- Fallback to original images where needed.
- Log the reason for skipping enhancement or dedupe.


---

## 15. Communication Style

In PR descriptions and issue comments:

- Be concise and factual.
- Avoid speculation; state what the code does now.
- Use bullet points for clarity.
- Link to docs where relevant.

Example good PR description:

- Summary: add "/api/albums" endpoint to list Google Photos albums.
- Implementation:
  - Adds `GET /api/albums` endpoint.
  - Integrates with Google Photos `albums.list`.
  - Handles pagination with `nextPageToken`.
- Testing:
  - `curl -H "Authorization: Bearer <token>" http://localhost:8000/api/albums`
- Checklist:
  - [X] Code compiles
  - [X] Manual tests added/runs documented
  - [X] No secrets added
  - [X] Docs updated (if needed)

---
