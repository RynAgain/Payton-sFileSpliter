"""
Text Tools
Transform and analyze text with various operations
"""
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import sys

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from config import TEXT_OPERATIONS, PADDING
from ui.widgets import ScrolledText
from utils import (
    to_uppercase,
    to_lowercase,
    to_title_case,
    reverse_text,
    count_characters,
    count_words,
    clean_extra_spaces
)


class TextToolsTool(ttk.Frame):
    """Tool for text transformation and analysis"""
    
    def __init__(self, parent: tk.Widget):
        """
        Initialize Text Tools
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the user interface"""
        # Title
        title = ttk.Label(
            self,
            text="Text Tools",
            style="Title.TLabel"
        )
        title.pack(pady=PADDING["medium"])
        
        # Description
        desc = ttk.Label(
            self,
            text="Transform and analyze text with various operations",
            wraplength=600
        )
        desc.pack(pady=PADDING["small"])
        
        # Main content frame
        content_frame = ttk.Frame(self)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING["large"], pady=PADDING["medium"])
        
        # Input text area
        input_frame = ttk.LabelFrame(content_frame, text="Input Text", padding=PADDING["medium"])
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, PADDING["medium"]))
        
        self.input_text = ScrolledText(input_frame, width=70, height=8)
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # Operations frame
        operations_frame = ttk.Frame(content_frame)
        operations_frame.pack(fill=tk.X, pady=PADDING["medium"])
        
        # Operation buttons in a grid
        ttk.Label(operations_frame, text="Select Operation:").pack(anchor=tk.W, pady=(0, PADDING["small"]))
        
        buttons_frame = ttk.Frame(operations_frame)
        buttons_frame.pack(fill=tk.X)
        
        # Create buttons for each operation
        operations = [
            ("UPPERCASE", self._to_uppercase),
            ("lowercase", self._to_lowercase),
            ("Title Case", self._to_title_case),
            ("Reverse", self._reverse_text),
            ("Count Characters", self._count_characters),
            ("Count Words", self._count_words),
            ("Clean Spaces", self._clean_spaces),
        ]
        
        row = 0
        col = 0
        for text, command in operations:
            btn = ttk.Button(
                buttons_frame,
                text=text,
                command=command,
                width=18
            )
            btn.grid(row=row, column=col, padx=PADDING["small"], pady=PADDING["small"], sticky=tk.EW)
            
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        # Configure grid columns to expand evenly
        for i in range(3):
            buttons_frame.columnconfigure(i, weight=1)
        
        # Output text area
        output_frame = ttk.LabelFrame(content_frame, text="Output / Result", padding=PADDING["medium"])
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(PADDING["medium"], 0))
        
        self.output_text = ScrolledText(output_frame, width=70, height=8)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Action buttons
        action_frame = ttk.Frame(content_frame)
        action_frame.pack(pady=PADDING["medium"])
        
        ttk.Button(
            action_frame,
            text="Copy to Input",
            command=self._copy_to_input
        ).pack(side=tk.LEFT, padx=PADDING["small"])
        
        ttk.Button(
            action_frame,
            text="Clear All",
            command=self._clear_all
        ).pack(side=tk.LEFT, padx=PADDING["small"])
        
        # Status label
        self.status_var = tk.StringVar(value="")
        self.status_label = ttk.Label(
            content_frame,
            textvariable=self.status_var,
            wraplength=600
        )
        self.status_label.pack(pady=PADDING["small"])
    
    def _get_input_text(self) -> str:
        """Get text from input area"""
        return self.input_text.get_text()
    
    def _set_output_text(self, text: str):
        """Set text in output area"""
        self.output_text.set_text(text)
    
    def _to_uppercase(self):
        """Convert text to uppercase"""
        input_text = self._get_input_text()
        if not input_text:
            self.status_var.set("⚠ No input text")
            return
        
        result = to_uppercase(input_text)
        self._set_output_text(result)
        self.status_var.set("✓ Converted to UPPERCASE")
    
    def _to_lowercase(self):
        """Convert text to lowercase"""
        input_text = self._get_input_text()
        if not input_text:
            self.status_var.set("⚠ No input text")
            return
        
        result = to_lowercase(input_text)
        self._set_output_text(result)
        self.status_var.set("✓ Converted to lowercase")
    
    def _to_title_case(self):
        """Convert text to title case"""
        input_text = self._get_input_text()
        if not input_text:
            self.status_var.set("⚠ No input text")
            return
        
        result = to_title_case(input_text)
        self._set_output_text(result)
        self.status_var.set("✓ Converted to Title Case")
    
    def _reverse_text(self):
        """Reverse the text"""
        input_text = self._get_input_text()
        if not input_text:
            self.status_var.set("⚠ No input text")
            return
        
        result = reverse_text(input_text)
        self._set_output_text(result)
        self.status_var.set("✓ Text reversed")
    
    def _count_characters(self):
        """Count characters in text"""
        input_text = self._get_input_text()
        if not input_text:
            self.status_var.set("⚠ No input text")
            return
        
        with_spaces = count_characters(input_text, include_spaces=True)
        without_spaces = count_characters(input_text, include_spaces=False)
        
        result = f"Character Count:\n\n"
        result += f"With spaces: {with_spaces:,}\n"
        result += f"Without spaces: {without_spaces:,}\n"
        result += f"Spaces: {with_spaces - without_spaces:,}"
        
        self._set_output_text(result)
        self.status_var.set("✓ Characters counted")
    
    def _count_words(self):
        """Count words in text"""
        input_text = self._get_input_text()
        if not input_text:
            self.status_var.set("⚠ No input text")
            return
        
        word_count = count_words(input_text)
        char_count = count_characters(input_text, include_spaces=True)
        lines = input_text.split('\n')
        line_count = len(lines)
        
        result = f"Text Statistics:\n\n"
        result += f"Words: {word_count:,}\n"
        result += f"Characters: {char_count:,}\n"
        result += f"Lines: {line_count:,}\n"
        
        if word_count > 0:
            avg_word_length = (char_count - input_text.count(' ')) / word_count
            result += f"Average word length: {avg_word_length:.1f} characters"
        
        self._set_output_text(result)
        self.status_var.set("✓ Words counted")
    
    def _clean_spaces(self):
        """Clean extra spaces from text"""
        input_text = self._get_input_text()
        if not input_text:
            self.status_var.set("⚠ No input text")
            return
        
        result = clean_extra_spaces(input_text)
        self._set_output_text(result)
        self.status_var.set("✓ Extra spaces cleaned")
    
    def _copy_to_input(self):
        """Copy output text to input"""
        output_text = self.output_text.get_text()
        if not output_text:
            self.status_var.set("⚠ No output text to copy")
            return
        
        self.input_text.set_text(output_text)
        self.status_var.set("✓ Output copied to input")
    
    def _clear_all(self):
        """Clear all text areas"""
        self.input_text.clear()
        self.output_text.clear()
        self.status_var.set("✓ All cleared")