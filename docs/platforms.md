# Platform Support Matrix

AudioArchitect integrates with multiple streaming services. This document tracks API status, commercial-use rules, and how each platform fits into the overall product strategy.

> This file is the single source of truth for what is allowed where.  
> The Premium app may only use platforms that permit commercial, non‑streaming, metadata‑only applications.

---

## Legend

- **API Status**
  - Public: documented, self‑serve developer access.
  - Partner: requires separate business agreement.
  - Limited/Unknown: no clear public API for playlist management.

- **Commercial Use**
  - Yes: Terms explicitly allow monetizing non‑streaming apps that use metadata only.
  - No: Terms explicitly restrict use to non‑commercial applications.
  - Constrained: Possible, but only under narrow conditions or with additional agreements.

---

## Primary Monetized Platforms (Premium App)

These services can appear inside **AudioArchitect Premium** with full metadata‑only features (randomization, analytics, batch tools), subject to their terms.

| Service             | API Status  | Commercial Use           | Role in AudioArchitect               | Notes |
|---------------------|------------|--------------------------|--------------------------------------|-------|
| **Spotify**         | Public Web API[web:153] | **Yes** for non‑streaming apps (playlist manager example at $5/mo)[web:129][web:132] | Core platform for Premium app       | No playback in our app; metadata only. |
| **YouTube / YT Music** | Public API Services (YouTube Data API)[web:177][web:178] | **Yes**, selling an API client is allowed; content and ad restrictions apply[web:177] | Secondary platform for Premium (metadata only) | No download/stream; must respect YouTube content policies. |
| **SoundCloud**      | Public API[web:150] | **Constrained**, some commercial use allowed with restrictions[web:150] | Candidate for Premium integration   | Needs detailed ToS review before launch. |

---

## Non‑Commercial / Bridge Platforms

These services must **not** be monetized directly. They will be supported via separate, free, stand‑alone “Bridge” apps that only handle import/export using the neutral playlist format.

| Service        | API Status                | Commercial Use        | Role in AudioArchitect                 | Notes |
|----------------|---------------------------|-----------------------|----------------------------------------|-------|
| **TIDAL**      | Official Developer API[web:19][web:22] | **No** – “non‑commercial applications” only[web:10] | Stand‑alone free TIDAL Bridge app (import/export only) | May request Production Mode for higher quotas; still non‑commercial. |
| **Apple Music** | MusicKit / Apple Music API[web:146][web:189] | **Constrained** – subscriber‑only; commercial playlist tools unclear[web:139][web:148] | Stand‑alone free Apple Music Bridge app (import/export only) | Requires Apple Music subscription for end‑u
