# Contributing to AudioArchitect

Thank you for your interest in contributing! This document explains how to contribute to **AudioArchitect**, including:

- The monetized **Premium app** (metadata‑only playlist tools for commercial‑friendly platforms like Spotify).
- The free, stand‑alone **Bridge apps** (non‑commercial import/export tools for platforms like TIDAL and Apple Music).

Our goals are:

- A great experience for power users.
- Strict respect for each platform’s API terms.
- Clear separation between commercial and non‑commercial components.

---

## Code of Conduct

By participating in this project, you agree to:

- Be respectful and constructive in discussions.
- Focus on improving the project for all users.
- Accept maintainers’ decisions on scope and legal boundaries (API terms, commercial use, etc.).

If a separate `CODE_OF_CONDUCT.md` exists, that document also applies.

---

## Project Structure (High Level)

- **AudioArchitect Premium**
  - Monetized desktop/web app.
  - Works with platforms that allow commercial, metadata‑only apps (e.g., Spotify).
  - Provides advanced features: randomization, deduplication, analytics, batch tools.

- **Bridge Apps**
  - Free, stand‑alone tools (e.g., `tidal-bridge`, `apple-music-bridge`).
  - Non‑commercial, open source.
  - Only handle import/export between a single service and the **neutral playlist format** (JSON/CSV).
  - No randomization, analytics, or batch “magic” here.

For platform rules and allowed use cases, see `docs/platforms.md`.

---

## Reporting Bugs

Before opening a new issue:

- Check existing issues to avoid duplicates.
- Confirm you are on the latest `main` commit.
- If relevant, test with a clean environment (e.g., fresh virtualenv).

**Bug Report Template**

Include the following:

- **Describe the bug**  
  Clear description of what is going wrong.

- **To Reproduce**  
  1. Steps with commands or UI actions.  
  2. What you expected.  
  3. What actually happened.

- **Environment**  
  - OS: (e.g., Windows 11, macOS 15)  
  - Python/Node/Runtime version (if relevant)  
  - App variant: Premium / TIDAL Bridge / Apple Bridge, etc.  
  - App version or Git commit SHA

- **Logs / Error Messages**  
  Paste stack traces or logs in fenced code blocks (```).

---

## Suggesting Features

We welcome ideas that:

- Improve power‑user workflows.
- Add safe metadata‑only features.
- Respect platform API terms and the platform matrix in `docs/platforms.md`.

**Feature Request Template**

- **Problem**  
  What problem are you trying to solve?

- **Proposed solution**  
  What behavior or feature would you like to see?

- **Alternatives considered**  
  Other approaches you’ve thought about.

- **Additional context**  
  Screenshots, mockups, related tools or workflows.

---

## Development Setup

> These instructions may evolve per component (Premium vs. specific Bridge). Check the relevant `README.md` for details.

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/audioarchitect.git
cd audioarchitect
