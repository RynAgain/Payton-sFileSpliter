"""
Helper utilities for Wizard Tools application
"""
import os
import zipfile
from pathlib import Path
from typing import List, Tuple, Optional
import colorsys


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: File size in bytes
        
    Returns:
        Formatted file size string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def get_file_extension(file_path: str) -> str:
    """
    Get file extension from file path
    
    Args:
        file_path: Path to the file
        
    Returns:
        File extension (lowercase, with dot)
    """
    return Path(file_path).suffix.lower()


def is_csv_file(file_path: str) -> bool:
    """
    Check if file is a CSV file
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if CSV file, False otherwise
    """
    return get_file_extension(file_path) == '.csv'


def is_excel_file(file_path: str) -> bool:
    """
    Check if file is an Excel file
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if Excel file, False otherwise
    """
    return get_file_extension(file_path) in ['.xlsx', '.xls']


def create_output_filename(
    base_name: str,
    suffix: str,
    extension: str,
    index: Optional[int] = None
) -> str:
    """
    Create output filename with suffix and optional index
    
    Args:
        base_name: Base filename without extension
        suffix: Suffix to add (e.g., '_chunk', '_combined')
        extension: File extension (with dot)
        index: Optional index number
        
    Returns:
        Output filename
    """
    if index is not None:
        return f"{base_name}{suffix}_{index}{extension}"
    return f"{base_name}{suffix}{extension}"


def create_zip_file(file_paths: List[str], zip_path: str) -> bool:
    """
    Create a ZIP file containing the specified files
    
    Args:
        file_paths: List of file paths to include
        zip_path: Path for the output ZIP file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in file_paths:
                if os.path.exists(file_path):
                    zipf.write(file_path, os.path.basename(file_path))
        return True
    except Exception as e:
        print(f"Error creating ZIP file: {e}")
        return False


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """
    Convert hex color to RGB
    
    Args:
        hex_color: Hex color code (e.g., '#FF0000' or 'FF0000')
        
    Returns:
        Tuple of (r, g, b) values (0-255)
    """
    hex_color = hex_color.lstrip('#')
    
    # Handle 3-character hex codes
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """
    Convert RGB to hex color
    
    Args:
        r: Red value (0-255)
        g: Green value (0-255)
        b: Blue value (0-255)
        
    Returns:
        Hex color code (e.g., '#FF0000')
    """
    return f"#{r:02x}{g:02x}{b:02x}".upper()


def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[int, int, int]:
    """
    Convert RGB to HSL
    
    Args:
        r: Red value (0-255)
        g: Green value (0-255)
        b: Blue value (0-255)
        
    Returns:
        Tuple of (h, s, l) where h is 0-360, s and l are 0-100
    """
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return (int(h * 360), int(s * 100), int(l * 100))


def hsl_to_rgb(h: int, s: int, l: int) -> Tuple[int, int, int]:
    """
    Convert HSL to RGB
    
    Args:
        h: Hue (0-360)
        s: Saturation (0-100)
        l: Lightness (0-100)
        
    Returns:
        Tuple of (r, g, b) values (0-255)
    """
    h, s, l = h / 360.0, s / 100.0, l / 100.0
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return (int(r * 255), int(g * 255), int(b * 255))


def count_words(text: str) -> int:
    """
    Count words in text
    
    Args:
        text: Text to count words in
        
    Returns:
        Number of words
    """
    return len(text.split())


def count_characters(text: str, include_spaces: bool = True) -> int:
    """
    Count characters in text
    
    Args:
        text: Text to count characters in
        include_spaces: Whether to include spaces in count
        
    Returns:
        Number of characters
    """
    if include_spaces:
        return len(text)
    return len(text.replace(' ', ''))


def clean_extra_spaces(text: str) -> str:
    """
    Remove extra spaces from text
    
    Args:
        text: Text to clean
        
    Returns:
        Cleaned text
    """
    # Replace multiple spaces with single space
    import re
    text = re.sub(r' +', ' ', text)
    # Remove leading/trailing spaces from each line
    lines = [line.strip() for line in text.split('\n')]
    return '\n'.join(lines)


def reverse_text(text: str) -> str:
    """
    Reverse text
    
    Args:
        text: Text to reverse
        
    Returns:
        Reversed text
    """
    return text[::-1]


def to_uppercase(text: str) -> str:
    """
    Convert text to uppercase
    
    Args:
        text: Text to convert
        
    Returns:
        Uppercase text
    """
    return text.upper()


def to_lowercase(text: str) -> str:
    """
    Convert text to lowercase
    
    Args:
        text: Text to convert
        
    Returns:
        Lowercase text
    """
    return text.lower()


def to_title_case(text: str) -> str:
    """
    Convert text to title case
    
    Args:
        text: Text to convert
        
    Returns:
        Title case text
    """
    return text.title()


def safe_divide(a: float, b: float) -> Optional[float]:
    """
    Safely divide two numbers
    
    Args:
        a: Numerator
        b: Denominator
        
    Returns:
        Result of division, or None if division by zero
    """
    try:
        if b == 0:
            return None
        return a / b
    except Exception:
        return None


def format_number(number: float, decimals: int = 2) -> str:
    """
    Format number with specified decimal places
    
    Args:
        number: Number to format
        decimals: Number of decimal places
        
    Returns:
        Formatted number string
    """
    return f"{number:.{decimals}f}"


def ensure_directory_exists(directory: str) -> bool:
    """
    Ensure a directory exists, creating it if necessary
    
    Args:
        directory: Directory path
        
    Returns:
        True if directory exists or was created, False otherwise
    """
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory: {e}")
        return False


def get_unique_filename(file_path: str) -> str:
    """
    Get a unique filename by adding a number if file exists
    
    Args:
        file_path: Original file path
        
    Returns:
        Unique file path
    """
    if not os.path.exists(file_path):
        return file_path
    
    path = Path(file_path)
    base = path.stem
    ext = path.suffix
    directory = path.parent
    
    counter = 1
    while True:
        new_path = directory / f"{base}_{counter}{ext}"
        if not os.path.exists(new_path):
            return str(new_path)
        counter += 1