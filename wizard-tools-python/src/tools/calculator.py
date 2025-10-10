"""
Calculator Tool
Basic arithmetic calculator with display
"""
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import sys

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from config import CALCULATOR_BUTTONS, COLORS, FONTS, PADDING
from utils import safe_divide


class CalculatorTool(ttk.Frame):
    """Tool for basic arithmetic calculations"""
    
    def __init__(self, parent: tk.Widget):
        """
        Initialize Calculator tool
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.current_value = "0"
        self.previous_value = ""
        self.operation = ""
        self.new_number = True
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the user interface"""
        # Title
        title = ttk.Label(
            self,
            text="Calculator",
            style="Title.TLabel"
        )
        title.pack(pady=PADDING["medium"])
        
        # Description
        desc = ttk.Label(
            self,
            text="Perform basic arithmetic calculations",
            wraplength=600
        )
        desc.pack(pady=PADDING["small"])
        
        # Calculator frame
        calc_frame = ttk.Frame(self)
        calc_frame.pack(pady=PADDING["large"])
        
        # Display
        display_frame = tk.Frame(
            calc_frame,
            bg=COLORS["white"],
            relief=tk.SOLID,
            borderwidth=2
        )
        display_frame.pack(fill=tk.X, padx=PADDING["medium"], pady=PADDING["medium"])
        
        self.display_var = tk.StringVar(value="0")
        display = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=("Consolas", 24, "bold"),
            bg=COLORS["white"],
            fg=COLORS["black"],
            anchor=tk.E,
            padx=PADDING["medium"],
            pady=PADDING["medium"]
        )
        display.pack(fill=tk.BOTH)
        
        # Buttons frame
        buttons_frame = ttk.Frame(calc_frame)
        buttons_frame.pack(padx=PADDING["medium"], pady=PADDING["small"])
        
        # Create calculator buttons
        button_layout = [
            ["7", "8", "9", "÷"],
            ["4", "5", "6", "×"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"],
            ["C", "CE", "←", ""],
        ]
        
        for row_idx, row in enumerate(button_layout):
            for col_idx, btn_text in enumerate(row):
                if btn_text:  # Skip empty buttons
                    self._create_button(buttons_frame, btn_text, row_idx, col_idx)
        
        # History display
        history_frame = ttk.LabelFrame(calc_frame, text="History", padding=PADDING["small"])
        history_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING["medium"], pady=PADDING["medium"])
        
        self.history_text = tk.Text(
            history_frame,
            width=40,
            height=8,
            font=FONTS["monospace"],
            bg=COLORS["white"],
            fg=COLORS["black"],
            state=tk.DISABLED
        )
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        # Clear history button
        ttk.Button(
            history_frame,
            text="Clear History",
            command=self._clear_history
        ).pack(pady=PADDING["small"])
    
    def _create_button(self, parent: tk.Widget, text: str, row: int, col: int):
        """Create a calculator button"""
        # Determine button color based on type
        if text in ["÷", "×", "-", "+"]:
            bg_color = COLORS["secondary_green"]
            fg_color = COLORS["white"]
        elif text == "=":
            bg_color = COLORS["primary_green"]
            fg_color = COLORS["white"]
        elif text in ["C", "CE", "←"]:
            bg_color = COLORS["error_red"]
            fg_color = COLORS["white"]
        else:
            bg_color = COLORS["light_gray"]
            fg_color = COLORS["black"]
        
        btn = tk.Button(
            parent,
            text=text,
            font=FONTS["button"],
            bg=bg_color,
            fg=fg_color,
            width=5,
            height=2,
            relief=tk.RAISED,
            borderwidth=2,
            command=lambda: self._on_button_click(text),
            cursor="hand2"
        )
        btn.grid(row=row, column=col, padx=2, pady=2, sticky=tk.NSEW)
        
        # Hover effects
        def on_enter(e):
            btn.config(relief=tk.SUNKEN)
        
        def on_leave(e):
            btn.config(relief=tk.RAISED)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
    def _on_button_click(self, button: str):
        """Handle button click"""
        if button.isdigit() or button == ".":
            self._handle_number(button)
        elif button in ["÷", "×", "-", "+"]:
            self._handle_operation(button)
        elif button == "=":
            self._calculate()
        elif button == "C":
            self._clear()
        elif button == "CE":
            self._clear_entry()
        elif button == "←":
            self._backspace()
    
    def _handle_number(self, digit: str):
        """Handle number button press"""
        if self.new_number:
            if digit == ".":
                self.current_value = "0."
            else:
                self.current_value = digit
            self.new_number = False
        else:
            # Prevent multiple decimal points
            if digit == "." and "." in self.current_value:
                return
            
            if self.current_value == "0" and digit != ".":
                self.current_value = digit
            else:
                self.current_value += digit
        
        self._update_display()
    
    def _handle_operation(self, op: str):
        """Handle operation button press"""
        if self.operation and not self.new_number:
            self._calculate()
        
        self.previous_value = self.current_value
        self.operation = op
        self.new_number = True
    
    def _calculate(self):
        """Perform calculation"""
        if not self.operation or not self.previous_value:
            return
        
        try:
            num1 = float(self.previous_value)
            num2 = float(self.current_value)
            
            if self.operation == "+":
                result = num1 + num2
            elif self.operation == "-":
                result = num1 - num2
            elif self.operation == "×":
                result = num1 * num2
            elif self.operation == "÷":
                result = safe_divide(num1, num2)
                if result is None:
                    self.current_value = "Error: Div by 0"
                    self._update_display()
                    self._add_to_history(f"{num1} ÷ {num2} = Error")
                    self.operation = ""
                    self.new_number = True
                    return
            else:
                return
            
            # Format result
            if result == int(result):
                self.current_value = str(int(result))
            else:
                self.current_value = f"{result:.10f}".rstrip('0').rstrip('.')
            
            # Add to history
            self._add_to_history(f"{num1} {self.operation} {num2} = {self.current_value}")
            
            self._update_display()
            self.operation = ""
            self.new_number = True
        
        except Exception as e:
            self.current_value = "Error"
            self._update_display()
            self.operation = ""
            self.new_number = True
    
    def _clear(self):
        """Clear all"""
        self.current_value = "0"
        self.previous_value = ""
        self.operation = ""
        self.new_number = True
        self._update_display()
    
    def _clear_entry(self):
        """Clear current entry"""
        self.current_value = "0"
        self.new_number = True
        self._update_display()
    
    def _backspace(self):
        """Remove last digit"""
        if not self.new_number and len(self.current_value) > 1:
            self.current_value = self.current_value[:-1]
        else:
            self.current_value = "0"
            self.new_number = True
        
        self._update_display()
    
    def _update_display(self):
        """Update the display"""
        # Limit display length
        display_value = self.current_value
        if len(display_value) > 15:
            display_value = display_value[:15] + "..."
        
        self.display_var.set(display_value)
    
    def _add_to_history(self, entry: str):
        """Add calculation to history"""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, entry + "\n")
        self.history_text.see(tk.END)
        self.history_text.config(state=tk.DISABLED)
    
    def _clear_history(self):
        """Clear calculation history"""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete("1.0", tk.END)
        self.history_text.config(state=tk.DISABLED)