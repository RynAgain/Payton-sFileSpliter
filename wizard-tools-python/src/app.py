"""
Main application class for Wizard Tools
"""
import tkinter as tk
from pathlib import Path
import sys

# Add src directory to path
src_dir = Path(__file__).parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from ui import MainWindow


class WizardToolsApp:
    """Main application class"""
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the application
        
        Args:
            root: Root Tk window
        """
        self.root = root
        self.main_window = MainWindow(root)
    
    def run(self):
        """Run the application"""
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = WizardToolsApp(root)
    app.run()