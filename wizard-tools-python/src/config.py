"""
Configuration settings for Wizard Tools application
"""
from typing import Dict, Tuple

# Application metadata
APP_NAME = "Wizard Tools"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Wizard Tools Team"

# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_MIN_WIDTH = 600
WINDOW_MIN_HEIGHT = 400

# Whole Foods Theme Colors
COLORS: Dict[str, str] = {
    # Primary colors
    "primary_green": "#2D5016",      # Dark forest green
    "secondary_green": "#6B8E23",    # Olive drab green
    "accent_green": "#8FBC8F",       # Dark sea green
    "light_green": "#90EE90",        # Light green
    
    # Neutral colors
    "beige": "#F5F5DC",              # Beige
    "cream": "#FFFDD0",              # Cream
    "light_gray": "#E8E8E8",         # Light gray
    "medium_gray": "#CCCCCC",        # Medium gray
    "dark_gray": "#666666",          # Dark gray
    
    # Earth tones
    "brown": "#8B4513",              # Saddle brown
    "tan": "#D2B48C",                # Tan
    "sand": "#F4A460",               # Sandy brown
    
    # UI colors
    "white": "#FFFFFF",
    "black": "#000000",
    "error_red": "#DC143C",          # Crimson
    "success_green": "#228B22",      # Forest green
    "warning_orange": "#FF8C00",     # Dark orange
    
    # Button states
    "button_bg": "#6B8E23",
    "button_hover": "#8FBC8F",
    "button_active": "#2D5016",
    "button_disabled": "#CCCCCC",
}

# Font settings
FONTS: Dict[str, Tuple[str, int, str]] = {
    "header": ("Segoe UI", 16, "bold"),
    "title": ("Segoe UI", 14, "bold"),
    "normal": ("Segoe UI", 10, "normal"),
    "small": ("Segoe UI", 9, "normal"),
    "button": ("Segoe UI", 10, "bold"),
    "monospace": ("Consolas", 10, "normal"),
}

# File settings
SUPPORTED_FILE_TYPES = [
    ("CSV files", "*.csv"),
    ("Excel files", "*.xlsx *.xls"),
    ("All files", "*.*"),
]

CHUNK_SIZE_OPTIONS = [100, 500, 1000, 5000, 10000, 50000]
DEFAULT_CHUNK_SIZE = 1000

# Text tool operations
TEXT_OPERATIONS = [
    "UPPERCASE",
    "lowercase",
    "Title Case",
    "Reverse",
    "Count Characters",
    "Count Words",
    "Clean Extra Spaces",
]

# Calculator buttons layout
CALCULATOR_BUTTONS = [
    ["7", "8", "9", "÷"],
    ["4", "5", "6", "×"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"],
    ["C", "CE", "←", ""],
]

# File processing settings
MAX_FILE_SIZE_MB = 500
EXCEL_ENGINE = "openpyxl"  # For .xlsx files
EXCEL_ENGINE_XLS = "xlrd"  # For .xls files

# Progress bar settings
PROGRESS_BAR_LENGTH = 400
PROGRESS_BAR_MODE = "determinate"

# Padding and spacing
PADDING = {
    "small": 5,
    "medium": 10,
    "large": 20,
}

# Tool descriptions
TOOL_DESCRIPTIONS = {
    "file_chunker": "Split large CSV/Excel files into smaller chunks",
    "file_combiner": "Combine multiple CSV/Excel files using Union or Join operations",
    "text_tools": "Transform and analyze text with various operations",
    "color_picker": "Pick colors and convert between HEX, RGB, and HSL formats",
    "calculator": "Perform basic arithmetic calculations",
}