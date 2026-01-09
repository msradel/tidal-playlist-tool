#!/usr/bin/env python3
"""
Tidal Playlist Tool v1.30.1
Free, open-source Tidal playlist management tool
Windows 10 Pro | Python 3.12.0 | tidalapi 0.8.10

CHANGELOG v1.30.0:
- BASELINE: Established v1.30.0 as GitHub project baseline
- UPDATED: Migrated to GitHub repository for version control
- IMPROVED: Added MIT License with TIDAL API usage disclaimer
- ADDED: Comprehensive project documentation and donation support

CHANGELOG v1.24.6:
- FIXED: Cache timeout bug (used .seconds instead of .total_seconds())
- FIXED: Pagination safety for playlists with 1000+ tracks
- FIXED: Column width calculations to exactly 100 characters
- IMPROVED: Added error handling to all file export operations
- IMPROVED: Removed unused CONFIG variable
- IMPROVED: Added constants for magic numbers (cache time, batch size, etc.)
- IMPROVED: Added filename sanitization helper function

CHANGELOG v1.24.5:
- FIXED: Removed "Press Enter" prompt after [0] Exit from playlist list
- IMPROVED: Main loop now only pauses when appropriate (errors, info screens)
- IMPROVED: Smooth workflow when returning to main menu

CHANGELOG v1.24.4:
- FIXED: Standardized ALL display elements to 100 character width
- IMPROVED: Consistent header/footer format across all screens
- IMPROVED: Playlist list uses full words (Owned, Favorite, Editorial)
- IMPROVED: Sort arrow explanation in subtitle (^ = asc, v = desc)

CHANGELOG v1.24.3:
- IMPROVED: Track browser with expanded song column (40 chars)
- IMPROVED: Playlist detail view with word-wrapped descriptions
- IMPROVED: Compact 2-column stats layout in playlist details

CHANGELOG v1.24.2:
- IMPROVED: Playlist list view with type indicators and sort explanation
- IMPROVED: Legend moved above table for better clarity

CHANGELOG v1.24.1:
- ADDED: Standardized display width (100 chars) for all screens
- ADDED: Consistent header/footer format across application

CHANGELOG v1.24.0:
- ADDED: Track browser (Level 3) with pagination, search, sort, filter
- ADDED: Export from track browser
- IMPROVED: Unified export functionality (JSON/CSV/TXT)

CHANGELOG v1.23.0:
- ADDED: Hybrid menu system (numbers for actions, letters for navigation)
- IMPROVED: Menu consistency across all screens

Author: AI Assistant + User Collaboration
License: Open Source
"""

import os
import sys
import json
import csv
import time
import random
import subprocess
import platform
import re
from pathlib import Path
from datetime import datetime, timedelta
import tidalapi
from display_framework import DisplayBox, StartupInfoBox, print_section_header, Paginator, DISPLAY_WIDTH

# Application Version
VERSION = "v1.30.1"
import requests

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

try:
    from tkinter import Tk, filedialog
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

# ============================================================================
# CONFIGURATION
# ============================================================================

CONFIG_PATH = Path("D:/Desktop/Randomizer/config.json")

# STANDARD WIDTH FOR ALL DISPLAYS
DISPLAY_WIDTH = 100
CACHE_TTL_SECONDS = 300  # 5 minutes
TIDAL_BATCH_SIZE = 100
TRACKS_PER_PAGE = 20

STATUS_ICONS = {
    "OK": "[OK]",
    "FAIL": "[FAIL]",
    "WARN": "[WARN]",
    "INFO": "[INFO]",
    "ERROR": "[ERROR]",
    "SUCCESS": "[SUCCESS]",
    "AUTH": "[AUTH]",
    "TIMER": "[TIME]",
    "LOAD": "[LOAD]",
        #     "USER": "[USER]",
    "STAR": "[*]",
    "ARROW": "[>]",
    "FILTER": "[FILTER]",
    "SORT": "[SORT]",
    "SUB": "[SUB]",
    "STATS": "[STATS]",
    "OWNED": "[OWNED]",
    "FAV": "[FAV]",
    "EDIT": "[EDITORIAL]",
    "PLAYLIST": "[PLAYLIST]",
    "TRACK": "[TRACK]",
}

TIDAL_CREDS_FILE = Path.home() / ".tidal_session_st.txt"

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title: str, subtitle: str = None):
    """Print standardized header (100 char width)"""
    print(f"\n{'='*DISPLAY_WIDTH}")
    print(f" {title}")
    if subtitle:
        print(f" {subtitle}")
    print(f"{'='*DISPLAY_WIDTH}")

def print_footer(actions: list, prompt: str):
    """
    Print standardized footer with actions and prompt (100 char width)

    Args:
        actions: List of tuples [(key, description), ...]
        prompt: What user should enter (e.g., "playlist # or action")
    """
    print(f"\n{'='*DISPLAY_WIDTH}")
    action_str = " | ".join([f"[{key}] {desc}" for key, desc in actions])
    print(action_str)
    print(f"{STATUS_ICONS['ARROW']} Enter {prompt}: ", end='')

