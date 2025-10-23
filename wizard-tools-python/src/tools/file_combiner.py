"""
File Combiner Tool
Combine multiple CSV/Excel files using Union or Join operations
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from pathlib import Path
from typing import List, Tuple
import sys

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from config import SUPPORTED_FILE_TYPES, PADDING, COLORS
from ui.widgets import FileSelector, ProgressDialog, ExcelSheetSelector
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
        self.sheet_selections = {}  # {file_path: sheet_name}
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the user interface"""
        # Create canvas and scrollbar for scrollable content
        canvas = tk.Canvas(self, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Title
        title = ttk.Label(
            self.scrollable_frame,
            text="File Combiner",
            style="Title.TLabel"
        )
        title.pack(pady=PADDING["medium"])
        
        # Description
        desc = ttk.Label(
            self.scrollable_frame,
            text="Combine multiple CSV or Excel files using Union or Join operations",
            wraplength=600
        )
        desc.pack(pady=PADDING["small"])
        
        # Input files selector
        self.file_selector = FileSelector(
            self.scrollable_frame,
            "Select Input Files (multiple files will be combined):",
            SUPPORTED_FILE_TYPES,
            multiple=True,
            on_change=self._update_file_order_display
        )
        self.file_selector.pack(fill=tk.X, padx=PADDING["large"], pady=PADDING["medium"])
        
        # File order info
        self.file_order_var = tk.StringVar(value="")
        file_order_label = ttk.Label(
            self.scrollable_frame,
            textvariable=self.file_order_var,
            wraplength=600,
            font=("Segoe UI", 9, "italic"),
            foreground=COLORS["dark_gray"]
        )
        file_order_label.pack(fill=tk.X, padx=PADDING["large"], pady=(0, PADDING["small"]))
        
        # Excel sheet selection button
        sheet_button_frame = ttk.Frame(self.scrollable_frame)
        sheet_button_frame.pack(fill=tk.X, padx=PADDING["large"], pady=PADDING["small"])
        
        ttk.Button(
            sheet_button_frame,
            text="Select Excel Sheets...",
            command=self._select_excel_sheets
        ).pack(side=tk.LEFT)
        
        self.sheet_status_var = tk.StringVar(value="")
        ttk.Label(
            sheet_button_frame,
            textvariable=self.sheet_status_var,
            font=("Segoe UI", 9, "italic")
        ).pack(side=tk.LEFT, padx=PADDING["medium"])
        
        # Operation type frame
        operation_frame = ttk.LabelFrame(self.scrollable_frame, text="Combine Operation", padding=PADDING["medium"])
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
        
        # Use combobox instead of entry for better UX
        self.join_column_combo = ttk.Combobox(
            join_col_frame,
            textvariable=self.join_column_var,
            width=30,
            state="normal"
        )
        self.join_column_combo.pack(side=tk.LEFT, padx=PADDING["small"])
        
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
        output_frame = ttk.Frame(self.scrollable_frame)
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
        buttons_frame = ttk.Frame(self.scrollable_frame)
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
            self.scrollable_frame,
            textvariable=self.status_var,
            wraplength=600
        )
        self.status_label.pack(pady=PADDING["small"])
    
    def _update_file_order_display(self):
        """Update the file order display"""
        file_paths = self.file_selector.get_paths()
        
        if not file_paths:
            self.file_order_var.set("")
            return
        
        if len(file_paths) == 1:
            self.file_order_var.set(f"📄 Selected: {Path(file_paths[0]).name}")
        else:
            first_file = Path(file_paths[0]).name
            self.file_order_var.set(
                f"📄 {len(file_paths)} files selected. "
                f"For joins: '{first_file}' will be the LEFT table, others will join to it in order."
            )
    
    def _select_excel_sheets(self):
        """Open dialog to select Excel sheets"""
        file_paths = self.file_selector.get_paths()
        
        if not file_paths:
            messagebox.showwarning("No Files", "Please select input files first")
            return
        
        self._update_file_order_display()
        
        # Filter for Excel files only
        excel_files = [f for f in file_paths if f.lower().endswith(('.xlsx', '.xls'))]
        
        if not excel_files:
            messagebox.showinfo("No Excel Files", "No Excel files selected. Sheet selection is only needed for Excel files.")
            return
        
        # Open sheet selector dialog
        dialog = ExcelSheetSelector(self, excel_files, self.processor)
        self.wait_window(dialog)
        
        # Get selections
        selections = dialog.get_selections()
        if selections:
            self.sheet_selections = selections
            count = len(selections)
            self.sheet_status_var.set(f"✓ Sheets selected for {count} Excel file(s)")
        else:
            self.sheet_status_var.set("")
    
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
        
        self._update_file_order_display()
        
        try:
            # Get columns from first file (with sheet selection if applicable)
            sheet_name = self.sheet_selections.get(file_paths[0])
            columns = self.processor.get_column_names(file_paths[0], sheet_name=sheet_name)
            
            if not columns:
                messagebox.showerror("Error", "Could not read columns from first file")
                return
            
            # Find common columns across all files
            common_columns = set(columns)
            for file_path in file_paths[1:]:
                sheet_name = self.sheet_selections.get(file_path)
                file_columns = set(self.processor.get_column_names(file_path, sheet_name=sheet_name))
                common_columns &= file_columns
            
            if not common_columns:
                messagebox.showwarning(
                    "No Common Columns",
                    f"No common columns found across all files.\n\n"
                    f"First file columns: {', '.join(columns[:5])}{'...' if len(columns) > 5 else ''}"
                )
                # Still populate combobox with first file's columns
                self.join_column_combo['values'] = sorted(columns)
                return
            
            # Populate combobox with common columns
            common_list = sorted(common_columns)
            self.join_column_combo['values'] = common_list
            
            # Auto-select first common column
            if common_list:
                self.join_column_var.set(common_list[0])
            
            messagebox.showinfo(
                "Columns Detected",
                f"Found {len(common_list)} common column(s):\n" +
                ", ".join(common_list[:10]) +
                ("..." if len(common_list) > 10 else "")
            )
        
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
                    success, error = self._union_files_with_sheets(file_paths, output_path)
                else:
                    join_column = self.join_column_var.get().strip()
                    join_type = self.join_type_var.get()
                    progress.update_status(f"Combining files with {join_type} join...")
                    success, error = self._join_files_with_sheets(
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
    
    def _union_files_with_sheets(self, file_paths: List[str], output_path: str) -> Tuple[bool, str]:
        """Union files with sheet selection support"""
        try:
            dfs = []
            for file_path in file_paths:
                sheet_name = self.sheet_selections.get(file_path)
                df = self.processor.read_file(file_path, sheet_name=sheet_name)
                dfs.append(df)
            
            # Concatenate all DataFrames
            import pandas as pd
            combined_df = pd.concat(dfs, ignore_index=True)
            
            # Write output file
            success = self.processor.write_file(combined_df, output_path)
            
            if success:
                return True, ""
            else:
                return False, "Failed to write output file"
        except Exception as e:
            return False, str(e)
    
    def _join_files_with_sheets(
        self,
        file_paths: List[str],
        output_path: str,
        join_column: str,
        join_type: str
    ) -> Tuple[bool, str]:
        """Join files with sheet selection support"""
        try:
            import pandas as pd
            import os
            
            # Read first file
            sheet_name = self.sheet_selections.get(file_paths[0])
            result_df = self.processor.read_file(file_paths[0], sheet_name=sheet_name)
            
            # Check if join column exists
            if join_column not in result_df.columns:
                return False, f"Join column '{join_column}' not found in first file"
            
            # Join with remaining files
            for file_path in file_paths[1:]:
                sheet_name = self.sheet_selections.get(file_path)
                df = self.processor.read_file(file_path, sheet_name=sheet_name)
                
                # Check if join column exists
                if join_column not in df.columns:
                    return False, f"Join column '{join_column}' not found in {os.path.basename(file_path)}"
                
                # Perform join
                result_df = result_df.merge(
                    df,
                    on=join_column,
                    how=join_type,
                    suffixes=('', f'_{os.path.basename(file_path)}')
                )
            
            # Write output file
            success = self.processor.write_file(result_df, output_path)
            
            if success:
                return True, ""
            else:
                return False, "Failed to write output file"
        except Exception as e:
            return False, str(e)
    
    def _clear_form(self):
        """Clear all form inputs"""
        self.file_selector.clear()
        self.operation_var.set("union")
        self.join_column_var.set("")
        self.join_type_var.set("inner")
        self.output_format_var.set("csv")
        self.status_var.set("")
        self.sheet_selections = {}
        self.sheet_status_var.set("")
        self._on_operation_change()