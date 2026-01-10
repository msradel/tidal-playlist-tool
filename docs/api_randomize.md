# POST /api/randomize

This document defines the **Smart Randomization** API endpoint for AudioArchitect Premium.

- This is a **backend API** used by the app UI.
- It accepts a neutral playlist JSON (see `docs/playlist_format.md`) and randomization options.
- It returns a new playlist JSON with tracks reordered by the Smart Randomization engine.[file:265]

---

## Endpoint

- **Method:** `POST`
- **Path:** `/api/randomize`
- **Auth:** (to be defined later; typically requires an authenticated Premium user)

---

## Request

### URL

```text
POST /api/randomize
Content-Type: application/json
