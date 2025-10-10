"""
Validation utilities for Wizard Tools application
"""
import os
from pathlib import Path
from typing import List, Tuple, Optional
import sys

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from config import MAX_FILE_SIZE_MB


def validate_file_exists(file_path: str) -> Tuple[bool, str]:
    """
    Validate that a file exists
    
    Args:
        file_path: Path to the file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not file_path:
        return False, "No file path provided"
    
    if not os.path.exists(file_path):
        return False, f"File does not exist: {file_path}"
    
    if not os.path.isfile(file_path):
        return False, f"Path is not a file: {file_path}"
    
    return True, ""


def validate_file_size(file_path: str, max_size_mb: int = MAX_FILE_SIZE_MB) -> Tuple[bool, str]:
    """
    Validate that a file is not too large
    
    Args:
        file_path: Path to the file
        max_size_mb: Maximum file size in MB
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if size_mb > max_size_mb:
            return False, f"File is too large ({size_mb:.1f}MB). Maximum size is {max_size_mb}MB"
        return True, ""
    except Exception as e:
        return False, f"Error checking file size: {str(e)}"


def validate_file_extension(file_path: str, allowed_extensions: List[str]) -> Tuple[bool, str]:
    """
    Validate that a file has an allowed extension
    
    Args:
        file_path: Path to the file
        allowed_extensions: List of allowed extensions (e.g., ['.csv', '.xlsx'])
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    ext = Path(file_path).suffix.lower()
    if ext not in allowed_extensions:
        return False, f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
    return True, ""


def validate_csv_file(file_path: str) -> Tuple[bool, str]:
    """
    Validate a CSV file
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check file exists
    valid, msg = validate_file_exists(file_path)
    if not valid:
        return valid, msg
    
    # Check file size
    valid, msg = validate_file_size(file_path)
    if not valid:
        return valid, msg
    
    # Check extension
    valid, msg = validate_file_extension(file_path, ['.csv'])
    if not valid:
        return valid, msg
    
    return True, ""


def validate_excel_file(file_path: str) -> Tuple[bool, str]:
    """
    Validate an Excel file
    
    Args:
        file_path: Path to the Excel file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check file exists
    valid, msg = validate_file_exists(file_path)
    if not valid:
        return valid, msg
    
    # Check file size
    valid, msg = validate_file_size(file_path)
    if not valid:
        return valid, msg
    
    # Check extension
    valid, msg = validate_file_extension(file_path, ['.xlsx', '.xls'])
    if not valid:
        return valid, msg
    
    return True, ""


def validate_data_file(file_path: str) -> Tuple[bool, str]:
    """
    Validate a data file (CSV or Excel)
    
    Args:
        file_path: Path to the data file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check file exists
    valid, msg = validate_file_exists(file_path)
    if not valid:
        return valid, msg
    
    # Check file size
    valid, msg = validate_file_size(file_path)
    if not valid:
        return valid, msg
    
    # Check extension
    valid, msg = validate_file_extension(file_path, ['.csv', '.xlsx', '.xls'])
    if not valid:
        return valid, msg
    
    return True, ""


def validate_folder_exists(folder_path: str) -> Tuple[bool, str]:
    """
    Validate that a folder exists
    
    Args:
        folder_path: Path to the folder
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not folder_path:
        return False, "No folder path provided"
    
    if not os.path.exists(folder_path):
        return False, f"Folder does not exist: {folder_path}"
    
    if not os.path.isdir(folder_path):
        return False, f"Path is not a folder: {folder_path}"
    
    return True, ""


def validate_folder_writable(folder_path: str) -> Tuple[bool, str]:
    """
    Validate that a folder is writable
    
    Args:
        folder_path: Path to the folder
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    valid, msg = validate_folder_exists(folder_path)
    if not valid:
        return valid, msg
    
    if not os.access(folder_path, os.W_OK):
        return False, f"Folder is not writable: {folder_path}"
    
    return True, ""


def validate_chunk_size(chunk_size: int) -> Tuple[bool, str]:
    """
    Validate chunk size for file splitting
    
    Args:
        chunk_size: Number of rows per chunk
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if chunk_size <= 0:
        return False, "Chunk size must be greater than 0"
    
    if chunk_size > 1000000:
        return False, "Chunk size is too large (max 1,000,000 rows)"
    
    return True, ""


def validate_color_hex(hex_color: str) -> Tuple[bool, str]:
    """
    Validate a hex color code
    
    Args:
        hex_color: Hex color code (e.g., '#FF0000')
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not hex_color:
        return False, "No color provided"
    
    # Remove # if present
    hex_color = hex_color.lstrip('#')
    
    # Check length
    if len(hex_color) not in [3, 6]:
        return False, "Hex color must be 3 or 6 characters"
    
    # Check if all characters are valid hex
    try:
        int(hex_color, 16)
        return True, ""
    except ValueError:
        return False, "Invalid hex color code"


def validate_rgb_values(r: int, g: int, b: int) -> Tuple[bool, str]:
    """
    Validate RGB color values
    
    Args:
        r: Red value (0-255)
        g: Green value (0-255)
        b: Blue value (0-255)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    for value, name in [(r, 'Red'), (g, 'Green'), (b, 'Blue')]:
        if not isinstance(value, int):
            return False, f"{name} value must be an integer"
        if value < 0 or value > 255:
            return False, f"{name} value must be between 0 and 255"
    
    return True, ""


def validate_number(value: str) -> Tuple[bool, str]:
    """
    Validate that a string is a valid number
    
    Args:
        value: String to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value:
        return False, "No value provided"
    
    try:
        float(value)
        return True, ""
    except ValueError:
        return False, f"Invalid number: {value}"