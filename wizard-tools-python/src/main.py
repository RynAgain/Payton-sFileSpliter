#!/usr/bin/env python3
"""
Wizard Tools - Main Entry Point
A comprehensive toolkit application with Whole Foods theme
"""
import sys
import tkinter as tk
from pathlib import Path

# Add src directory to path
src_dir = Path(__file__).parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from app import WizardToolsApp


def main():
    """Main entry point for the application"""
    root = tk.Tk()
    app = WizardToolsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()