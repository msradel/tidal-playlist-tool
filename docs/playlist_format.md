# Neutral Playlist Format

AudioArchitect uses a **service‑agnostic playlist format** so that:

- Each Bridge app (TIDAL Bridge, Apple Music Bridge, etc.) can import/export playlists without depending on other services.
- AudioArchitect Premium can read, process (randomize, clean up), and write playlists in a consistent way, regardless of origin.

This document defines the JSON and CSV formats. TXT is intentionally **not** a primary interchange format, to avoid ambiguity; see the note at the end.

---

## JSON Format (Preferred)

JSON is the primary interchange format. All new work should target JSON first.

### Top‑level structure

```json
{
  "schema_version": "1.0",
  "exported_at": "2026-01-09T19:00:00Z",
  "source_service": "tidal",
  "source_playlist_id": "uuid-or-id",
  "title": "My Playlist",
  "description": "Optional description",
  "owner": "username-or-id",
  "tracks": [ /* array of track objects */ ]
}
