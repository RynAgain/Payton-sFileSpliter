"""
File Chunker Tool
Split large CSV/Excel files into smaller chunks
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
from pathlib import Path
import sys

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from config import CHUNK_SIZE_OPTIONS, DEFAULT_CHUNK_SIZE, SUPPORTED_FILE_TYPES, PADDING
from ui.widgets import FileSelector, FolderSelector, ProgressDialog
from utils import (
    FileProcessor,
    validate_data_file,
    validate_folder_writable,
    validate_chunk_size,
    create_zip_file,
    format_file_size
)


class FileChunkerTool(ttk.Frame):
    """Tool for splitting files into chunks"""
    
    def __init__(self, parent: tk.Widget):
        """
        Initialize File Chunker tool
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.processor = FileProcessor()
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the user interface"""
        # Title
        title = ttk.Label(
            self,
            text="File Chunker",
            style="Title.TLabel"
        )
        title.pack(pady=PADDING["medium"])
        
        # Description
        desc = ttk.Label(
            self,
            text="Split large CSV or Excel files into smaller chunks",
            wraplength=600
        )
        desc.pack(pady=PADDING["small"])
        
        # Input file selector
        self.file_selector = FileSelector(
            self,
            "Select Input File:",
            SUPPORTED_FILE_TYPES,
            multiple=False
        )
        self.file_selector.pack(fill=tk.X, padx=PADDING["large"], pady=PADDING["medium"])
        
        # Output folder selector
        self.folder_selector = FolderSelector(
            self,
            "Select Output Folder:"
        )
        self.folder_selector.pack(fill=tk.X, padx=PADDING["large"], pady=PADDING["medium"])
        
        # Options frame
        options_frame = ttk.Frame(self)
        options_frame.pack(fill=tk.X, padx=PADDING["large"], pady=PADDING["medium"])
        
        # Chunk size
        chunk_frame = ttk.Frame(options_frame)
        chunk_frame.pack(fill=tk.X, pady=PADDING["small"])
        
        ttk.Label(chunk_frame, text="Rows per chunk:").pack(side=tk.LEFT, padx=(0, PADDING["small"]))
        
        self.chunk_size_var = tk.IntVar(value=DEFAULT_CHUNK_SIZE)
        chunk_combo = ttk.Combobox(
            chunk_frame,
            textvariable=self.chunk_size_var,
            values=CHUNK_SIZE_OPTIONS,
            width=15,
            state="readonly"
        )
        chunk_combo.pack(side=tk.LEFT)
        
        # Output format
        format_frame = ttk.Frame(options_frame)
        format_frame.pack(fill=tk.X, pady=PADDING["small"])
        
        ttk.Label(format_frame, text="Output format:").pack(side=tk.LEFT, padx=(0, PADDING["small"]))
        
        self.output_format_var = tk.StringVar(value="csv")
        ttk.Radiobutton(
            format_frame,
            text="CSV",
            variable=self.output_format_var,
            value="csv"
        ).pack(side=tk.LEFT, padx=PADDING["small"])
        
        ttk.Radiobutton(
            format_frame,
            text="Excel",
            variable=self.output_format_var,
            value="excel"
        ).pack(side=tk.LEFT, padx=PADDING["small"])
        
        # Create ZIP option
        self.create_zip_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            options_frame,
            text="Create ZIP file of chunks",
            variable=self.create_zip_var
        ).pack(anchor=tk.W, pady=PADDING["small"])
        
        # Buttons frame
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(pady=PADDING["large"])
        
        ttk.Button(
            buttons_frame,
            text="Split File",
            command=self._split_file,
            style="Primary.TButton"
        ).pack(side=tk.LEFT, padx=PADDING["small"])
        
        ttk.Button(
            buttons_frame,
            text="Clear",
            command=self._clear_form
        ).pack(side=tk.LEFT, padx=PADDING["small"])
        
        # Status label
        self.status_var = tk.StringVar(value="")
        self.status_label = ttk.Label(
            self,
            textvariable=self.status_var,
            wraplength=600
        )
        self.status_label.pack(pady=PADDING["small"])
    
    def _validate_inputs(self) -> tuple[bool, str]:
        """
        Validate user inputs
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate input file
        input_file = self.file_selector.get_path()
        valid, msg = validate_data_file(input_file)
        if not valid:
            return False, msg
        
        # Validate output folder
        output_folder = self.folder_selector.get_path()
        if not output_folder:
            return False, "Please select an output folder"
        
        valid, msg = validate_folder_writable(output_folder)
        if not valid:
            return False, msg
        
        # Validate chunk size
        chunk_size = self.chunk_size_var.get()
        valid, msg = validate_chunk_size(chunk_size)
        if not valid:
            return False, msg
        
        return True, ""
    
    def _split_file(self):
        """Split the file into chunks"""
        # Validate inputs
        valid, error_msg = self._validate_inputs()
        if not valid:
            messagebox.showerror("Validation Error", error_msg)
            return
        
        # Get parameters
        input_file = self.file_selector.get_path()
        output_folder = self.folder_selector.get_path()
        chunk_size = self.chunk_size_var.get()
        output_format = self.output_format_var.get()
        create_zip = self.create_zip_var.get()
        
        # Show progress dialog
        progress = ProgressDialog(self, "Splitting File", "Processing file...")
        
        # Process in background thread
        def process():
            try:
                # Split file
                progress.update_status("Splitting file into chunks...")
                success, output_files, error = self.processor.chunk_file(
                    input_file,
                    output_folder,
                    chunk_size,
                    output_format
                )
                
                if not success:
                    self.after(0, lambda: self._show_error(error, progress))
                    return
                
                # Create ZIP if requested
                zip_path = None
                if create_zip and output_files:
                    progress.update_status("Creating ZIP file...")
                    base_name = Path(input_file).stem
                    zip_path = os.path.join(output_folder, f"{base_name}_chunks.zip")
                    create_zip_file(output_files, zip_path)
                
                # Show success message
                self.after(0, lambda: self._show_success(
                    len(output_files),
                    output_folder,
                    zip_path,
                    progress
                ))
            
            except Exception as e:
                self.after(0, lambda: self._show_error(str(e), progress))
        
        thread = threading.Thread(target=process, daemon=True)
        thread.start()
    
    def _show_success(self, num_chunks: int, output_folder: str, zip_path: str, progress: ProgressDialog):
        """Show success message"""
        progress.close()
        
        message = f"Successfully created {num_chunks} chunk(s) in:\n{output_folder}"
        if zip_path:
            message += f"\n\nZIP file created:\n{zip_path}"
        
        self.status_var.set(f"✓ Split complete: {num_chunks} chunks created")
        messagebox.showinfo("Success", message)
    
    def _show_error(self, error: str, progress: ProgressDialog):
        """Show error message"""
        progress.close()
        self.status_var.set("✗ Error occurred")
        messagebox.showerror("Error", f"Failed to split file:\n{error}")
    
    def _clear_form(self):
        """Clear all form inputs"""
        self.file_selector.clear()
        self.folder_selector.clear()
        self.chunk_size_var.set(DEFAULT_CHUNK_SIZE)
        self.output_format_var.set("csv")
        self.create_zip_var.set(True)
        self.status_var.set("")