def sanitize_filename(filename: str) -> str:
    """Remove invalid characters from filename"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def get_default_browser_windows() -> tuple[str, str]:
    """Get the default browser from Windows Registry"""
    try:
        from winreg import HKEY_CURRENT_USER, HKEY_CLASSES_ROOT, OpenKey, QueryValueEx

        reg_path = r'Software\Microsoft\Windows\Shell\Associations\UrlAssociations\https\UserChoice'
        with OpenKey(HKEY_CURRENT_USER, reg_path) as key:
            prog_id, _ = QueryValueEx(key, 'ProgId')

        reg_path = rf'{prog_id}\shell\open\command'
        with OpenKey(HKEY_CLASSES_ROOT, reg_path) as key:
            command, _ = QueryValueEx(key, '')

        match = re.match(r'"([^"]+)"', command)
        if match:
            exe_path = match.group(1)
            exe_lower = exe_path.lower()

            if 'firefox' in exe_lower:
                browser_name = "Firefox"
            elif 'chrome' in exe_lower:
                browser_name = "Chrome"
            elif 'msedge' in exe_lower or 'edge' in exe_lower:
                browser_name = "Edge"
            elif 'brave' in exe_lower:
                browser_name = "Brave"
            elif 'opera' in exe_lower:
                browser_name = "Opera"
            else:
                browser_name = "Unknown"

            return (browser_name, exe_path)

        return ("Unknown", None)

    except Exception as e:
        return ("Error", None)

def open_browser_smart(url: str) -> tuple[bool, str]:
    """Open URL in the TRUE system default browser"""
    if platform.system() == 'Windows':
        browser_name, browser_path = get_default_browser_windows()

        if browser_path and os.path.exists(browser_path):
            try:
                subprocess.Popen([browser_path, url], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
                return (True, f"{browser_name} (registry)")
            except Exception as e:
                pass

    try:
        import webbrowser
        webbrowser.open(url)
        return (True, "System default (fallback)")
    except Exception as e:
        return (False, f"Failed: {e}")

def copy_to_clipboard(text: str) -> bool:
    """Copy text to clipboard"""
    if not CLIPBOARD_AVAILABLE:
        return False
    try:
        pyperclip.copy(text)
        return True
    except:
        return False

def format_duration(seconds: int) -> str:
    """Convert seconds to HH:MM:SS or MM:SS format"""
    if seconds is None or seconds == 0:
        return "0:00"

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes}:{secs:02d}"

def format_date(date_obj) -> str:
    """Format datetime object to readable string"""
    if date_obj is None:
        return "Unknown"

    if isinstance(date_obj, str):
        try:
            date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
        except:
            return date_obj

    if isinstance(date_obj, datetime):
        return date_obj.strftime("%Y-%m-%d %H:%M")

    return str(date_obj)

def format_date_short(date_obj) -> str:
    """Format datetime object to short date string"""
    if date_obj is None:
        return "Unknown"

    if isinstance(date_obj, str):
        try:
            date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
        except:
            return date_obj

    if isinstance(date_obj, datetime):
        return date_obj.strftime("%Y-%m-%d")

    return str(date_obj)

def calculate_age(date_obj) -> str:
    """Calculate age from date"""
    if date_obj is None:
        return "Unknown"

    if isinstance(date_obj, str):
        try:
            date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
        except:
            return "Unknown"

    if isinstance(date_obj, datetime):
        now = datetime.now(date_obj.tzinfo) if date_obj.tzinfo else datetime.now()
        delta = now - date_obj

        years = delta.days // 365
        months = (delta.days % 365) // 30
        days = (delta.days % 365) % 30

        parts = []
        if years > 0:
            parts.append(f"{years} year{'s' if years != 1 else ''}")
        if months > 0:
            parts.append(f"{months} month{'s' if months != 1 else ''}")
        if days > 0 and years == 0:
            parts.append(f"{days} day{'s' if days != 1 else ''}")

        return ", ".join(parts) if parts else "Less than a day"

    return "Unknown"

def calculate_time_remaining(date_obj) -> str:
    """Calculate time remaining until date"""
    if date_obj is None:
        return "Unknown"

    if isinstance(date_obj, str):
        try:
            date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
        except:
            return "Unknown"

    if isinstance(date_obj, datetime):
        now = datetime.now(date_obj.tzinfo) if date_obj.tzinfo else datetime.now()
        delta = date_obj - now

        if delta.total_seconds() <= 0:
            return "EXPIRED"

        days = delta.days

        if days == 0:
            hours = delta.seconds // 3600
            return f"{hours} hours"
        elif days == 1:
            return "1 day"
        elif days < 30:
            return f"{days} days"
        elif days < 365:
            months = days // 30
            remaining_days = days % 30
            if remaining_days > 0:
                return f"{months} month{'s' if months != 1 else ''}, {remaining_days} day{'s' if remaining_days != 1 else ''}"
            return f"{months} month{'s' if months != 1 else ''}"
        else:
            years = days // 365
            remaining_days = days % 365
            months = remaining_days // 30
            if months > 0:
                return f"{years} year{'s' if years != 1 else ''}, {months} month{'s' if months != 1 else ''}"
            return f"{years} year{'s' if years != 1 else ''}"

    return "Unknown"

def truncate_string(text: str, max_length: int) -> str:
    """Truncate string to max length with ellipsis"""
    if text is None:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def wrap_text(text: str, width: int = 98, indent: str = "  ") -> str:
    """Wrap text to specified width with indentation (default 98 to fit 100 char display)"""
    if not text:
        return ""

    words = text.split()
    lines = []
    current_line = []
    current_length = len(indent)

    for word in words:
        word_length = len(word)

        # If adding this word would exceed width, start new line
        if current_length + word_length + 1 > width and current_line:
            lines.append(indent + ' '.join(current_line))
            current_line = [word]
            current_length = len(indent) + word_length
        else:
            current_line.append(word)
            current_length += word_length + 1

    # Add the last line
    if current_line:
        lines.append(indent + ' '.join(current_line))

    return '\n'.join(lines)

def fetch_raw_api_data(session, endpoint: str, params: dict = None):
    """Fetch raw JSON data from Tidal API"""
    try:
        headers = {
            'Authorization': f'Bearer {session.access_token}',
            'Accept': 'application/json'
        }

        base_url = 'https://api.tidal.com/v1'
        url = f'{base_url}/{endpoint}'

        if params is None:
            params = {}
        params['countryCode'] = session.country_code

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    except Exception as e:
        return None

# ============================================================================
# MAIN APPLICATION CLASS
# ============================================================================

class TidalTool:
    def __init__(self):
        self.session = None
        self.access_token = None
        self.user_id = None
        self.project_root = Path("D:/Desktop/Randomizer")
        self.exports_dir = self.project_root / "exports"
        self.exports_dir.mkdir(exist_ok=True)

        # Playlist cache
        self.playlists_cache = None
        self.cache_time = None

        # Playlist sort settings
        self.sort_by = "name"  # name, tracks, duration, created, updated, type
        self.sort_order = "asc"  # asc or desc

        # Track sort settings
        self.track_sort_by = "original"  # original, artist, song, album, duration
        self.track_sort_order = "asc"  # asc or desc

        # Display startup info
        clear_screen()
        self.print_startup_info()

    def print_startup_info(self):
        """Display startup information using unified box style"""
        startup = StartupInfoBox()
        startup.display(
            version=f"v{VERSION}",
            project=str(getattr(self, 'project_root', 'Unknown')),
            exports=str(getattr(self, 'exports_dir', 'Unknown')),
            browser=getattr(self, 'browser', 'Firefox')
        )
    # ========================================================================
    # AUTHENTICATION
    # ========================================================================

    def authenticate(self) -> bool:
        """OAuth authentication with session persistence"""
        try:
            tidal = tidalapi.Session()

            # Try to load existing session
            if TIDAL_CREDS_FILE.exists():
                try:
                    with open(TIDAL_CREDS_FILE, 'r') as file:
                        cred = [line.rstrip() for line in file]

                    expiry_time = datetime.strptime(cred[3], "%m/%d/%Y, %H:%M:%S.%f")

                    if expiry_time > datetime.now() and tidal.load_oauth_session(cred[0], cred[1], cred[2], expiry_time):
                        self.session = tidal
                        self.access_token = cred[1]
                        self.user_id = tidal.user.id

                        print(f"{STATUS_ICONS['SUCCESS']} Loaded existing session")
                        self.display_user_profile()
                        return True

                except Exception as e:
                    print(f"{STATUS_ICONS['WARN']} Session file invalid, re-authenticating...")
                    TIDAL_CREDS_FILE.unlink(missing_ok=True)

            # New authentication required
            print(f"\n{STATUS_ICONS['AUTH']} TIDAL AUTHENTICATION REQUIRED")
            print(f"{STATUS_ICONS['INFO']} Starting OAuth flow...")

            login_data, future = tidal.login_oauth()
            auth_url = login_data.verification_uri_complete

            print(f"\n{STATUS_ICONS['AUTH']} Authentication URL:")
            print(f"{STATUS_ICONS['ARROW']} {auth_url}")

            # Copy to clipboard
            if copy_to_clipboard(auth_url):
                print(f"{STATUS_ICONS['SUCCESS']} URL copied to clipboard!")

            # Open browser
            success, browser_info = open_browser_smart(auth_url)
            if success:
                print(f"{STATUS_ICONS['SUCCESS']} Opened in {browser_info}")
            else:
                print(f"{STATUS_ICONS['WARN']} Could not auto-open browser: {browser_info}")
                print(f"{STATUS_ICONS['INFO']} Please open the URL manually")

            print(f"\n{STATUS_ICONS['INFO']} Waiting for authentication...")
            print(f"{STATUS_ICONS['INFO']} Complete the login in your browser...")

            # Wait for authentication
            max_wait = 300  # 5 minutes
            start_time = time.time()

            while time.time() - start_time < max_wait:
                if tidal.check_login():
                    # Save credentials
                    creds = [
                        tidal.token_type,
                        tidal.access_token,
                        tidal.refresh_token,
                        tidal.expiry_time.strftime("%m/%d/%Y, %H:%M:%S.%f")
                    ]
                    TIDAL_CREDS_FILE.write_text('\n'.join(creds))

                    self.session = tidal
                    self.access_token = tidal.access_token
                    self.user_id = tidal.user.id

                    print(f"\n{STATUS_ICONS['SUCCESS']} AUTHENTICATION SUCCESSFUL!")
                    self.display_user_profile()
                    return True

                time.sleep(2)

            print(f"\n{STATUS_ICONS['FAIL']} Login timeout after {max_wait} seconds")
            return False

        except Exception as e:
            print(f"{STATUS_ICONS['ERROR']} Authentication error: {e}")
            import traceback
            traceback.print_exc()
            return False

    def display_user_profile(self):
        """Display compact user profile on startup"""
        if not self.session:
            return

        try:
            user = self.session.user

            print(f"\n{'='*70}")
        #             print(" USER PROFILE")  # REMOVED: Using APPLICATION INFO box instead
            print(f"{'='*70}")

            first_name = getattr(user, 'first_name', '')
            last_name = getattr(user, 'last_name', '')
            full_name = f"{first_name} {last_name}".strip() if first_name or last_name else "N/A"

            print(f"{STATUS_ICONS['USER']} Name: {full_name}")
            print(f"{STATUS_ICONS['USER']} Username: {getattr(user, 'username', 'N/A')}")
            print(f"{STATUS_ICONS['USER']} User ID: {user.id}")
            print(f"{STATUS_ICONS['USER']} Country: {self.session.country_code}")
            print(f"{'='*70}\n")

        except Exception as e:
            pass  # TODO: Handle exception
        #             print(f"{STATUS_ICONS['WARN']} Could not load user profile: {e}")  # REMOVED: Using APPLICATION INFO box instead

    # ========================================================================
    # PLAYLIST OPERATIONS
    # ========================================================================

    def get_all_playlists(self, force_refresh=False):
        """
        Fetch ALL playlists with caching

        Returns list of playlist dictionaries with metadata
        """
        # Check cache (valid for 5 minutes) - FIXED: use total_seconds()
        if not force_refresh and self.playlists_cache and self.cache_time:
            if (datetime.now() - self.cache_time).total_seconds() < CACHE_TTL_SECONDS:
                return self.playlists_cache

        if not self.session:
            print(f"{STATUS_ICONS['ERROR']} Not authenticated")
            return []

        print(f"\n{STATUS_ICONS['LOAD']} Fetching playlists...")

        try:
            api_start = time.time()

            # Fetch all playlists
            all_playlists = list(self.session.user.playlist_and_favorite_playlists())

            api_time = time.time() - api_start

            # Process playlists
            proc_start = time.time()
            playlists = []

            for idx, playlist in enumerate(all_playlists, 1):
                creator_name = "Unknown"
                creator_id = None
                is_owned = False
                playlist_type = getattr(playlist, 'type', 'UNKNOWN')

                try:
                    if hasattr(playlist, 'creator') and playlist.creator:
                        creator_name = getattr(playlist.creator, 'name', 'Unknown')
                        creator_id = getattr(playlist.creator, 'id', None)
                        is_owned = (creator_id == self.user_id)
                except (AttributeError, TypeError):
                    pass

                playlists.append({
                    'id': playlist.id,
                    'name': playlist.name,
                    'tracks_count': getattr(playlist, 'num_tracks', 0),
                    'videos_count': getattr(playlist, 'num_videos', 0),
                    'duration': getattr(playlist, 'duration', 0),
                    'created': getattr(playlist, 'created', None),
                    'last_updated': getattr(playlist, 'last_updated', None),
                    'last_item_added': getattr(playlist, 'last_item_added_at', None),
                    'public': getattr(playlist, 'public', False),
                    'description': getattr(playlist, 'description', ''),
                    'creator': creator_name,
                    'creator_id': creator_id,
                    'is_owned': is_owned,
                    'type': playlist_type,
                    'url': getattr(playlist, 'listen_url', ''),
                    'share_url': getattr(playlist, 'share_url', ''),
                    'picture': getattr(playlist, 'picture', None),
                    'square_picture': getattr(playlist, 'square_picture', None),
                })

                if idx % 5 == 0:
                    print(f"{STATUS_ICONS['INFO']} Processed {idx}/{len(all_playlists)} playlists...")

            processing_time = time.time() - proc_start

            print(f"{STATUS_ICONS['SUCCESS']} Found {len(playlists)} playlists")
            print(f"{STATUS_ICONS['TIMER']} Fetch: {api_time:.2f}s | Process: {processing_time:.2f}s | Total: {api_time + processing_time:.2f}s")

            # Cache results
            self.playlists_cache = playlists
            self.cache_time = datetime.now()

            return playlists

        except Exception as e:
            print(f"{STATUS_ICONS['ERROR']} Failed to fetch playlists: {e}")
            import traceback
            traceback.print_exc()
            return []

    def fetch_playlist_tracks(self, playlist_id: str):
        """
        Fetch all tracks from a playlist with pagination
        Returns list of track dictionaries with metadata
        """
        print(f"\n{STATUS_ICONS['LOAD']} Fetching tracks...")

        try:
            playlist = self.session.playlist(playlist_id)

            all_tracks = []
            offset = 0
            limit = 100

            while True:
                tracks = playlist.tracks(limit=limit, offset=offset)

                if not tracks:
                    break

                all_tracks.extend(tracks)


                if len(all_tracks) % 100 == 0:
                    print(f"{STATUS_ICONS['INFO']} Fetched {len(all_tracks)} tracks...")

                if len(tracks) < limit:
                    break

                offset += limit

            print(f"{STATUS_ICONS['SUCCESS']} Loaded {len(all_tracks)} tracks")

            # Convert to dictionaries for easier sorting/filtering
            track_dicts = []
            for idx, track in enumerate(all_tracks):
                track_dicts.append({
                    'index': idx + 1,
                    'track_obj': track,
                    'id': track.id,
                    'name': track.name,
                    'artist': track.artist.name if track.artist else "Unknown",
                    'album': track.album.name if track.album else "Unknown",
                    'duration': track.duration,
                })

            return track_dicts

        except Exception as e:
            print(f"{STATUS_ICONS['ERROR']} Failed to fetch tracks: {e}")
            return []

    def sort_playlists(self, playlists):
        """Sort playlists based on current settings"""
        reverse = (self.sort_order == "desc")

        if self.sort_by == "name":
            return sorted(playlists, key=lambda x: x['name'].lower(), reverse=reverse)
        elif self.sort_by == "tracks":
            return sorted(playlists, key=lambda x: x['tracks_count'], reverse=reverse)
        elif self.sort_by == "duration":
            return sorted(playlists, key=lambda x: x['duration'], reverse=reverse)
        elif self.sort_by == "created":
            return sorted(playlists, key=lambda x: x['created'] or datetime.min, reverse=reverse)
        elif self.sort_by == "updated":
            return sorted(playlists, key=lambda x: x['last_updated'] or datetime.min, reverse=reverse)
        elif self.sort_by == "type":
            return sorted(playlists, key=lambda x: (x['type'], x['name'].lower()), reverse=reverse)
        else:
            return playlists

    def sort_tracks(self, tracks):
        """Sort tracks based on current settings"""
        if self.track_sort_by == "original":
            # Keep original order
            return sorted(tracks, key=lambda x: x['index'])

        reverse = (self.track_sort_order == "desc")

        if self.track_sort_by == "artist":
            return sorted(tracks, key=lambda x: (x['artist'].lower(), x['name'].lower()), reverse=reverse)
        elif self.track_sort_by == "song":
            return sorted(tracks, key=lambda x: x['name'].lower(), reverse=reverse)
        elif self.track_sort_by == "album":
            return sorted(tracks, key=lambda x: (x['album'].lower(), x['index']), reverse=reverse)
        elif self.track_sort_by == "duration":
            return sorted(tracks, key=lambda x: x['duration'], reverse=reverse)
        else:
            return tracks

    def list_playlists_table(self):
        """Display playlists in paginated table with global grid alignment"""
        playlists = self.get_all_playlists()

        if not playlists:
            print(f"{STATUS_ICONS['WARN']} No playlists found")
            return

        # Sort playlists
        sorted_playlists = self.sort_playlists(playlists)

        # Create paginator (20 items per page)
        paginator = Paginator(sorted_playlists, items_per_page=20)

        while True:
            clear_screen()
            self.print_startup_info()

            # Get current page items
            page_items = paginator.get_current_page()

            # Build title with counts
            total_count = len(sorted_playlists)
            page_info = paginator.get_page_info()
            title = f"YOUR PLAYLISTS ({total_count} total) - {page_info}"

            # Show sort info
            sort_indicator = "^" if self.sort_order == "asc" else "v"
            sort_subtitle = f"Sorted by: {self.sort_by.upper()} {sort_indicator} (^ = asc, v = desc)"

            # Create display box
            box = DisplayBox(title)
            box.print_header()

            # Print subtitle
            box.print_text(sort_subtitle, align='left')

            # Print separator line
            print(f"├{'─' * (DISPLAY_WIDTH - 2)}┤")

            # Print column headers (left-aligned labels, right-aligned numbers)
            header = f"  #  {'Name':<42} {'Type':<10} {'Tracks':>6}  {'Duration':>10}  {'Updated':>10}"
            padded_header = f"{header:<96}"
            print(f"│ {padded_header} │")

            # Print separator line
            print(f"├{'─' * (DISPLAY_WIDTH - 2)}┤")

            # Print playlist rows
            start_num = (paginator.current_page - 1) * paginator.items_per_page

            for idx, pl in enumerate(page_items, start=start_num + 1):
                # Format playlist number (right-aligned in 3 chars)
                num = f"{idx:>3}"

                # Truncate name to 42 chars
                name = pl['name']
                if len(name) > 48:
                    name = name[:45] + "..."
                name = f"{name:<48}"

                # Format type with proper labels (left-aligned, 10 chars)
                if pl.get('is_owned'):
                    type_label = "Owned"
                elif pl.get('is_favorite'):
                    type_label = "Favorite"
                else:
                    type_label = "Editorial"
                pl_type = f"{type_label:<10}"

                # Format tracks count (right-aligned, 6 chars)
                tracks = f"{pl['tracks_count']:>6}"

                # Format duration (right-aligned, 10 chars)
                duration = format_duration(pl['duration'])
                duration = f"{duration:>10}"

                # Format date (right-aligned, 10 chars)
                date_str = pl['last_updated'].strftime("%Y-%m-%d") if pl.get('last_updated') else "N/A"
                date_str = f"{date_str:>10}"

                # Build complete row
                row = f"{num}  {name} {pl_type} {tracks}  {duration}  {date_str}"
                padded_row = f"{row:<96}"
                print(f"│ {padded_row} │")

            # Print footer
            box.print_footer()

            # Navigation menu
            print(f"\n{'=' * DISPLAY_WIDTH}")
            nav_items = []

            if paginator.current_page > 1:
                nav_items.append("[P] Previous Page")
            if paginator.current_page < paginator.total_pages:
                nav_items.append("[N] Next Page")

            nav_items.extend(["[S] Sort", "[R] Refresh", "[0] Exit"])
            print(f"{' | '.join(nav_items)}")
            print(f"{'=' * DISPLAY_WIDTH}")

            # Get user input
            user_input = input("[>] Enter playlist # or action: ").strip().lower()

            # Handle navigation
            if user_input == 'n' and paginator.current_page < paginator.total_pages:
                paginator.next_page()
                continue
            elif user_input == 'p' and paginator.current_page > 1:
                paginator.previous_page()
                continue
            elif user_input == 's':
                # Call existing sort menu
                self.playlist_sort_menu()
                sorted_playlists = self.sort_playlists(self.get_all_playlists())
                paginator = Paginator(sorted_playlists, items_per_page=20)
                continue
            elif user_input == 'r':
                # Refresh playlists
                sorted_playlists = self.sort_playlists(self.get_all_playlists(force_refresh=True))
                paginator = Paginator(sorted_playlists, items_per_page=20)
                continue
            elif user_input == '0':
                return
            elif user_input.isdigit():
                # Select playlist by number
                playlist_num = int(user_input)
                if 1 <= playlist_num <= len(sorted_playlists):
                    selected_playlist = sorted_playlists[playlist_num - 1]
                    # Call the playlist menu with selected playlist
                    self.playlist_menu(selected_playlist)
                else:
                    print(f"{STATUS_ICONS['ERROR']} Invalid playlist number")
                    input("Press Enter to continue...")
            else:
                print(f"{STATUS_ICONS['ERROR']} Invalid input")
                input("Press Enter to continue...")

    def playlist_menu(self, playlist):
        """Display playlist details and available actions"""
        while True:
            clear_screen()
            self.print_startup_info()

            # Create playlist info box
            box = DisplayBox(f"PLAYLIST: {playlist['name']}")
            box.print_header()

            # Playlist metadata
            box.print_field("Type", playlist['type'])
            box.print_field("Tracks", str(playlist['tracks_count']))
            box.print_field("Duration", format_duration(playlist['duration']))

            if playlist.get('description'):
                box.print_text("")  # Blank line
                box.print_text("Description:", align='left')

                # Word wrap description to fit in box (94 chars per line)
                desc = playlist['description']
                import textwrap
                wrapped_lines = textwrap.wrap(desc, width=94)

                for line in wrapped_lines:
                    box.print_text(line, align='left')

            box.print_footer()

            # Action menu
            print(f"\n{'=' * DISPLAY_WIDTH}")
            print("Available Actions:")
            print("  1. View tracks")
            print("  2. Export playlist")
            print("  3. Randomize playlist")
            print(f"{'=' * DISPLAY_WIDTH}")
            print("[1-3] Select action | [0] Back")
            print(f"{'=' * DISPLAY_WIDTH}")

            choice = input("[>] Enter option: ").strip()

            if choice == '0':
                return
            elif choice == '1':
                # View tracks (to be implemented)
                print(f"\n{STATUS_ICONS['INFO']} Track viewing coming soon!")
                input("Press Enter to continue...")
            elif choice == '2':
                # Export playlist
                self.export_playlist(playlist['uuid'])
                input("Press Enter to continue...")
            elif choice == '3':
                # Randomize playlist
                self.randomize_playlist(playlist['uuid'])
                input("Press Enter to continue...")
            else:
                print(f"{STATUS_ICONS['ERROR']} Invalid option")
                input("Press Enter to continue...")
    def change_sort_settings(self):
        """Change sort settings with STANDARDIZED HEADER/FOOTER"""
        clear_screen()

        print_header("SORT OPTIONS", f"Current: {self.sort_by.upper()} ({self.sort_order.upper()})")

        print("\n1. Name")
        print("2. Tracks")
        print("3. Duration")
        print("4. Created")
        print("5. Updated")
        print("6. Type")

        actions = [('1-6', 'Select field'), ('0', 'Cancel')]
        print_footer(actions, "option")

        try:
            choice = input().strip()

            if choice == '0':
                return

            sort_map = {
                '1': 'name',
                '2': 'tracks',
                '3': 'duration',
                '4': 'created',
                '5': 'updated',
                '6': 'type'
            }

            if choice in sort_map:
                self.sort_by = sort_map[choice]

                # Ask for order
                clear_screen()
                print_header("SORT ORDER")
                print("\n1. Ascending (A-Z, 0-9, oldest-newest)")
                print("2. Descending (Z-A, 9-0, newest-oldest)")

                actions = [('1-2', 'Select order')]
                print_footer(actions, "option")

                order = input().strip()

                if order == '2':
                    self.sort_order = 'desc'
                else:
                    self.sort_order = 'asc'

                print(f"\n{STATUS_ICONS['SUCCESS']} Sort changed to: {self.sort_by.upper()} ({self.sort_order.upper()})")
                time.sleep(1)
            else:
                print(f"{STATUS_ICONS['ERROR']} Invalid choice")
                time.sleep(1)

        except Exception as e:
            print(f"{STATUS_ICONS['ERROR']} Error: {e}")
            time.sleep(1)

    def change_track_sort_settings(self):
        """Change track sort settings with STANDARDIZED HEADER/FOOTER"""
        clear_screen()

        print_header("TRACK SORT OPTIONS", f"Current: {self.track_sort_by.upper()}" + 
                    (f" ({self.track_sort_order.upper()})" if self.track_sort_by != 'original' else ""))

        print("\n1. Original order")
        print("2. Artist")
        print("3. Song name")
        print("4. Album")
        print("5. Duration")

        actions = [('1-5', 'Select field'), ('0', 'Cancel')]
        print_footer(actions, "option")

        try:
            choice = input().strip()

            if choice == '0':
                return

            sort_map = {
                '1': 'original',
                '2': 'artist',
                '3': 'song',
                '4': 'album',
                '5': 'duration'
            }

            if choice in sort_map:
                self.track_sort_by = sort_map[choice]

                # Ask for order (skip if original)
                if self.track_sort_by != 'original':
                    clear_screen()
                    print_header("SORT ORDER")
                    print("\n1. Ascending (A-Z, 0-9, shortest-longest)")
                    print("2. Descending (Z-A, 9-0, longest-shortest)")

                    actions = [('1-2', 'Select order')]
                    print_footer(actions, "option")

                    order = input().strip()

                    if order == '2':
                        self.track_sort_order = 'desc'
                    else:
                        self.track_sort_order = 'asc'

                print(f"\n{STATUS_ICONS['SUCCESS']} Sort changed to: {self.track_sort_by.upper()}" + 
                      (f" ({self.track_sort_order.upper()})" if self.track_sort_by != 'original' else ""))
                time.sleep(1)
            else:
                print(f"{STATUS_ICONS['ERROR']} Invalid choice")
                time.sleep(1)

        except Exception as e:
            print(f"{STATUS_ICONS['ERROR']} Error: {e}")
            time.sleep(1)

    def filter_tracks_by_duration(self, tracks):
        """Filter tracks by duration range with STANDARDIZED HEADER/FOOTER"""
        clear_screen()

        print_header("FILTER BY DURATION")

        print(f"\n{STATUS_ICONS['INFO']} Enter duration range in seconds")
        print(f"{STATUS_ICONS['INFO']} Leave blank to skip min/max")
        print(f"{STATUS_ICONS['INFO']} Examples: 180 = 3 minutes, 300 = 5 minutes")

        try:
            min_dur = input(f"\n{STATUS_ICONS['ARROW']} Minimum duration (seconds, or blank): ").strip()
            max_dur = input(f"{STATUS_ICONS['ARROW']} Maximum duration (seconds, or blank): ").strip()

            filtered = tracks

            if min_dur.isdigit():
                filtered = [t for t in filtered if t['duration'] >= int(min_dur)]
                print(f"{STATUS_ICONS['SUCCESS']} Applied minimum: {min_dur}s ({format_duration(int(min_dur))})")

            if max_dur.isdigit():
                filtered = [t for t in filtered if t['duration'] <= int(max_dur)]
                print(f"{STATUS_ICONS['SUCCESS']} Applied maximum: {max_dur}s ({format_duration(int(max_dur))})")

            if min_dur or max_dur:
                print(f"{STATUS_ICONS['SUCCESS']} Found {len(filtered)} tracks in duration range")
            else:
                print(f"{STATUS_ICONS['INFO']} No filter applied")

            time.sleep(1)
            return filtered

        except Exception as e:
            print(f"{STATUS_ICONS['ERROR']} Filter error: {e}")
            time.sleep(1)
            return tracks

    def show_playlist_details(self, playlist_data):
        """Show detailed view of a single playlist with STANDARDIZED WIDTH (100 chars)"""
        clear_screen()

        # STANDARDIZED HEADER (100 chars)
        print_header(playlist_data['name'])

        # Type badge
        if playlist_data['is_owned']:
            type_badge = f"{STATUS_ICONS['OWNED']} USER PLAYLIST"
        elif playlist_data['type'] == 'EDITORIAL':
            type_badge = f"{STATUS_ICONS['EDIT']} EDITORIAL PLAYLIST"
        else:
            type_badge = f"{STATUS_ICONS['FAV']} FAVORITED PLAYLIST"

        print(f"\n{type_badge}")
        print(f"Creator: {playlist_data['creator']}")

        # Description (if exists)
        if playlist_data['description']:
            desc = playlist_data['description'].strip()
            print(f"\n{wrap_text(desc, width=98, indent='')}")

        # Stats section (compact, 2-column layout, 100 char width)
        print(f"\n{'-'*DISPLAY_WIDTH}")
        print(f"Tracks: {playlist_data['tracks_count']:<20} Duration: {format_duration(playlist_data['duration'])}")
        print(f"Videos: {playlist_data['videos_count']:<20} Public: {'Yes' if playlist_data['public'] else 'No'}")
        print(f"Created: {format_date_short(playlist_data['created']):<19} Updated: {format_date_short(playlist_data['last_updated'])}")
        print(f"{'-'*DISPLAY_WIDTH}")

        # STANDARDIZED FOOTER (100 chars)
        actions = [
            ('1', 'View tracks'),
            ('2', 'Export'),
            ('3', 'Open in browser'),
            ('4', 'Randomize'),
            ('0', 'Back')
        ]
        print_footer(actions, "option")

        try:
            choice = input().strip()

            if choice == '0':
                self.list_playlists_table()
            elif choice == '1':
                # Reset track sort to original when entering track view
                self.track_sort_by = "original"
                self.track_sort_order = "asc"
                self.view_playlist_tracks(playlist_data)
            elif choice == '2':
                self.export_playlist_unified(playlist_data)
            elif choice == '3':
                success, info = open_browser_smart(playlist_data['url'])
                if success:
                    print(f"\n{STATUS_ICONS['SUCCESS']} Opened in {info}")
                else:
                    print(f"\n{STATUS_ICONS['ERROR']} Failed: {info}")
                input(f"\n{STATUS_ICONS['INFO']} Press Enter to continue...")
                self.show_playlist_details(playlist_data)
            elif choice == '4':
                self.randomize_playlist_unified(playlist_data)
            else:
                print(f"\n{STATUS_ICONS['ERROR']} Invalid choice")
                input(f"\n{STATUS_ICONS['INFO']} Press Enter to continue...")
                self.show_playlist_details(playlist_data)

        except Exception as e:
            print(f"\n{STATUS_ICONS['ERROR']} Error: {e}")
            input(f"\n{STATUS_ICONS['INFO']} Press Enter to continue...")
            self.show_playlist_details(playlist_data)

    def view_playlist_tracks(self, playlist_data, page=1, search_term=None, filtered_tracks=None):
        """View tracks with EXPANDED song column - FIXED column widths (100 chars total)"""
        # Fetch tracks (only once, then reuse)
        if filtered_tracks is None:
            all_tracks = self.fetch_playlist_tracks(playlist_data['id'])
            filtered_tracks = all_tracks
        else:
            all_tracks = filtered_tracks

        if not all_tracks:
            print(f"{STATUS_ICONS['WARN']} No tracks found")
            input(f"\n{STATUS_ICONS['INFO']} Press Enter to continue...")
            self.show_playlist_details(playlist_data)
            return

        # Apply search filter
        if search_term:
            filtered_tracks = [
                t for t in all_tracks
                if search_term.lower() in t['name'].lower() or
                   search_term.lower() in t['artist'].lower() or
                   search_term.lower() in t['album'].lower()
            ]
            tracks_to_show = filtered_tracks
        else:
            tracks_to_show = all_tracks

        # Apply sorting
        tracks_to_show = self.sort_tracks(tracks_to_show)

        total_tracks = len(tracks_to_show)

        if total_tracks == 0:
            print(f"{STATUS_ICONS['WARN']} No tracks match current filters")
            input(f"\n{STATUS_ICONS['INFO']} Press Enter to continue...")
            self.view_playlist_tracks(playlist_data, page=1, search_term=None, filtered_tracks=all_tracks)
            return

        # Pagination
        per_page = TRACKS_PER_PAGE
        total_pages = (total_tracks + per_page - 1) // per_page
        page = max(1, min(page, total_pages))

        start_idx = (page - 1) * per_page
        end_idx = min(start_idx + per_page, total_tracks)
        page_tracks = tracks_to_show[start_idx:end_idx]

        # Display with STANDARDIZED HEADER (100 chars)
        clear_screen()

        subtitle_parts = [f"Page {page}/{total_pages} (showing {start_idx+1}-{end_idx} of {total_tracks})"]

        print_header(f"TRACKS: {playlist_data['name']}", " | ".join(subtitle_parts))

        # Status line (filters/sort)
        status_parts = []
        if search_term:
            status_parts.append(f"Search: '{search_term}'")
        if self.track_sort_by != "original":
            sort_arrow = "^" if self.track_sort_order == "asc" else "v"
            status_parts.append(f"Sort: {self.track_sort_by.upper()} {sort_arrow}")
        if len(all_tracks) != len(tracks_to_show):
            status_parts.append(f"Filtered: {len(tracks_to_show)}/{len(all_tracks)}")

        if status_parts:
            print(f"\n{STATUS_ICONS['FILTER']} {' | '.join(status_parts)}")

        # FIXED: Column widths now total exactly 100 (6+20+38+20+10+6=100)
        print(f"\n{'#':<6} {'Artist':<20} {'Song':<38} {'Album':<20} {'Duration':<10}")
        print("-" * DISPLAY_WIDTH)

        for track_dict in page_tracks:
            artist = truncate_string(track_dict['artist'], 20)
            song = truncate_string(track_dict['name'], 38)  # FIXED: was 40
            album = truncate_string(track_dict['album'], 20)
            duration = format_duration(track_dict['duration'])

            print(f"{track_dict['index']:<6} {artist:<20} {song:<38} {album:<20} {duration:<10}")

        print("-" * DISPLAY_WIDTH)

        # COMPACT FOOTER (fits in 100 chars)
        actions = [
            ('N', 'Next'),
            ('P', 'Prev'),
            ('A', 'All'),
            ('S', 'Search'),
            ('O', 'Sort'),
            ('F', 'Filter'),
            ('E', 'Export'),
            ('0', 'Back')
        ]
        print_footer(actions, "action")

        try:
            choice = input().strip().upper()

            if choice == '0':
                # Reset sort when leaving
                self.track_sort_by = "original"
                self.track_sort_order = "asc"
                self.show_playlist_details(playlist_data)
            elif choice == 'N':
                if page < total_pages:
                    self.view_playlist_tracks(playlist_data, page=page+1, search_term=search_term, filtered_tracks=all_tracks)
                else:
                    print(f"\n{STATUS_ICONS['INFO']} Already on last page")
                    input(f"\n{STATUS_ICONS['INFO']} Press Enter to continue...")
                    self.view_playlist_tracks(playlist_data, page=page, search_term=search_term, filtered_tracks=all_tracks)
            elif choice == 'P':
                if page > 1:
                    self.view_playlist_tracks(playlist_data, page=page-1, search_term=search_term, filtered_tracks=all_tracks)
                else:
                    print(f"\n{STATUS_ICONS['INFO']} Already on first page")
                    input(f"\n{STATUS_ICONS['INFO']} Press Enter to continue...")
                    self.view_playlist_tracks(playlist_data, page=page, search_term=search_term, filtered_tracks=all_tracks)
            elif choice == 'A':
                self.view_all_tracks(playlist_data, tracks_to_show, search_term, all_tracks)
            elif choice == 'S':
                search = input(f"\n{STATUS_ICONS['ARROW']} Search artist/song/album (or blank to clear): ").strip()
                self.view_playlist_tracks(playlist_data, page=1, search_term=search if search else None, filtered_tracks=all_tracks)
            elif choice == 'O':
                self.change_track_sort_settings()
                self.view_playlist_tracks(playlist_data, page=1, search_term=search_term, filtered_tracks=all_tracks)
            elif choice == 'F':
                new_filtered = self.filter_tracks_by_duration(all_tracks)
                self.view_playlist_tracks(playlist_data, page=1, search_term=search_term, filtered_tracks=new_filtered)
            elif choice == 'E':
                self.export_playlist_unified(playlist_data)
                self.view_playlist_tracks(playlist_data, page=page, search_term=search_term, filtered_tracks=all_tracks)
            else:
                print(f"\n{STATUS_ICONS['ERROR']} Invalid choice")
                input(f"\n{STATUS_ICONS['INFO']} Press Enter to continue...")
                self.view_playlist_tracks(playlist_data, page=page, search_term=search_term, filtered_tracks=all_tracks)

        except Exception as e:
            print(f"\n{STATUS_ICONS['ERROR']} Error: {e}")
            input(f"\n{STATUS_ICONS['INFO']} Press Enter to continue...")
            self.view_playlist_tracks(playlist_data, page=page, search_term=search_term, filtered_tracks=all_tracks)

    def view_all_tracks(self, playlist_data, tracks, search_term, all_tracks):
        """Display all tracks without pagination with EXPANDED song column - FIXED widths (100 chars)"""
        clear_screen()

        print_header(f"ALL TRACKS: {playlist_data['name']}", f"Total: {len(tracks)} tracks")

        # Status line
        status_parts = []
        if search_term:
            status_parts.append(f"Search: '{search_term}'")
        if self.track_sort_by != "original":
            sort_arrow = "^" if self.track_sort_order == "asc" else "v"
            status_parts.append(f"Sort: {self.track_sort_by.upper()} {sort_arrow}")
        if len(all_tracks) != len(tracks):
            status_parts.append(f"Filtered: {len(tracks)}/{len(all_tracks)}")

        if status_parts:
            print(f"\n{STATUS_ICONS['FILTER']} {' | '.join(status_parts)}")

        # FIXED: Column widths (6+20+38+20+10+6=100)
        print(f"\n{'#':<6} {'Artist':<20} {'Song':<38} {'Album':<20} {'Duration':<10}")
        print("-" * DISPLAY_WIDTH)

        for track_dict in tracks:
            artist = truncate_string(track_dict['artist'], 20)
            song = truncate_string(track_dict['name'], 38)  # FIXED: was 40
            album = truncate_string(track_dict['album'], 20)
            duration = format_duration(track_dict['duration'])

            print(f"{track_dict['index']:<6} {artist:<20} {song:<38} {album:<20} {duration:<10}")

        print("-" * DISPLAY_WIDTH)

        # STANDARDIZED FOOTER (100 chars)
        actions = [('0', 'Back')]
        print_footer(actions, "action")

        input()
        self.view_playlist_tracks(playlist_data, page=1, search_term=search_term, filtered_tracks=all_tracks)

    def export_playlist_unified(self, playlist_data):
        """Export playlist with STANDARDIZED HEADER/FOOTER"""
        clear_screen()

        print_header("EXPORT PLAYLIST", playlist_data['name'])

        print("\n1. JSON (structured data)")
        print("2. CSV (spreadsheet)")
        print("3. TXT (plain text)")

        actions = [('1-3', 'Select format'), ('0', 'Cancel')]
        print_footer(actions, "option")

        try:
            choice = input().strip()

            if choice == '0':
                return  # Direct return, no pause

            if choice not in ['1', '2', '3']:
                print(f"\n{STATUS_ICONS['ERROR']} Invalid choice")
                input(f"\n{STATUS_ICONS['INFO']} Press Enter to continue...")
                self.export_playlist_unified(playlist_data)
                return

            # Fetch tracks
            all_tracks_dicts = self.fetch_playlist_tracks(playlist_data['id'])
            all_tracks = [t['track_obj'] for t in all_tracks_dicts]

            if not all_tracks:
                print(f"\n{STATUS_ICONS['ERROR']} No tracks to export")
                input(f"\n{STATUS_ICONS['INFO']} Press Enter to continue...")
                return

            # Export based on format
            if choice == '1':
                self.export_json(playlist_data, all_tracks)
            elif choice == '2':
                self.export_csv(playlist_data, all_tracks)
            elif choice == '3':
                self.export_txt(playlist_data, all_tracks)

            input(f"\n{STATUS_ICONS['INFO']} Press Enter to continue...")

        except Exception as e:
            print(f"\n{STATUS_ICONS['ERROR']} Export failed: {e}")
            import traceback
            traceback.print_exc()
            input(f"\n{STATUS_ICONS['INFO']} Press Enter to continue...")

    def export_json(self, playlist_data, tracks):
        """Export playlist to JSON format - FIXED: Added error handling"""
        export_data = {
            'playlist_name': playlist_data['name'],
            'playlist_id': playlist_data['id'],
            'playlist_type': playlist_data['type'],
            'is_owned': playlist_data['is_owned'],
            'creator': playlist_data['creator'],
            'total_tracks': len(tracks),
            'exported_at': datetime.now().isoformat(),
            'tracks': []
        }

        for track in tracks:
            export_data['tracks'].append({
                'id': track.id,
                'name': track.name,
                'artist': track.artist.name if track.artist else 'Unknown',
                'album': track.album.name if track.album else 'Unknown',
                'duration': track.duration,
                'track_number': getattr(track, 'track_num', None),
                'isrc': getattr(track, 'isrc', None),
            })

        filename = f"playlist_{playlist_data['id']}.json"
        filepath = self.exports_dir / filename

        # FIXED: Added error handling
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)

            print(f"\n{STATUS_ICONS['SUCCESS']} Exported {len(tracks)} tracks to JSON")
            print(f"{STATUS_ICONS['INFO']} Saved to: {filepath}")
        except (IOError, OSError) as e:
            print(f"\n{STATUS_ICONS['ERROR']} Failed to write file: {e}")

    def export_csv(self, playlist_data, tracks):
        """Export playlist to CSV format - FIXED: Added error handling"""
        filename = f"playlist_{playlist_data['id']}.csv"
        filepath = self.exports_dir / filename

        # FIXED: Added error handling
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)

                # Header
                writer.writerow(['#', 'Track ID', 'Artist', 'Song', 'Album', 'Duration', 'Track Number', 'ISRC'])

                # Rows
                for idx, track in enumerate(tracks, 1):
                    writer.writerow([
                        idx,
                        track.id,
                        track.artist.name if track.artist else 'Unknown',
                        track.name,
                        track.album.name if track.album else 'Unknown',
                        format_duration(track.duration),
                        getattr(track, 'track_num', ''),
                        getattr(track, 'isrc', ''),
                    ])

            print(f"\n{STATUS_ICONS['SUCCESS']} Exported {len(tracks)} tracks to CSV")
            print(f"{STATUS_ICONS['INFO']} Saved to: {filepath}")
        except (IOError, OSError) as e:
            print(f"\n{STATUS_ICONS['ERROR']} Failed to write file: {e}")

    def export_txt(self, playlist_data, tracks):
        """Export playlist to TXT format - FIXED: Added error handling"""
        filename = f"playlist_{playlist_data['id']}.txt"
        filepath = self.exports_dir / filename

        # FIXED: Added error handling
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Playlist: {playlist_data['name']}\n")
                f.write(f"ID: {playlist_data['id']}\n")
                f.write(f"Type: {playlist_data['type']}\n")
                f.write(f"Creator: {playlist_data['creator']}\n")
                f.write(f"Total Tracks: {len(tracks)}\n")
                f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"\n{'='*80}\n\n")

                for idx, track in enumerate(tracks, 1):
                    artist = track.artist.name if track.artist else 'Unknown'
                    album = track.album.name if track.album else 'Unknown'
                    duration = format_duration(track.duration)

                    f.write(f"{idx}. {track.name}\n")
                    f.write(f"   Artist: {artist} | Album: {album} | Duration: {duration}\n")
                    f.write(f"   Track ID: {track.id}\n\n")

            print(f"\n{STATUS_ICONS['SUCCESS']} Exported {len(tracks)} tracks to TXT")
            print(f"{STATUS_ICONS['INFO']} Saved to: {filepath}")
        except (IOError, OSError) as e:
            print(f"\n{STATUS_ICONS['ERROR']} Failed to write file: {e}")

    def randomize_playlist_unified(self, playlist_data):
        """Randomize playlist with STANDARDIZED HEADER/FOOTER"""
        new_name = f"{playlist_data['name']} [Shuffled]"

        clear_screen()

        print_header("RANDOMIZE PLAYLIST")

        print(f"\n{STATUS_ICONS['INFO']} This will create a new playlist:")
        print(f"{STATUS_ICONS['ARROW']} Original: {playlist_data['name']}")
        print(f"{STATUS_ICONS['ARROW']} New: {new_name}")

        actions = [('1', 'Yes, create shuffled playlist'), ('0', 'Cancel')]
        print_footer(actions, "option")

        confirm = input().strip()

        if confirm != '1':
            return  # Direct return, no pause

        try:
            # Fetch tracks
            all_tracks_dicts = self.fetch_playlist_tracks(playlist_data['id'])
            all_tracks = [t['track_obj'] for t in all_tracks_dicts]

            if not all_tracks:
                print(f"\n{STATUS_ICONS['ERROR']} No tracks found in playlist")
                input(f"\n{STATUS_ICONS['INFO']} Press Enter to continue...")
                return

            # Randomize track order
            print(f"\n{STATUS_ICONS['INFO']} Shuffling {len(all_tracks)} tracks...")
            random.shuffle(all_tracks)

            # Create new playlist
            print(f"{STATUS_ICONS['INFO']} Creating new playlist: {new_name}")
            new_playlist = self.session.user.create_playlist(new_name, "")

            # Add tracks in batches (API limit)
            print(f"{STATUS_ICONS['INFO']} Adding tracks to new playlist...")
            track_ids = [track.id for track in all_tracks]

            batch_size = TIDAL_BATCH_SIZE
            for i in range(0, len(track_ids), batch_size):
                batch = track_ids[i:i+batch_size]
                new_playlist.add(batch)
                print(f"{STATUS_ICONS['INFO']} Added {min(i+batch_size, len(track_ids))}/{len(track_ids)} tracks...")

            print(f"\n{STATUS_ICONS['SUCCESS']} Playlist created successfully!")
            print(f"{STATUS_ICONS['INFO']} Name: {new_name}")
            print(f"{STATUS_ICONS['INFO']} Tracks: {len(all_tracks)}")
            print(f"{STATUS_ICONS['INFO']} ID: {new_playlist.id}")

            # Invalidate cache
            self.playlists_cache = None

            input(f"\n{STATUS_ICONS['INFO']} Press Enter to continue...")
            self.list_playlists_table()

        except Exception as e:
            print(f"\n{STATUS_ICONS['ERROR']} Randomization failed: {e}")
            import traceback
            traceback.print_exc()
            input(f"\n{STATUS_ICONS['INFO']} Press Enter to continue...")

    def show_playlist_selection_table(self, title: str, action_callback):
        """
        UNIFIED TABLE VIEW for playlist selection (Export/Randomize)

        Args:
            title: Screen title (e.g., "EXPORT PLAYLIST" or "RANDOMIZE PLAYLIST")
            action_callback: Function to call with selected playlist_data
        """
        playlists = self.get_all_playlists()

        if not playlists:
            print(f"{STATUS_ICONS['WARN']} No playlists found")
            return

        # Sort playlists by name
        sorted_playlists = sorted(playlists, key=lambda x: x['name'].lower())

        clear_screen()

        print_header(title, f"{len(sorted_playlists)} playlists available")

        # REMOVED: Duplicate display code - using list_playlists_table() instead
        # STANDARDIZED FOOTER
        actions = [('1-' + str(len(sorted_playlists)), 'Select playlist'), ('0', 'Cancel')]
        print_footer(actions, "playlist #")

        try:
            choice = input().strip()

            if choice == '0':
                return  # Direct return, no pause

            idx = int(choice)
            if 1 <= idx <= len(sorted_playlists):
                action_callback(sorted_playlists[idx - 1])
            else:
                print(f"\n{STATUS_ICONS['ERROR']} Invalid playlist number")
                input(f"\n{STATUS_ICONS['INFO']} Press Enter to continue...")
                self.show_playlist_selection_table(title, action_callback)

        except ValueError:
            print(f"\n{STATUS_ICONS['ERROR']} Invalid input")
            input(f"\n{STATUS_ICONS['INFO']} Press Enter to continue...")
            self.show_playlist_selection_table(title, action_callback)

    def export_playlist_by_number(self):
        """Export playlist - now uses unified table view"""
        self.show_playlist_selection_table("EXPORT PLAYLIST", self.export_playlist_unified)

    def randomize_playlist(self):
        """Randomize playlist - now uses unified table view"""
        self.show_playlist_selection_table("RANDOMIZE PLAYLIST", self.randomize_playlist_unified)

    def import_playlist_json(self):
        """Import playlist from JSON file"""
        clear_screen()
        print_header("IMPORT PLAYLIST FROM JSON")
        print(f"\n{STATUS_ICONS['WARN']} Not yet implemented")
        input(f"\n{STATUS_ICONS['INFO']} Press Enter to continue...")

    def display_user_dashboard(self):
        """Display user dashboard with GLOBAL GRID ALIGNMENT"""
        if not self.session:
            print(f"{STATUS_ICONS['ERROR']} Not authenticated")
            return

        print(f"\n{STATUS_ICONS['LOAD']} Loading user dashboard...")

        try:
            user = self.session.user
            profile_metadata = getattr(user, 'profile_metadata', {})
            subscription_data = fetch_raw_api_data(self.session, f'users/{self.user_id}/subscription')

            clear_screen()
            self.print_startup_info()
            print_header("USER DASHBOARD")

            # ============================================================
            # GLOBAL GRID CONSTANTS - Used by ALL sections!
            # ============================================================
            CONTENT_WIDTH = 96
            LABEL_WIDTH = 19        # ALL labels align to this position
            COL2_START = 48         # Column 2 starts here (exactly middle)
            COL2_LABEL_WIDTH = 19   # Column 2 labels also align consistently

            def print_field(label, value):
                """Print single field with globally-aligned label"""
                line = f"{label:>{LABEL_WIDTH}} : {value}"
                padded = f"{line:<{CONTENT_WIDTH}}"
                print(f"│ {padded} │")

            def print_double_field(label1, value1, label2, value2):
                """Print two fields with globally-aligned labels"""
                # Column 1: Label right-aligned to LABEL_WIDTH
                col1 = f"{label1:>{LABEL_WIDTH}} : {value1}"
                col1_padded = f"{col1:<{COL2_START}}"

                # Column 2: Label right-aligned to COL2_LABEL_WIDTH, starts at COL2_START
                col2 = f"{label2:>{COL2_LABEL_WIDTH}} : {value2}"
                # Calculate remaining space for col2
                col2_width = CONTENT_WIDTH - COL2_START
                col2_padded = f"{col2:<{col2_width}}"

                line = f"{col1_padded}{col2_padded}"
                print(f"│ {line} │")

            # ================================================================
            # ACCOUNT INFORMATION
            # ================================================================
            print(f"┌─ ACCOUNT INFORMATION {'─' * (DISPLAY_WIDTH - 24)}┐")

            full_name = f"{getattr(user, 'first_name', '')} {getattr(user, 'last_name', '')}".strip()
            print_field("Name", full_name)

            email = getattr(user, 'email', 'N/A')
            email_verified = profile_metadata.get('emailVerified', False)
            verify_status = 'Verified' if email_verified else 'Not Verified'
            print_field("Email", f"{email} ({verify_status})")

            print_field("Username", getattr(user, 'username', 'N/A'))
            print_field("User ID", str(user.id))

            country = self.session.country_code
            locale = getattr(self.session, 'locale', 'N/A')
            print_double_field("Country", country, "Locale", locale)

            created = profile_metadata.get('created')
            if created:
                created_date = format_date_short(created)
                account_age = calculate_age(created)
                print_field("Created", f"{created_date} (Age: {account_age})")

            print_field("Date of Birth", profile_metadata.get('dateOfBirth', 'Not provided'))

            print(f"└{'─' * (DISPLAY_WIDTH - 2)}┘")

            # ================================================================
            # SUBSCRIPTION
            # ================================================================
            print(f"\n┌─ SUBSCRIPTION {'─' * (DISPLAY_WIDTH - 17)}┐")

            if subscription_data:
                sub_type = subscription_data.get('subscription', {}).get('type', 'Unknown')
                status = subscription_data.get('status', 'Unknown')
                print_double_field("Type", sub_type, "Status", status)

                quality = subscription_data.get('highestSoundQuality', 'Unknown')
                quality_display = f"{quality} (Lossless)" if quality == "HI_RES" else quality
                payment = subscription_data.get('paymentType', 'Unknown')
                print_double_field("Sound Quality", quality_display, "Payment", payment)

                start_date = subscription_data.get('startDate')
                if start_date:
                    start_display = format_date_short(start_date)
                    sub_age = calculate_age(start_date)
                    print_field("Started", f"{start_display} (Age: {sub_age})")

                valid_until = subscription_data.get('validUntil')
                if valid_until:
                    valid_display = format_date_short(valid_until)
                    time_remaining = calculate_time_remaining(valid_until)
                    print_field("Valid Until", f"{valid_display} ({time_remaining} remaining)")

                offline_grace = subscription_data.get('subscription', {}).get('offlineGracePeriod', 'N/A')
                premium = subscription_data.get('premiumAccess', False)
                print_double_field("Offline Grace", f"{offline_grace} days", "Premium Access", 'Yes' if premium else 'No')

                can_trial = subscription_data.get('canGetTrial', False)
                overdue = subscription_data.get('paymentOverdue', False)
                print_double_field("Trial Eligible", 'Yes' if can_trial else 'No', "Payment Overdue", 'Yes' if overdue else 'No')
            else:
                line = "Could not fetch subscription details"
                padded = f"{line:<{CONTENT_WIDTH}}"
                print(f"│ {padded} │")

            print(f"└{'─' * (DISPLAY_WIDTH - 2)}┘")

            # ================================================================
            # LIBRARY STATISTICS
            # ================================================================
            print(f"\n┌─ LIBRARY STATISTICS {'─' * (DISPLAY_WIDTH - 23)}┐")

            try:
                fav_tracks = len(list(self.session.user.favorites.tracks()))
            except:
                fav_tracks = 0

            try:
                fav_albums = len(list(self.session.user.favorites.albums()))
            except:
                fav_albums = 0

            try:
                fav_artists = len(list(self.session.user.favorites.artists()))
            except:
                fav_artists = 0

            try:
                fav_playlists = len(list(self.session.user.favorites.playlists()))
            except:
                fav_playlists = 0

            all_playlists = list(self.session.user.playlist_and_favorite_playlists())
            owned_playlists = [pl for pl in all_playlists if hasattr(pl, 'creator') and pl.creator and pl.creator.id == self.user_id]

            print_double_field("Favorite Tracks", str(fav_tracks), "Total Playlists", str(len(all_playlists)))
            print_double_field("Favorite Albums", str(fav_albums), "Owned Playlists", str(len(owned_playlists)))
            print_double_field("Favorite Artists", str(fav_artists), "Favorite Playlists", str(fav_playlists))

            print(f"└{'─' * (DISPLAY_WIDTH - 2)}┘")

            # ================================================================
            # PREFERENCES
            # ================================================================
            print(f"\n┌─ PREFERENCES {'─' * (DISPLAY_WIDTH - 16)}┐")

            newsletter = profile_metadata.get('newsletter', False)
            early_access = profile_metadata.get('earlyAccessProgram', False)

            newsletter_status = 'Subscribed' if newsletter else 'Not Subscribed'
            beta_status = 'Enrolled' if early_access else 'Not Enrolled'

            print_field("Newsletter", newsletter_status)
            print_field("Early Access", beta_status)

            print(f"└{'─' * (DISPLAY_WIDTH - 2)}┘")

            # ================================================================
            # SESSION INFO
            # ================================================================
            print(f"\n┌─ SESSION INFO {'─' * (DISPLAY_WIDTH - 17)}┐")

            audio_quality = getattr(self.session, 'audio_quality', 'N/A')
            video_quality = getattr(self.session, 'video_quality', 'N/A')
            expiry = getattr(self.session, 'expiry_time', None)

            print_double_field("Audio Quality", audio_quality, "Video Quality", video_quality)

            if expiry:
                expiry_display = expiry.strftime("%Y-%m-%d %H:%M")
                print_field("Token Expires", expiry_display)

            print(f"└{'─' * (DISPLAY_WIDTH - 2)}┘")

        except Exception as e:
            print(f"\n{STATUS_ICONS['ERROR']} Failed to load dashboard: {e}")
            import traceback
            traceback.print_exc()
    # ========================================================================
    # MAIN MENU
    # ========================================================================

    def show_menu(self):
        """Display main menu with STANDARDIZED HEADER/FOOTER"""
        print_header("TIDAL PLAYLIST TOOL v1.24.6 - MAIN MENU")

        print("\n1. List playlists")
        print("2. Export playlist by number")
        print("3. Import playlist (JSON)")
        print("4. Randomize playlist by number")
        print("5. Show user dashboard")

        actions = [('1-5', 'Select option'), ('0', 'Exit')]
        print_footer(actions, "option")

    def run(self):
        """Main application loop"""
        if not self.authenticate():
            print(f"\n{STATUS_ICONS['ERROR']} Authentication failed. Exiting.")
            return False

        while True:
            self.show_menu()

            try:
                choice = input().strip()

                if choice == '0':
                    print(f"\n{STATUS_ICONS['INFO']} Goodbye!")
                    return True
                elif choice == '1':
                    self.list_playlists_table()
                    # NO PAUSE - list_playlists_table() returns directly on [0]
                elif choice == '2':
                    self.export_playlist_by_number()
                elif choice == '3':
                    self.import_playlist_json()
                elif choice == '4':
                    self.randomize_playlist()
                elif choice == '5':
                    self.display_user_dashboard()
                    input(f"\n{STATUS_ICONS['INFO']} Press Enter to continue...")
                else:
                    print(f"\n{STATUS_ICONS['ERROR']} Invalid choice")
                    input(f"\n{STATUS_ICONS['INFO']} Press Enter to continue...")

                # Clear screen and refresh display for next iteration
                clear_screen()
                self.print_startup_info()
                if self.session:
                    self.display_user_profile()

            except KeyboardInterrupt:
                print(f"\n\n{STATUS_ICONS['INFO']} Operation cancelled")
                return True
            except Exception as e:
                print(f"\n{STATUS_ICONS['ERROR']} Error: {e}")
                import traceback
                traceback.print_exc()
                input(f"\n{STATUS_ICONS['INFO']} Press Enter to continue...")

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

    def main_menu(self):
        """Main menu with boxed formatting"""
        box = DisplayBox('MAIN MENU')
        box.print_header()

        # Menu options
        box.print_text('1. List playlists', align='left')
        box.print_text('2. Export playlist by number', align='left')
        box.print_text('3. Import playlist (JSON)', align='left')
        box.print_text('4. Randomize playlist by number', align='left')
        box.print_text('5. Show user dashboard', align='left')

        box.print_footer()

        # Footer navigation
        print(f"\n{'=' * DISPLAY_WIDTH}")
        print('[1-5] Select option | [0] Exit')
        print(f"{'=' * DISPLAY_WIDTH}")
        choice = input('[>] Enter option: ').strip()
        return choice

def main():
    """Application entry point"""
    try:
        tool = TidalTool()
        success = tool.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{STATUS_ICONS['INFO']} Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"{STATUS_ICONS['ERROR']} Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()




























