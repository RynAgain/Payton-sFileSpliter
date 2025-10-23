"""
Theme management for Wizard Tools application
Implements Whole Foods inspired color scheme
"""
import tkinter as tk
from tkinter import ttk
from typing import Dict
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from config import COLORS, FONTS


class WholeFoodsTheme:
    """Manages the Whole Foods inspired theme for the application"""
    
    def __init__(self):
        """Initialize theme with Whole Foods colors"""
        self.colors = COLORS
        self.fonts = FONTS
    
    def apply_theme(self, root: tk.Tk) -> None:
        """
        Apply the Whole Foods theme to the root window and all widgets
        
        Args:
            root: The root Tk window
        """
        # Configure root window
        root.configure(bg=self.colors["beige"])
        
        # Create and configure ttk style
        style = ttk.Style()
        
        # Configure TFrame
        style.configure(
            "TFrame",
            background=self.colors["beige"]
        )
        
        # Configure Header Frame (draggable header)
        style.configure(
            "Header.TFrame",
            background=self.colors["primary_green"]
        )
        
        # Configure TLabel
        style.configure(
            "TLabel",
            background=self.colors["beige"],
            foreground=self.colors["black"],
            font=self.fonts["normal"]
        )
        
        # Configure Header Label
        style.configure(
            "Header.TLabel",
            background=self.colors["primary_green"],
            foreground=self.colors["white"],
            font=self.fonts["header"]
        )
        
        # Configure Title Label
        style.configure(
            "Title.TLabel",
            background=self.colors["beige"],
            foreground=self.colors["primary_green"],
            font=self.fonts["title"]
        )
        
        # Configure TButton
        style.configure(
            "TButton",
            background=self.colors["button_bg"],
            foreground=self.colors["black"],
            font=self.fonts["button"],
            borderwidth=1,
            relief="raised",
            padding=(10, 5)
        )
        
        style.map(
            "TButton",
            background=[
                ("active", self.colors["button_hover"]),
                ("pressed", self.colors["button_active"]),
                ("disabled", self.colors["button_disabled"])
            ],
            foreground=[
                ("active", self.colors["black"]),
                ("pressed", self.colors["white"]),
                ("disabled", self.colors["dark_gray"])
            ]
        )
        
        # Configure Primary Button (accent style)
        style.configure(
            "Primary.TButton",
            background=self.colors["secondary_green"],
            foreground=self.colors["black"],
            font=self.fonts["button"],
            padding=(15, 8)
        )
        
        style.map(
            "Primary.TButton",
            foreground=[
                ("active", self.colors["black"]),
                ("pressed", self.colors["white"])
            ]
        )
        
        # Configure TEntry
        style.configure(
            "TEntry",
            fieldbackground=self.colors["white"],
            foreground=self.colors["black"],
            borderwidth=2,
            relief="solid"
        )
        
        # Configure TNotebook (tabs)
        style.configure(
            "TNotebook",
            background=self.colors["beige"],
            borderwidth=0
        )
        
        style.configure(
            "TNotebook.Tab",
            background=self.colors["light_gray"],
            foreground=self.colors["dark_gray"],
            padding=(20, 10),
            font=self.fonts["normal"]
        )
        
        style.map(
            "TNotebook.Tab",
            background=[
                ("selected", self.colors["secondary_green"]),
                ("active", self.colors["accent_green"])
            ],
            foreground=[
                ("selected", self.colors["white"]),
                ("active", self.colors["white"])
            ]
        )
        
        # Configure Progressbar
        style.configure(
            "TProgressbar",
            background=self.colors["secondary_green"],
            troughcolor=self.colors["light_gray"],
            borderwidth=1,
            thickness=20
        )
        
        # Configure Combobox
        style.configure(
            "TCombobox",
            fieldbackground=self.colors["white"],
            background=self.colors["white"],
            foreground=self.colors["black"],
            arrowcolor=self.colors["secondary_green"]
        )
        
        # Configure Checkbutton
        style.configure(
            "TCheckbutton",
            background=self.colors["beige"],
            foreground=self.colors["black"],
            font=self.fonts["normal"]
        )
        
        # Configure Radiobutton
        style.configure(
            "TRadiobutton",
            background=self.colors["beige"],
            foreground=self.colors["black"],
            font=self.fonts["normal"]
        )
        
        # Configure Scrollbar
        style.configure(
            "TScrollbar",
            background=self.colors["secondary_green"],
            troughcolor=self.colors["light_gray"],
            borderwidth=1,
            arrowcolor=self.colors["white"]
        )
    
    def get_color(self, color_name: str) -> str:
        """
        Get a color value by name
        
        Args:
            color_name: Name of the color
            
        Returns:
            Hex color code
        """
        return self.colors.get(color_name, self.colors["black"])
    
    def get_font(self, font_name: str) -> tuple:
        """
        Get a font configuration by name
        
        Args:
            font_name: Name of the font
            
        Returns:
            Font tuple (family, size, weight)
        """
        return self.fonts.get(font_name, self.fonts["normal"])
    
    def create_styled_button(
        self,
        parent: tk.Widget,
        text: str,
        command: callable,
        style: str = "TButton"
    ) -> ttk.Button:
        """
        Create a styled button with theme colors
        
        Args:
            parent: Parent widget
            text: Button text
            command: Command to execute on click
            style: Button style name
            
        Returns:
            Configured ttk.Button
        """
        return ttk.Button(
            parent,
            text=text,
            command=command,
            style=style
        )
    
    def create_styled_label(
        self,
        parent: tk.Widget,
        text: str,
        style: str = "TLabel"
    ) -> ttk.Label:
        """
        Create a styled label with theme colors
        
        Args:
            parent: Parent widget
            text: Label text
            style: Label style name
            
        Returns:
            Configured ttk.Label
        """
        return ttk.Label(
            parent,
            text=text,
            style=style
        )
    
    def create_styled_entry(
        self,
        parent: tk.Widget,
        width: int = 30
    ) -> ttk.Entry:
        """
        Create a styled entry with theme colors
        
        Args:
            parent: Parent widget
            width: Entry width
            
        Returns:
            Configured ttk.Entry
        """
        return ttk.Entry(
            parent,
            width=width,
            style="TEntry"
        )