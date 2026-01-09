# 🎵 TIDAL Playlist Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![TIDAL API](https://img.shields.io/badge/TIDAL-API-00FFFF.svg)](https://listen.tidal.com/)

> **Free, open-source TIDAL playlist management tool for Windows**
> 
> Manage, organize, randomize, and export your TIDAL playlists with a professional command-line interface.

---

## ✨ Features

### 📋 Playlist Management
- **View All Playlists** - Paginated table view with 20 playlists per page
- **Smart Categorization** - Automatically identifies Owned, Favorite, and Editorial playlists
- **Multi-Sort Options** - Sort by name, track count, duration, created date, updated date, or type
- **Playlist Details** - View comprehensive metadata with word-wrapped descriptions

### 🎲 Playlist Randomization
- **Shuffle Tracks** - Create new randomized playlists with one click
- **Preserves Originals** - Never modifies your original playlists
- **Batch Processing** - Handles large playlists (1000+ tracks) efficiently

### 💾 Export Capabilities
- **JSON Export** - Full metadata including track IDs, ISRC codes, timestamps
- **CSV Export** - Spreadsheet-compatible format for analysis
- **TXT Export** - Human-readable text format
- **Track-Level Data** - Artist, album, duration, track numbers

### 🎯 Track Browser (Level 3)
- **Pagination** - 20 tracks per page with next/previous navigation
- **Search** - Filter by artist, song name, or album
- **Multi-Sort** - Original order, artist, song, album, or duration
- **Duration Filter** - Find tracks within specific time ranges
- **Export from View** - Export filtered/sorted track lists

### 🎨 Professional UI
- **Boxed Display Framework** - Consistent 100-character width across all screens
- **Global Grid Alignment** - Labels, values, and columns perfectly aligned
- **Status Icons** - Clear visual indicators for actions and states
- **Hybrid Menu System** - Numbers for actions, letters for navigation

---

## 📦 Installation

### Prerequisites
- **Windows 10/11** (tested on Windows 10 Pro)
- **Python 3.12+** ([Download here](https://www.python.org/downloads/))
- **TIDAL Premium Subscription** (required for API access)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/msradel/tidal-playlist-tool.git
   cd tidal-playlist-tool
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python tidal_tool.py
   ```

4. **First-Time Authentication:**
   - The app will open your browser for OAuth login
   - Log in with your TIDAL credentials
   - Session tokens are saved locally (`.tidal_session_st.txt`)

---

## 🚀 Quick Start

### Main Menu
```
┌─ MAIN MENU ──────────────────────────────────────────────────────────────────────────────────────┐
│ 1. List playlists                                                                                │
│ 2. Export playlist by number                                                                     │
│ 3. Import playlist (JSON)                                                                        │
│ 4. Randomize playlist by number                                                                  │
│ 5. Show user dashboard                                                                           │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Common Workflows

**View and Sort Playlists:**
1. Select option `1` (List playlists)
2. Press `S` to change sort options
3. Choose field (name, tracks, duration, etc.)
4. Select ascending or descending order

**Randomize a Playlist:**
1. Select option `4` (Randomize)
2. Enter playlist number
3. Confirm creation of shuffled copy
4. New playlist appears with "[Shuffled]" suffix

**Export Playlist Data:**
1. Select option `2` (Export)
2. Enter playlist number
3. Choose format (JSON/CSV/TXT)
4. Files saved to `exports/` directory

---

## 📁 Project Structure

```
tidal-playlist-tool/
├── tidal_tool.py          # Main application (1900+ lines)
├── display_framework.py   # UI framework module
├── requirements.txt       # Python dependencies
├── LICENSE                # MIT License
├── README.md              # This file
├── .gitignore             # Git ignore rules
└── exports/               # Exported playlists (auto-created)
```

---

## 🛠️ Technical Details

### Technology Stack
- **Python 3.12.0** - Core language
- **tidalapi 0.8.10** - TIDAL API wrapper
- **pyperclip** - Clipboard integration (optional)
- **requests** - HTTP library

### Display Framework
- **Global Constants:**
  - `DISPLAY_WIDTH = 100` - Standard screen width
  - `LABEL_WIDTH = 19` - Right-aligned label position
  - `COL2_START = 48` - Second column start position
- **Box Drawing:** Unicode characters for consistent borders
- **Pagination:** 20 items per page standard

### API Integration
- **OAuth2 Device Flow** - Secure authentication
- **Session Persistence** - Tokens cached locally
- **Batch Operations** - 100 tracks per API call
- **Cache System** - 5-minute playlist cache (configurable)

---

## 🤝 Contributing

This project welcomes contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Use type hints where possible
- Add docstrings to all functions
- Maintain 100-character display width standard

---

## 💖 Support This Project

This tool is **100% free and open source**. If you find it useful, consider supporting its development:

### ☕ Buy Me a Coffee
- **PayPal:** [paypal.me/msradel](https://paypal.me/msradel)
- **Venmo:** [@msradel](https://venmo.com/msradel)
- **GitHub Sponsors:** [Sponsor this project](https://github.com/sponsors/msradel)

### 🌟 Other Ways to Help
- ⭐ Star this repository
- 🐛 Report bugs and request features
- 📝 Improve documentation
- 🔀 Submit pull requests
- 📢 Share with other TIDAL users

> **Note:** Donations support development time and infrastructure costs. This project remains free and open source regardless of funding.

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### TIDAL API Usage
**IMPORTANT:** This software uses the TIDAL API via the `tidalapi` library. TIDAL's Terms of Service **prohibit commercial use** of their API. This project is intended for **personal, non-commercial use only**.

- ✅ **Allowed:** Personal playlist management, backups, organization
- ❌ **Not Allowed:** Commercial services, reselling, public APIs

By using this tool, you agree to comply with [TIDAL's Terms of Service](https://tidal.com/terms).

---

## 🙏 Acknowledgments

- **[tidalapi](https://github.com/tamland/python-tidal)** - Excellent TIDAL API wrapper by @tamland
- **TIDAL** - For providing a high-quality music streaming service
- **Contributors** - Everyone who reports bugs and suggests features

---

## 📧 Contact

- **GitHub Issues:** [Report bugs or request features](https://github.com/msradel/tidal-playlist-tool/issues)
- **GitHub Profile:** [@msradel](https://github.com/msradel)

---

## 🗺️ Roadmap

### Priority 1 (Next Release)
- [ ] Complete UI standardization (all screens → boxed format)
- [ ] Enhanced playlist detail menu
- [ ] Full description display with word wrap
- [ ] Remove legacy `print_header()` calls

### Priority 2 (Future)
- [ ] Playlist search and filtering
- [ ] Advanced randomization (smart shuffle, artist spreading)
- [ ] Track management (add/remove individual tracks)
- [ ] Bulk export operations

### Priority 3 (Ideas)
- [ ] Export to Spotify format
- [ ] Playlist comparison tool
- [ ] Statistics dashboard
- [ ] Automated GitHub backups

---

**Made with ❤️ for the TIDAL community**
