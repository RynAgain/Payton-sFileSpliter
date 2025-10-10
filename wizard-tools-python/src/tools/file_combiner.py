"""
File Combiner Tool
Combine multiple CSV/Excel files using Union or Join operations
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from pathlib import Path
import sys

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from config import SUPPORTED_FILE_TYPES, PADDING
from ui.widgets import FileSelector, ProgressDialog
from utils import FileProcessor, validate_data_file


class FileCombinerTool(ttk.Frame):
    """Tool for combining multiple files"""
    
    def __init__(self, parent: tk.Widget):
        """
        Initialize File Combiner tool
        
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
            text="File Combiner",
            style="Title.TLabel"
        )
        title.pack(pady=PADDING["medium"])
        
        # Description
        desc = ttk.Label(
            self,
            text="Combine multiple CSV or Excel files using Union or Join operations",
            wraplength=600
        )
        desc.pack(pady=PADDING["small"])
        
        # Input files selector
        self.file_selector = FileSelector(
            self,
            "Select Input Files (multiple):",
            SUPPORTED_FILE_TYPES,
            multiple=True
        )
        self.file_selector.pack(fill=tk.X, padx=PADDING["large"], pady=PADDING["medium"])
        
        # Operation type frame
        operation_frame = ttk.LabelFrame(self, text="Combine Operation", padding=PADDING["medium"])
        operation_frame.pack(fill=tk.X, padx=PADDING["large"], pady=PADDING["medium"])
        
        self.operation_var = tk.StringVar(value="union")
        
        # Union option
        union_frame = ttk.Frame(operation_frame)
        union_frame.pack(fill=tk.X, pady=PADDING["small"])
        
        ttk.Radiobutton(
            union_frame,
            text="Union (Concatenate Rows)",
            variable=self.operation_var,
            value="union",
            command=self._on_operation_change
        ).pack(side=tk.LEFT)
        
        ttk.Label(
            union_frame,
            text="- Stacks files vertically, combining all rows",
            font=("Segoe UI", 9, "italic")
        ).pack(side=tk.LEFT, padx=PADDING["medium"])
        
        # Join option
        join_frame = ttk.Frame(operation_frame)
        join_frame.pack(fill=tk.X, pady=PADDING["small"])
        
        ttk.Radiobutton(
            join_frame,
            text="Join (Merge on Column)",
            variable=self.operation_var,
            value="join",
            command=self._on_operation_change
        ).pack(side=tk.LEFT)
        
        ttk.Label(
            join_frame,
            text="- Merges files based on a common column",
            font=("Segoe UI", 9, "italic")
        ).pack(side=tk.LEFT, padx=PADDING["medium"])
        
        # Join options frame (initially hidden)
        self.join_options_frame = ttk.Frame(operation_frame)
        
        # Join column
        join_col_frame = ttk.Frame(self.join_options_frame)
        join_col_frame.pack(fill=tk.X, pady=PADDING["small"])
        
        ttk.Label(join_col_frame, text="Join Column:").pack(side=tk.LEFT, padx=(0, PADDING["small"]))
        
        self.join_column_var = tk.StringVar()
        self.join_column_entry = ttk.Entry(
            join_col_frame,
            textvariable=self.join_column_var,
            width=30
        )
        self.join_column_entry.pack(side=tk.LEFT, padx=PADDING["small"])
        
        ttk.Button(
            join_col_frame,
            text="Detect Columns",
            command=self._detect_columns
        ).pack(side=tk.LEFT)
        
        # Join type
        join_type_frame = ttk.Frame(self.join_options_frame)
        join_type_frame.pack(fill=tk.X, pady=PADDING["small"])
        
        ttk.Label(join_type_frame, text="Join Type:").pack(side=tk.LEFT, padx=(0, PADDING["small"]))
        
        self.join_type_var = tk.StringVar(value="inner")
        join_types = [
            ("Inner Join", "inner"),
            ("Outer Join", "outer"),
            ("Left Join", "left"),
            ("Right Join", "right")
        ]
        
        for text, value in join_types:
            ttk.Radiobutton(
                join_type_frame,
                text=text,
                variable=self.join_type_var,
                value=value
            ).pack(side=tk.LEFT, padx=PADDING["small"])
        
        # Output format
        output_frame = ttk.Frame(self)
        output_frame.pack(fill=tk.X, padx=PADDING["large"], pady=PADDING["medium"])
        
        ttk.Label(output_frame, text="Output format:").pack(side=tk.LEFT, padx=(0, PADDING["small"]))
        
        self.output_format_var = tk.StringVar(value="csv")
        ttk.Radiobutton(
            output_frame,
            text="CSV",
            variable=self.output_format_var,
            value="csv"
        ).pack(side=tk.LEFT, padx=PADDING["small"])
        
        ttk.Radiobutton(
            output_frame,
            text="Excel",
            variable=self.output_format_var,
            value="excel"
        ).pack(side=tk.LEFT, padx=PADDING["small"])
        
        # Buttons frame
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(pady=PADDING["large"])
        
        ttk.Button(
            buttons_frame,
            text="Combine Files",
            command=self._combine_files,
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
    
    def _on_operation_change(self):
        """Handle operation type change"""
        if self.operation_var.get() == "join":
            self.join_options_frame.pack(fill=tk.X, pady=PADDING["medium"])
        else:
            self.join_options_frame.pack_forget()
    
    def _detect_columns(self):
        """Detect common columns from selected files"""
        file_paths = self.file_selector.get_paths()
        
        if not file_paths:
            messagebox.showwarning("No Files", "Please select input files first")
            return
        
        try:
            # Get columns from first file
            columns = self.processor.get_column_names(file_paths[0])
            
            if not columns:
                messagebox.showerror("Error", "Could not read columns from file")
                return
            
            # Find common columns across all files
            common_columns = set(columns)
            for file_path in file_paths[1:]:
                file_columns = set(self.processor.get_column_names(file_path))
                common_columns &= file_columns
            
            if not common_columns:
                messagebox.showwarning(
                    "No Common Columns",
                    "No common columns found across all files"
                )
                return
            
            # Show dialog to select column
            self._show_column_selector(sorted(common_columns))
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to detect columns:\n{str(e)}")
    
    def _show_column_selector(self, columns: list):
        """Show dialog to select join column"""
        dialog = tk.Toplevel(self)
        dialog.title("Select Join Column")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.geometry("300x400")
        dialog.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - 300) // 2
        y = self.winfo_rooty() + (self.winfo_height() - 400) // 2
        dialog.geometry(f"+{x}+{y}")
        
        ttk.Label(
            dialog,
            text="Select a column to join on:",
            style="Title.TLabel"
        ).pack(pady=PADDING["medium"])
        
        # Listbox with scrollbar
        list_frame = ttk.Frame(dialog)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING["medium"], pady=PADDING["small"])
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        for col in columns:
            listbox.insert(tk.END, col)
        
        def on_select():
            selection = listbox.curselection()
            if selection:
                self.join_column_var.set(columns[selection[0]])
                dialog.destroy()
        
        ttk.Button(
            dialog,
            text="Select",
            command=on_select,
            style="Primary.TButton"
        ).pack(pady=PADDING["medium"])
    
    def _validate_inputs(self) -> tuple[bool, str]:
        """
        Validate user inputs
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate input files
        file_paths = self.file_selector.get_paths()
        
        if len(file_paths) < 2:
            return False, "Please select at least 2 files to combine"
        
        for file_path in file_paths:
            valid, msg = validate_data_file(file_path)
            if not valid:
                return False, f"Invalid file: {msg}"
        
        # Validate join-specific inputs
        if self.operation_var.get() == "join":
            join_column = self.join_column_var.get().strip()
            if not join_column:
                return False, "Please specify a join column"
        
        return True, ""
    
    def _combine_files(self):
        """Combine the selected files"""
        # Validate inputs
        valid, error_msg = self._validate_inputs()
        if not valid:
            messagebox.showerror("Validation Error", error_msg)
            return
        
        # Get parameters
        file_paths = self.file_selector.get_paths()
        operation = self.operation_var.get()
        output_format = self.output_format_var.get()
        
        # Get output file path
        from tkinter import filedialog
        ext = ".csv" if output_format == "csv" else ".xlsx"
        output_path = filedialog.asksaveasfilename(
            defaultextension=ext,
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if not output_path:
            return
        
        # Show progress dialog
        progress = ProgressDialog(self, "Combining Files", "Processing files...")
        
        # Process in background thread
        def process():
            try:
                if operation == "union":
                    progress.update_status("Combining files with union...")
                    success, error = self.processor.union_files(file_paths, output_path)
                else:
                    join_column = self.join_column_var.get().strip()
                    join_type = self.join_type_var.get()
                    progress.update_status(f"Combining files with {join_type} join...")
                    success, error = self.processor.join_files(
                        file_paths,
                        output_path,
                        join_column,
                        join_type
                    )
                
                if not success:
                    self.after(0, lambda: self._show_error(error, progress))
                    return
                
                # Show success message
                self.after(0, lambda: self._show_success(output_path, progress))
            
            except Exception as e:
                self.after(0, lambda: self._show_error(str(e), progress))
        
        thread = threading.Thread(target=process, daemon=True)
        thread.start()
    
    def _show_success(self, output_path: str, progress: ProgressDialog):
        """Show success message"""
        progress.close()
        
        message = f"Successfully combined files:\n{output_path}"
        self.status_var.set("✓ Files combined successfully")
        messagebox.showinfo("Success", message)
    
    def _show_error(self, error: str, progress: ProgressDialog):
        """Show error message"""
        progress.close()
        self.status_var.set("✗ Error occurred")
        messagebox.showerror("Error", f"Failed to combine files:\n{error}")
    
    def _clear_form(self):
        """Clear all form inputs"""
        self.file_selector.clear()
        self.operation_var.set("union")
        self.join_column_var.set("")
        self.join_type_var.set("inner")
        self.output_format_var.set("csv")
        self.status_var.set("")
        self._on_operation_change()