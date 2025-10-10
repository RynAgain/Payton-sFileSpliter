"""
Color Picker Tool
Visual color picker with HEX, RGB, and HSL conversions
"""
import tkinter as tk
from tkinter import ttk, colorchooser
from pathlib import Path
import sys

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from config import COLORS, PADDING
from utils import hex_to_rgb, rgb_to_hex, rgb_to_hsl, hsl_to_rgb, validate_color_hex, validate_rgb_values


class ColorPickerTool(ttk.Frame):
    """Tool for picking and converting colors"""
    
    def __init__(self, parent: tk.Widget):
        """
        Initialize Color Picker tool
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.current_color = "#6B8E23"  # Default to secondary green
        self._setup_ui()
        self._update_color_display()
    
    def _setup_ui(self):
        """Setup the user interface"""
        # Title
        title = ttk.Label(
            self,
            text="Color Picker",
            style="Title.TLabel"
        )
        title.pack(pady=PADDING["medium"])
        
        # Description
        desc = ttk.Label(
            self,
            text="Pick colors and convert between HEX, RGB, and HSL formats",
            wraplength=600
        )
        desc.pack(pady=PADDING["small"])
        
        # Color display frame
        display_frame = ttk.LabelFrame(self, text="Current Color", padding=PADDING["large"])
        display_frame.pack(fill=tk.X, padx=PADDING["large"], pady=PADDING["medium"])
        
        # Color preview canvas
        self.color_canvas = tk.Canvas(
            display_frame,
            width=200,
            height=100,
            bg=self.current_color,
            relief=tk.SOLID,
            borderwidth=2
        )
        self.color_canvas.pack(pady=PADDING["medium"])
        
        # Pick color button
        ttk.Button(
            display_frame,
            text="Pick Color",
            command=self._pick_color,
            style="Primary.TButton"
        ).pack(pady=PADDING["small"])
        
        # Color values frame
        values_frame = ttk.LabelFrame(self, text="Color Values", padding=PADDING["medium"])
        values_frame.pack(fill=tk.X, padx=PADDING["large"], pady=PADDING["medium"])
        
        # HEX input
        hex_frame = ttk.Frame(values_frame)
        hex_frame.pack(fill=tk.X, pady=PADDING["small"])
        
        ttk.Label(hex_frame, text="HEX:", width=10).pack(side=tk.LEFT)
        
        self.hex_var = tk.StringVar(value=self.current_color)
        hex_entry = ttk.Entry(hex_frame, textvariable=self.hex_var, width=15)
        hex_entry.pack(side=tk.LEFT, padx=PADDING["small"])
        
        ttk.Button(
            hex_frame,
            text="Apply",
            command=self._apply_hex
        ).pack(side=tk.LEFT, padx=PADDING["small"])
        
        ttk.Button(
            hex_frame,
            text="Copy",
            command=lambda: self._copy_to_clipboard(self.hex_var.get())
        ).pack(side=tk.LEFT)
        
        # RGB inputs
        rgb_frame = ttk.Frame(values_frame)
        rgb_frame.pack(fill=tk.X, pady=PADDING["small"])
        
        ttk.Label(rgb_frame, text="RGB:", width=10).pack(side=tk.LEFT)
        
        self.r_var = tk.IntVar(value=0)
        self.g_var = tk.IntVar(value=0)
        self.b_var = tk.IntVar(value=0)
        
        ttk.Label(rgb_frame, text="R:").pack(side=tk.LEFT, padx=(PADDING["small"], 2))
        ttk.Spinbox(
            rgb_frame,
            from_=0,
            to=255,
            textvariable=self.r_var,
            width=8
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Label(rgb_frame, text="G:").pack(side=tk.LEFT, padx=(PADDING["small"], 2))
        ttk.Spinbox(
            rgb_frame,
            from_=0,
            to=255,
            textvariable=self.g_var,
            width=8
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Label(rgb_frame, text="B:").pack(side=tk.LEFT, padx=(PADDING["small"], 2))
        ttk.Spinbox(
            rgb_frame,
            from_=0,
            to=255,
            textvariable=self.b_var,
            width=8
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            rgb_frame,
            text="Apply",
            command=self._apply_rgb
        ).pack(side=tk.LEFT, padx=PADDING["small"])
        
        ttk.Button(
            rgb_frame,
            text="Copy",
            command=lambda: self._copy_to_clipboard(f"rgb({self.r_var.get()}, {self.g_var.get()}, {self.b_var.get()})")
        ).pack(side=tk.LEFT)
        
        # HSL inputs
        hsl_frame = ttk.Frame(values_frame)
        hsl_frame.pack(fill=tk.X, pady=PADDING["small"])
        
        ttk.Label(hsl_frame, text="HSL:", width=10).pack(side=tk.LEFT)
        
        self.h_var = tk.IntVar(value=0)
        self.s_var = tk.IntVar(value=0)
        self.l_var = tk.IntVar(value=0)
        
        ttk.Label(hsl_frame, text="H:").pack(side=tk.LEFT, padx=(PADDING["small"], 2))
        ttk.Spinbox(
            hsl_frame,
            from_=0,
            to=360,
            textvariable=self.h_var,
            width=8
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Label(hsl_frame, text="S:").pack(side=tk.LEFT, padx=(PADDING["small"], 2))
        ttk.Spinbox(
            hsl_frame,
            from_=0,
            to=100,
            textvariable=self.s_var,
            width=8
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Label(hsl_frame, text="L:").pack(side=tk.LEFT, padx=(PADDING["small"], 2))
        ttk.Spinbox(
            hsl_frame,
            from_=0,
            to=100,
            textvariable=self.l_var,
            width=8
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            hsl_frame,
            text="Apply",
            command=self._apply_hsl
        ).pack(side=tk.LEFT, padx=PADDING["small"])
        
        ttk.Button(
            hsl_frame,
            text="Copy",
            command=lambda: self._copy_to_clipboard(f"hsl({self.h_var.get()}, {self.s_var.get()}%, {self.l_var.get()}%)")
        ).pack(side=tk.LEFT)
        
        # Preset colors frame
        presets_frame = ttk.LabelFrame(self, text="Preset Colors", padding=PADDING["medium"])
        presets_frame.pack(fill=tk.X, padx=PADDING["large"], pady=PADDING["medium"])
        
        # Create preset color buttons
        preset_colors = [
            ("Primary Green", COLORS["primary_green"]),
            ("Secondary Green", COLORS["secondary_green"]),
            ("Accent Green", COLORS["accent_green"]),
            ("Beige", COLORS["beige"]),
            ("Brown", COLORS["brown"]),
            ("Tan", COLORS["tan"]),
            ("Red", "#FF0000"),
            ("Blue", "#0000FF"),
            ("Yellow", "#FFFF00"),
            ("Purple", "#800080"),
            ("Orange", "#FFA500"),
            ("Pink", "#FFC0CB"),
        ]
        
        preset_grid = ttk.Frame(presets_frame)
        preset_grid.pack()
        
        row = 0
        col = 0
        for name, color in preset_colors:
            btn = tk.Button(
                preset_grid,
                text=name,
                bg=color,
                fg="white" if self._is_dark_color(color) else "black",
                width=15,
                command=lambda c=color: self._set_color(c),
                cursor="hand2"
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky=tk.EW)
            
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # Status label
        self.status_var = tk.StringVar(value="")
        self.status_label = ttk.Label(
            self,
            textvariable=self.status_var,
            wraplength=600
        )
        self.status_label.pack(pady=PADDING["small"])
    
    def _is_dark_color(self, hex_color: str) -> bool:
        """Check if color is dark (for text contrast)"""
        try:
            r, g, b = hex_to_rgb(hex_color)
            # Calculate luminance
            luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            return luminance < 0.5
        except:
            return False
    
    def _pick_color(self):
        """Open color picker dialog"""
        color = colorchooser.askcolor(
            color=self.current_color,
            title="Pick a Color"
        )
        
        if color[1]:  # color[1] is the hex value
            self._set_color(color[1])
    
    def _set_color(self, hex_color: str):
        """Set the current color and update all displays"""
        self.current_color = hex_color.upper()
        self._update_color_display()
        self.status_var.set(f"✓ Color set to {self.current_color}")
    
    def _update_color_display(self):
        """Update all color value displays"""
        # Update canvas
        self.color_canvas.configure(bg=self.current_color)
        
        # Update HEX
        self.hex_var.set(self.current_color)
        
        # Update RGB
        r, g, b = hex_to_rgb(self.current_color)
        self.r_var.set(r)
        self.g_var.set(g)
        self.b_var.set(b)
        
        # Update HSL
        h, s, l = rgb_to_hsl(r, g, b)
        self.h_var.set(h)
        self.s_var.set(s)
        self.l_var.set(l)
    
    def _apply_hex(self):
        """Apply HEX color value"""
        hex_value = self.hex_var.get().strip()
        
        valid, msg = validate_color_hex(hex_value)
        if not valid:
            self.status_var.set(f"✗ {msg}")
            return
        
        # Ensure # prefix
        if not hex_value.startswith('#'):
            hex_value = '#' + hex_value
        
        self._set_color(hex_value)
    
    def _apply_rgb(self):
        """Apply RGB color values"""
        r = self.r_var.get()
        g = self.g_var.get()
        b = self.b_var.get()
        
        valid, msg = validate_rgb_values(r, g, b)
        if not valid:
            self.status_var.set(f"✗ {msg}")
            return
        
        hex_color = rgb_to_hex(r, g, b)
        self._set_color(hex_color)
    
    def _apply_hsl(self):
        """Apply HSL color values"""
        h = self.h_var.get()
        s = self.s_var.get()
        l = self.l_var.get()
        
        # Validate ranges
        if not (0 <= h <= 360):
            self.status_var.set("✗ Hue must be between 0 and 360")
            return
        if not (0 <= s <= 100):
            self.status_var.set("✗ Saturation must be between 0 and 100")
            return
        if not (0 <= l <= 100):
            self.status_var.set("✗ Lightness must be between 0 and 100")
            return
        
        r, g, b = hsl_to_rgb(h, s, l)
        hex_color = rgb_to_hex(r, g, b)
        self._set_color(hex_color)
    
    def _copy_to_clipboard(self, text: str):
        """Copy text to clipboard"""
        self.clipboard_clear()
        self.clipboard_append(text)
        self.status_var.set(f"✓ Copied to clipboard: {text}")