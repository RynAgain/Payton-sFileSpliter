"""
Main Window for Wizard Tools application
"""
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import sys

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from config import (
    APP_NAME,
    APP_VERSION,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_MIN_WIDTH,
    WINDOW_MIN_HEIGHT,
    PADDING
)
from ui.theme import WholeFoodsTheme
from ui.widgets import DraggableHeader
from tools import (
    FileChunkerTool,
    FileCombinerTool,
    TextToolsTool,
    ColorPickerTool
)


class MainWindow:
    """Main application window"""
    
    def __init__(self, root: tk.Tk):
        """
        Initialize main window
        
        Args:
            root: Root Tk window
        """
        self.root = root
        self.theme = WholeFoodsTheme()
        self._setup_window()
        self._create_ui()
    
    def _setup_window(self):
        """Setup window properties"""
        # Set title
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        
        # Set size and position
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - WINDOW_WIDTH) // 2
        y = (screen_height - WINDOW_HEIGHT) // 2
        
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
        self.root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        
        # Remove default window decorations for custom header
        self.root.overrideredirect(True)
        
        # Apply theme
        self.theme.apply_theme(self.root)
        
        # Make window resizable with custom border
        self._add_resize_grip()
    
    def _add_resize_grip(self):
        """Add resize grip to window"""
        # This is a simplified version - full implementation would handle all edges
        def start_resize(event):
            self.root.x = event.x
            self.root.y = event.y
        
        def do_resize(event):
            width = self.root.winfo_width() + (event.x - self.root.x)
            height = self.root.winfo_height() + (event.y - self.root.y)
            
            if width >= WINDOW_MIN_WIDTH and height >= WINDOW_MIN_HEIGHT:
                self.root.geometry(f"{width}x{height}")
    
    def _create_ui(self):
        """Create the user interface"""
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Draggable header
        header = DraggableHeader(
            main_container,
            f"{APP_NAME} v{APP_VERSION}",
            self._on_close
        )
        header.pack(fill=tk.X)
        
        # Content area
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Add tool tabs
        self._add_tool_tabs()
        
        # Footer
        footer = ttk.Frame(main_container)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        
        footer_label = ttk.Label(
            footer,
            text=f"© 2024 {APP_NAME} | Whole Foods Theme",
            font=("Segoe UI", 8),
            anchor=tk.CENTER
        )
        footer_label.pack(pady=PADDING["small"])
    
    def _add_tool_tabs(self):
        """Add all tool tabs to the notebook"""
        # File Chunker
        file_chunker_frame = ttk.Frame(self.notebook)
        self.notebook.add(file_chunker_frame, text="📄 File Chunker")
        file_chunker = FileChunkerTool(file_chunker_frame)
        file_chunker.pack(fill=tk.BOTH, expand=True)
        
        # File Combiner
        file_combiner_frame = ttk.Frame(self.notebook)
        self.notebook.add(file_combiner_frame, text="🔗 File Combiner")
        file_combiner = FileCombinerTool(file_combiner_frame)
        file_combiner.pack(fill=tk.BOTH, expand=True)
        
        # Text Tools
        text_tools_frame = ttk.Frame(self.notebook)
        self.notebook.add(text_tools_frame, text="📝 Text Tools")
        text_tools = TextToolsTool(text_tools_frame)
        text_tools.pack(fill=tk.BOTH, expand=True)
        
        # Color Picker
        color_picker_frame = ttk.Frame(self.notebook)
        self.notebook.add(color_picker_frame, text="🎨 Color Picker")
        color_picker = ColorPickerTool(color_picker_frame)
        color_picker.pack(fill=tk.BOTH, expand=True)
    
    def _on_close(self):
        """Handle window close"""
        self.root.quit()
        self.root.destroy()