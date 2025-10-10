"""
Custom widgets for Wizard Tools application
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional, Callable, List
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from config import COLORS, FONTS, PADDING


class DraggableHeader(ttk.Frame):
    """A draggable header frame for the main window"""
    
    def __init__(self, parent: tk.Widget, title: str, on_close: Callable):
        """
        Initialize draggable header
        
        Args:
            parent: Parent widget
            title: Header title text
            on_close: Callback for close button
        """
        super().__init__(parent, style="Header.TFrame")
        self.parent = parent
        self.on_close = on_close
        
        # Variables for dragging
        self._drag_start_x = 0
        self._drag_start_y = 0
        
        # Title label
        self.title_label = ttk.Label(
            self,
            text=title,
            style="Header.TLabel"
        )
        self.title_label.pack(side=tk.LEFT, padx=PADDING["medium"], pady=PADDING["small"])
        
        # Close button
        self.close_btn = tk.Button(
            self,
            text="✕",
            command=on_close,
            bg=COLORS["primary_green"],
            fg=COLORS["white"],
            font=FONTS["title"],
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2"
        )
        self.close_btn.pack(side=tk.RIGHT, padx=PADDING["small"])
        
        # Minimize button
        self.minimize_btn = tk.Button(
            self,
            text="−",
            command=self._minimize,
            bg=COLORS["primary_green"],
            fg=COLORS["white"],
            font=FONTS["title"],
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2"
        )
        self.minimize_btn.pack(side=tk.RIGHT, padx=PADDING["small"])
        
        # Bind dragging events
        self.bind("<Button-1>", self._start_drag)
        self.bind("<B1-Motion>", self._on_drag)
        self.title_label.bind("<Button-1>", self._start_drag)
        self.title_label.bind("<B1-Motion>", self._on_drag)
    
    def _start_drag(self, event):
        """Start dragging the window"""
        self._drag_start_x = event.x
        self._drag_start_y = event.y
    
    def _on_drag(self, event):
        """Handle window dragging"""
        root = self.winfo_toplevel()
        x = root.winfo_x() + event.x - self._drag_start_x
        y = root.winfo_y() + event.y - self._drag_start_y
        root.geometry(f"+{x}+{y}")
    
    def _minimize(self):
        """Minimize the window"""
        self.winfo_toplevel().iconify()


class FileSelector(ttk.Frame):
    """Widget for selecting files with browse button"""
    
    def __init__(
        self,
        parent: tk.Widget,
        label_text: str,
        file_types: List[tuple],
        multiple: bool = False
    ):
        """
        Initialize file selector
        
        Args:
            parent: Parent widget
            label_text: Label text
            file_types: List of file type tuples for file dialog
            multiple: Whether to allow multiple file selection
        """
        super().__init__(parent)
        self.file_types = file_types
        self.multiple = multiple
        
        # Label
        self.label = ttk.Label(self, text=label_text)
        self.label.grid(row=0, column=0, sticky=tk.W, pady=PADDING["small"])
        
        # Entry
        self.path_var = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.path_var, width=50)
        self.entry.grid(row=1, column=0, sticky=tk.EW, padx=(0, PADDING["small"]))
        
        # Browse button
        self.browse_btn = ttk.Button(
            self,
            text="Browse...",
            command=self._browse
        )
        self.browse_btn.grid(row=1, column=1)
        
        self.columnconfigure(0, weight=1)
    
    def _browse(self):
        """Open file dialog to select file(s)"""
        if self.multiple:
            files = filedialog.askopenfilenames(filetypes=self.file_types)
            if files:
                self.path_var.set(";".join(files))
        else:
            file = filedialog.askopenfilename(filetypes=self.file_types)
            if file:
                self.path_var.set(file)
    
    def get_path(self) -> str:
        """Get the selected file path(s)"""
        return self.path_var.get()
    
    def get_paths(self) -> List[str]:
        """Get list of selected file paths"""
        path_str = self.path_var.get()
        if not path_str:
            return []
        return [p.strip() for p in path_str.split(";") if p.strip()]
    
    def clear(self):
        """Clear the file path"""
        self.path_var.set("")


class FolderSelector(ttk.Frame):
    """Widget for selecting folders with browse button"""
    
    def __init__(self, parent: tk.Widget, label_text: str):
        """
        Initialize folder selector
        
        Args:
            parent: Parent widget
            label_text: Label text
        """
        super().__init__(parent)
        
        # Label
        self.label = ttk.Label(self, text=label_text)
        self.label.grid(row=0, column=0, sticky=tk.W, pady=PADDING["small"])
        
        # Entry
        self.path_var = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.path_var, width=50)
        self.entry.grid(row=1, column=0, sticky=tk.EW, padx=(0, PADDING["small"]))
        
        # Browse button
        self.browse_btn = ttk.Button(
            self,
            text="Browse...",
            command=self._browse
        )
        self.browse_btn.grid(row=1, column=1)
        
        self.columnconfigure(0, weight=1)
    
    def _browse(self):
        """Open folder dialog to select folder"""
        folder = filedialog.askdirectory()
        if folder:
            self.path_var.set(folder)
    
    def get_path(self) -> str:
        """Get the selected folder path"""
        return self.path_var.get()
    
    def clear(self):
        """Clear the folder path"""
        self.path_var.set("")


class ProgressDialog(tk.Toplevel):
    """Dialog showing progress for long operations"""
    
    def __init__(self, parent: tk.Widget, title: str, message: str):
        """
        Initialize progress dialog
        
        Args:
            parent: Parent widget
            title: Dialog title
            message: Progress message
        """
        super().__init__(parent)
        self.title(title)
        self.transient(parent)
        self.grab_set()
        
        # Configure window
        self.configure(bg=COLORS["beige"])
        self.resizable(False, False)
        
        # Center on parent
        self.geometry("400x150")
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 400) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 150) // 2
        self.geometry(f"+{x}+{y}")
        
        # Message label
        self.message_label = ttk.Label(
            self,
            text=message,
            style="Title.TLabel"
        )
        self.message_label.pack(pady=PADDING["large"])
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self,
            mode="indeterminate",
            length=350
        )
        self.progress.pack(pady=PADDING["medium"])
        self.progress.start(10)
        
        # Status label
        self.status_var = tk.StringVar(value="Processing...")
        self.status_label = ttk.Label(
            self,
            textvariable=self.status_var
        )
        self.status_label.pack(pady=PADDING["small"])
    
    def update_status(self, status: str):
        """Update the status message"""
        self.status_var.set(status)
        self.update()
    
    def close(self):
        """Close the progress dialog"""
        self.progress.stop()
        self.destroy()


class ScrolledText(ttk.Frame):
    """Text widget with scrollbar"""
    
    def __init__(
        self,
        parent: tk.Widget,
        width: int = 60,
        height: int = 10,
        wrap: str = tk.WORD
    ):
        """
        Initialize scrolled text widget
        
        Args:
            parent: Parent widget
            width: Text width in characters
            height: Text height in lines
            wrap: Text wrapping mode
        """
        super().__init__(parent)
        
        # Text widget
        self.text = tk.Text(
            self,
            width=width,
            height=height,
            wrap=wrap,
            font=FONTS["normal"],
            bg=COLORS["white"],
            fg=COLORS["black"],
            relief=tk.SOLID,
            borderwidth=1
        )
        self.text.grid(row=0, column=0, sticky=tk.NSEW)
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.text.yview
        )
        self.scrollbar.grid(row=0, column=1, sticky=tk.NS)
        
        self.text.configure(yscrollcommand=self.scrollbar.set)
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
    
    def get_text(self) -> str:
        """Get text content"""
        return self.text.get("1.0", tk.END).strip()
    
    def set_text(self, content: str):
        """Set text content"""
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", content)
    
    def clear(self):
        """Clear text content"""
        self.text.delete("1.0", tk.END)
    
    def append(self, content: str):
        """Append text content"""
        self.text.insert(tk.END, content)