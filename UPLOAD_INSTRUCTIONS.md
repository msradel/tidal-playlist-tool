# Upload Instructions for tidal_tool.py

## ⚠️ Action Required

The main application file `tidal_tool.py` needs to be uploaded to this repository.

### Option 1: GitHub Web Interface

1. Go to: https://github.com/msradel/tidal-playlist-tool
2. Click **Add file** → **Upload files**
3. Drag and drop `tidal_tool.py` from your local machine:
   - Location: `D:\Desktop\Randomizer\tidal_tool.py`
4. **IMPORTANT:** Before uploading, update the file:
   - Change line `VERSION = "v1.24.8"` to `VERSION = "v1.30.0"`
   - Update the docstring header from `v1.24.6` to `v1.30.0`
   - Add this to the top of the CHANGELOG:
   ```python
   CHANGELOG v1.30.0:
   - BASELINE: Established v1.30.0 as GitHub project baseline
   - UPDATED: Migrated to GitHub repository for version control
   - IMPROVED: Added MIT License with TIDAL API usage disclaimer
   - ADDED: Comprehensive project documentation and donation support
   ```
5. Commit message: `Add tidal_tool.py v1.30.0 - main application`
6. Click **Commit changes**

### Option 2: Git Command Line

```bash
# Navigate to your project directory
cd D:\Desktop\Randomizer

# Initialize git (if not already done)
git init

# Add remote
git remote add origin https://github.com/msradel/tidal-playlist-tool.git

# Pull latest changes
git pull origin main

# Make the version updates described above to tidal_tool.py

# Add the file
git add tidal_tool.py

# Commit
git commit -m "Add tidal_tool.py v1.30.0 - main application"

# Push
git push origin main
```

### Version Updates Required

**In tidal_tool.py, make these changes:**

1. **Line ~68** (VERSION constant):
   ```python
   # OLD:
   VERSION = "v1.24.8"
   
   # NEW:
   VERSION = "v1.30.0"
   ```

2. **Line ~4** (Docstring header):
   ```python
   # OLD:
   Tidal Playlist Tool v1.24.6
   
   # NEW:
   Tidal Playlist Tool v1.30.0
   ```

3. **After line ~9** (Add new changelog entry at the top):
   ```python
   CHANGELOG v1.30.0:
   - BASELINE: Established v1.30.0 as GitHub project baseline
   - UPDATED: Migrated to GitHub repository for version control  
   - IMPROVED: Added MIT License with TIDAL API usage disclaimer
   - ADDED: Comprehensive project documentation and donation support
   
   CHANGELOG v1.24.6:
   ...(existing changelog continues)...
   ```

4. **Line ~57** (License field):
   ```python
   # OLD:
   License: Open Source
   
   # NEW:
   License: MIT (Personal use only - TIDAL API non-commercial restriction)
   ```

### After Upload

Once `tidal_tool.py` is uploaded, delete this file:
```bash
git rm UPLOAD_INSTRUCTIONS.md
git commit -m "Remove upload instructions - tidal_tool.py now uploaded"
git push origin main
```

---

**Note:** This file exists because the automated push encountered size limitations. Manual upload ensures the complete source code is available in the repository.
