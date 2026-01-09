"""
AudioArchitect Backend Server Runner
Automatically detects terminal capabilities and adjusts display accordingly.
Usage: python -m backend.run
"""

import uvicorn
import os
import sys

def supports_ansi_colors():
    """
    Check if terminal supports ANSI color codes.
    Returns False in High Contrast mode or redirected output.
    """
    # Windows High Contrast mode disables ANSI rendering
    if os.getenv('HighContrastScheme'):
        return False
    
    # Check if output is going to a terminal (not redirected to file)
    if not (hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()):
        return False
    
    # Check for NO_COLOR environment variable (standard)
    if os.getenv('NO_COLOR'):
        return False
    
    return True

if __name__ == "__main__":
    if supports_ansi_colors():
        # ═══════════════════════════════════════════════════════
        # ANSI COLOR VERSION (Normal/Default Theme)
        # ═══════════════════════════════════════════════════════
        GOLD = "\033[93m"      # Bright yellow (AudioArchitect brand color)
        RESET = "\033[0m"      # Reset to default
        BOLD = "\033[1m"       # Bold text
        DIM = "\033[2m"        # Dimmed text
        
        print(f"""
    {GOLD}╔═══════════════════════════════════════════════════════╗
    ║           AudioArchitect Backend v2.0.0               ║
    ║        Build Your Perfect Music Library               ║
    ╠═══════════════════════════════════════════════════════╣{RESET}
    ║  {BOLD}Server:{RESET} http://127.0.0.1:8000                        ║
    ║  {BOLD}Docs:{RESET}   http://127.0.0.1:8000/docs                   ║
    {GOLD}╠═══════════════════════════════════════════════════════╣{RESET}
    ║  {DIM}Press CTRL+C to stop the server{RESET}                      ║
    {GOLD}╚═══════════════════════════════════════════════════════╝{RESET}
    """)
    else:
        # ═══════════════════════════════════════════════════════
        # PLAIN TEXT VERSION (High Contrast / Accessibility Mode)
        # ═══════════════════════════════════════════════════════
        print("""
    ╔═══════════════════════════════════════════════════════╗
    ║           AudioArchitect Backend v2.0.0               ║
    ║        Build Your Perfect Music Library               ║
    ╠═══════════════════════════════════════════════════════╣
    ║  Server: http://127.0.0.1:8000                        ║
    ║  Docs:   http://127.0.0.1:8000/docs                   ║
    ╠═══════════════════════════════════════════════════════╣
    ║  Press CTRL+C to stop the server                      ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    
    # Start the FastAPI server with auto-reload
    uvicorn.run(
        "backend.api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
