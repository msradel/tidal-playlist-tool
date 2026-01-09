# Contributing to TIDAL Playlist Tool

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

---

## 🎯 Code of Conduct

- Be respectful and constructive in discussions
- Focus on improving the project for all users
- Follow the technical guidelines below
- Remember this is a non-commercial, personal-use tool

---

## 🐛 Reporting Bugs

### Before Submitting
1. Check [existing issues](https://github.com/msradel/tidal-playlist-tool/issues) to avoid duplicates
2. Update to the latest version
3. Test with a clean Python environment

### Bug Report Template
```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

**Expected behavior**
What you expected to happen.

**Environment:**
- OS: [e.g., Windows 10 Pro]
- Python Version: [e.g., 3.12.0]
- Tool Version: [e.g., v1.30.0]
- tidalapi Version: [e.g., 0.8.10]

**Error Messages**
Paste any error messages or tracebacks.
```

---

## ✨ Suggesting Features

### Feature Request Template
```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
What you want to happen.

**Describe alternatives you've considered**
Other approaches you've thought about.

**Additional context**
Screenshots, mockups, or examples.
```

---

## 🔧 Development Setup

### 1. Fork and Clone
```bash
git clone https://github.com/YOUR_USERNAME/tidal-playlist-tool.git
cd tidal-playlist-tool
```

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Make Changes
- Follow the code style guidelines below
- Test your changes thoroughly
- Update documentation if needed

### 5. Commit
```bash
git add .
git commit -m "feat: add amazing feature"
```

### 6. Push and Create PR
```bash
git push origin feature/your-feature-name
```
Then open a Pull Request on GitHub.

---

## 📝 Code Style Guidelines

### Python Style
- **PEP 8 compliance** - Use `pylint` or `black` for formatting
- **Type hints** - Add where possible
- **Docstrings** - All functions need docstrings
- **Comments** - Explain "why", not "what"

### Display Standards (CRITICAL!)
```python
# Global Constants
DISPLAY_WIDTH = 100      # All screens are 100 characters wide
LABEL_WIDTH = 19         # Labels right-aligned to position 19
COL2_START = 48          # Second column starts at position 48
```

### Example Function
```python
def export_playlist(self, playlist_id: str, format: str = 'json') -> bool:
    """
    Export playlist to specified format
    
    Args:
        playlist_id: TIDAL playlist UUID
        format: Export format ('json', 'csv', 'txt')
    
    Returns:
        True if export succeeded, False otherwise
    """
    # Implementation here
    pass
```

### UI Components
- **Always use** `DisplayBox` class for headers/footers
- **Never hardcode** display widths - use constants
- **Grid alignment** - Labels at position 19, values at 21
- **Status icons** - Use `STATUS_ICONS` dictionary

---

## 🧪 Testing

### Manual Testing Checklist
- [ ] Authentication flow works
- [ ] Playlists load and display correctly
- [ ] Pagination works (20 items/page)
- [ ] Sort options function properly
- [ ] Export creates valid files
- [ ] Randomization preserves all tracks
- [ ] No encoding errors with special characters
- [ ] Display width is exactly 100 characters

### Test Cases
1. **Small playlist** (< 20 tracks)
2. **Large playlist** (1000+ tracks)
3. **Unicode characters** (non-ASCII in titles)
4. **Empty playlist** (0 tracks)
5. **Editorial vs Owned** playlists

---

## 📄 Documentation

### Update When Changing:
- **README.md** - For user-facing features
- **Code comments** - For complex logic
- **Docstrings** - For all functions
- **CHANGELOG** - In main file header

### Version Updates
Update `VERSION` constant in `tidal_tool.py`:
```python
VERSION = "v1.31.0"  # Increment appropriately
```

---

## 🔄 Pull Request Process

### PR Checklist
- [ ] Code follows style guidelines
- [ ] All functions have docstrings
- [ ] Manual testing completed
- [ ] Documentation updated
- [ ] VERSION constant updated (if applicable)
- [ ] No merge conflicts

### PR Title Format
```
feat: add playlist search functionality
fix: correct duration calculation bug
docs: update installation instructions
refactor: improve display framework performance
```

### Review Process
1. Automated checks run (if configured)
2. Maintainer reviews code
3. Feedback provided if changes needed
4. PR merged when approved

---

## 🎨 Design Principles

### DRY (Don't Repeat Yourself)
- Use `display_framework.py` for all UI elements
- Reuse functions, don't duplicate code
- Extract common patterns into helpers

### User Experience
- Clear error messages
- Consistent navigation ([0] always means back/exit)
- Predictable behavior across screens
- Professional appearance

### Performance
- Cache playlist data (5-minute TTL)
- Batch API calls (100 items at a time)
- Paginate large result sets

---

## 📚 Resources

### Documentation
- [tidalapi GitHub](https://github.com/tamland/python-tidal)
- [TIDAL API (unofficial)](https://tidal.com/api)
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)

### Tools
- [Python 3.12 Downloads](https://www.python.org/downloads/)
- [VS Code](https://code.visualstudio.com/)
- [GitHub Desktop](https://desktop.github.com/)

---

## 🤝 Getting Help

- **Questions:** Open a [GitHub Discussion](https://github.com/msradel/tidal-playlist-tool/discussions)
- **Bugs:** File an [Issue](https://github.com/msradel/tidal-playlist-tool/issues)
- **Ideas:** Start a [Feature Request](https://github.com/msradel/tidal-playlist-tool/issues/new)

---

**Thank you for contributing!** 🎉
