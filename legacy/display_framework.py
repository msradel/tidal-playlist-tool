"""
TIDAL Playlist Tool - Display Framework Module
Centralized display system for consistent UI across all screens

Version: 1.0.0
License: MIT
"""

# ============================================================================
# GLOBAL DISPLAY CONSTANTS
# ============================================================================

DISPLAY_WIDTH = 100  # Total display width (characters)
CONTENT_WIDTH = 96   # Content between box borders (100 - 4 for │ │)
LABEL_WIDTH = 19     # All labels right-aligned to this position
COL2_START = 48      # Column 2 starts at middle (exactly half)
COL2_LABEL_WIDTH = 19 # Column 2 labels also right-aligned

# ============================================================================
# BOX DRAWING CHARACTERS
# ============================================================================

class BoxChars:
    """Unicode box drawing characters"""
    HORIZONTAL = '─'
    VERTICAL = '│'
    TOP_LEFT = '┌'
    TOP_RIGHT = '┐'
    BOTTOM_LEFT = '└'
    BOTTOM_RIGHT = '┘'
    HEADER_SEP = '─'

# ============================================================================
# DISPLAY BOX CLASS
# ============================================================================

class DisplayBox:
    """Unified box display system with global grid alignment"""
    
    def __init__(self, title=None):
        """Initialize display box with optional title"""
        self.title = title
        self.lines = []
    
    def print_header(self, title=None):
        """Print box header with title"""
        if title:
            self.title = title
        
        if self.title:
            # ┌─ TITLE ─────...─────┐ = 100 chars total
            prefix = f"{BoxChars.TOP_LEFT}{BoxChars.HEADER_SEP} {self.title} "
            suffix = BoxChars.TOP_RIGHT
            dashes_needed = DISPLAY_WIDTH - len(prefix) - len(suffix)
            print(f"{prefix}{BoxChars.HEADER_SEP * dashes_needed}{suffix}")
        else:
            print(f"{BoxChars.TOP_LEFT}{BoxChars.HEADER_SEP * (DISPLAY_WIDTH - 2)}{BoxChars.TOP_RIGHT}")
    
    def print_footer(self):
        """Print box footer"""
        print(f"{BoxChars.BOTTOM_LEFT}{BoxChars.HORIZONTAL * (DISPLAY_WIDTH - 2)}{BoxChars.BOTTOM_RIGHT}")
    
    def print_field(self, label, value):
        """Print single field with globally-aligned label and colon"""
        line = f"{label:>{LABEL_WIDTH}} : {value}"
        padded = f"{line:<{CONTENT_WIDTH}}"
        print(f"{BoxChars.VERTICAL} {padded} {BoxChars.VERTICAL}")
    
    def print_double_field(self, label1, value1, label2, value2):
        """Print two fields side-by-side with globally-aligned labels"""
        # Column 1: Label right-aligned to LABEL_WIDTH
        col1 = f"{label1:>{LABEL_WIDTH}} : {value1}"
        col1_padded = f"{col1:<{COL2_START}}"
        
        # Column 2: Label right-aligned to COL2_LABEL_WIDTH, starts at COL2_START
        col2 = f"{label2:>{COL2_LABEL_WIDTH}} : {value2}"
        col2_width = CONTENT_WIDTH - COL2_START
        col2_padded = f"{col2:<{col2_width}}"
        
        line = f"{col1_padded}{col2_padded}"
        print(f"{BoxChars.VERTICAL} {line} {BoxChars.VERTICAL}")
    
    def print_blank_line(self):
        """Print blank line inside box"""
        padded = " " * CONTENT_WIDTH
        print(f"{BoxChars.VERTICAL} {padded} {BoxChars.VERTICAL}")
    
    def print_text(self, text, align='left'):
        """Print plain text inside box with optional alignment"""
        if align == 'center':
            padded = f"{text:^{CONTENT_WIDTH}}"
        elif align == 'right':
            padded = f"{text:>{CONTENT_WIDTH}}"
        else:  # left
            padded = f"{text:<{CONTENT_WIDTH}}"
        print(f"{BoxChars.VERTICAL} {padded} {BoxChars.VERTICAL}")

# ============================================================================
# STARTUP INFO BOX
# ============================================================================

class StartupInfoBox(DisplayBox):
    """Specialized box for application startup information"""
    
    def __init__(self):
        super().__init__("APPLICATION INFO")
    
    def display(self, version, project, exports, browser):
        """Display startup info in unified box style"""
        self.print_header()
        self.print_field("Version", version)
        self.print_field("Project", project)
        self.print_field("Exports", exports)
        self.print_field("Browser", browser)
        self.print_footer()

# ============================================================================
# HEADER FUNCTIONS
# ============================================================================

def print_section_header(title):
    """Print section header (full width with title)"""
    separator = '=' * DISPLAY_WIDTH
    print(f"\n{separator}")
    print(f" {title}")
    print(separator)

def print_separator():
    """Print full-width separator line"""
    print('─' * DISPLAY_WIDTH)

# ============================================================================
# PAGINATION HELPER
# ============================================================================

class Paginator:
    """Simple pagination helper for lists"""
    
    def __init__(self, items, items_per_page=20):
        """Initialize paginator with items and page size"""
        self.items = items
        self.items_per_page = items_per_page
        self.total_items = len(items)
        self.total_pages = max(1, (self.total_items + items_per_page - 1) // items_per_page)
        self.current_page = 1
    
    def get_page(self, page_num):
        """Get items for specific page (1-indexed)"""
        if page_num < 1 or page_num > self.total_pages:
            return []
        start_idx = (page_num - 1) * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, self.total_items)
        return self.items[start_idx:end_idx]
    
    def get_current_page(self):
        """Get items for current page"""
        return self.get_page(self.current_page)
    
    def next_page(self):
        """Move to next page, return True if successful"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            return True
        return False
    
    def previous_page(self):
        """Move to previous page, return True if successful"""
        if self.current_page > 1:
            self.current_page -= 1
            return True
        return False
    
    def get_page_info(self):
        """Get pagination info string"""
        start_item = (self.current_page - 1) * self.items_per_page + 1
        end_item = min(self.current_page * self.items_per_page, self.total_items)
        return f"Page {self.current_page} of {self.total_pages} | Showing {start_item}-{end_item} of {self.total_items}"
