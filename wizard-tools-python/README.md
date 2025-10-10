# Wizard Tools

A comprehensive Python tkinter application featuring multiple utility tools with a Whole Foods inspired theme.

## Features

### 🔧 Tools Included

1. **File Chunker** - Split large CSV/Excel files into smaller chunks
   - Support for CSV and Excel (.xlsx, .xls) files
   - Configurable chunk sizes
   - Optional ZIP file creation
   - Progress tracking for large files

2. **File Combiner** - Combine multiple CSV/Excel files
   - Union operation (concatenate rows)
   - Join operation (merge on common column)
   - Support for inner, outer, left, and right joins
   - Automatic column detection

3. **Text Tools** - Transform and analyze text
   - UPPERCASE, lowercase, Title Case conversions
   - Reverse text
   - Character and word counting
   - Clean extra spaces
   - Text statistics

4. **Color Picker** - Visual color picker with conversions
   - Interactive color selection
   - HEX, RGB, and HSL format support
   - Preset color palette
   - Copy to clipboard functionality

5. **Calculator** - Basic arithmetic calculator
   - Addition, subtraction, multiplication, division
   - Calculation history
   - Clean, intuitive interface

### 🎨 Design

- **Whole Foods Theme**: Earth tones and natural greens
- **Draggable Header**: Custom window with draggable title bar
- **Tabbed Interface**: Easy navigation between tools
- **Responsive Design**: Resizable window with minimum dimensions

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone or download this repository

2. Navigate to the project directory:
```bash
cd wizard-tools-python
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

From the project root directory, run:

```bash
python src/main.py
```

Or from the src directory:

```bash
cd src
python main.py
```

### Using the Tools

#### File Chunker
1. Select the "📄 File Chunker" tab
2. Browse and select your input CSV/Excel file
3. Choose an output folder
4. Set the desired chunk size (rows per chunk)
5. Select output format (CSV or Excel)
6. Optionally enable ZIP file creation
7. Click "Split File"

#### File Combiner
1. Select the "🔗 File Combiner" tab
2. Browse and select multiple input files (use semicolon to separate paths)
3. Choose operation type:
   - **Union**: Stacks files vertically (concatenates all rows)
   - **Join**: Merges files based on a common column
4. For Join operations:
   - Specify the join column or use "Detect Columns"
   - Select join type (inner, outer, left, right)
5. Choose output format
6. Click "Combine Files" and select save location

#### Text Tools
1. Select the "📝 Text Tools" tab
2. Enter or paste text in the input area
3. Click any operation button:
   - UPPERCASE, lowercase, Title Case
   - Reverse, Count Characters, Count Words
   - Clean Spaces
4. View results in the output area
5. Use "Copy to Input" to chain operations

#### Color Picker
1. Select the "🎨 Color Picker" tab
2. Click "Pick Color" to open color chooser
3. Or enter values directly:
   - HEX format (e.g., #FF0000)
   - RGB values (0-255 for each)
   - HSL values (H: 0-360, S/L: 0-100)
4. Click "Apply" to update the color
5. Use "Copy" buttons to copy color values
6. Try preset colors for quick selection

#### Calculator
1. Select the "🔢 Calculator" tab
2. Click number buttons to enter values
3. Click operation buttons (+, -, ×, ÷)
4. Click "=" to calculate result
5. View calculation history below
6. Use "C" to clear all, "CE" to clear entry, "←" for backspace

## Project Structure

```
wizard-tools-python/
├── src/
│   ├── main.py              # Application entry point
│   ├── app.py               # Main application class
│   ├── config.py            # Configuration settings
│   ├── tools/               # Tool implementations
│   │   ├── __init__.py
│   │   ├── file_chunker.py
│   │   ├── file_combiner.py
│   │   ├── text_tools.py
│   │   ├── color_picker.py
│   │   └── calculator.py
│   ├── ui/                  # UI components
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── theme.py
│   │   └── widgets.py
│   └── utils/               # Utility functions
│       ├── __init__.py
│       ├── file_processor.py
│       ├── validators.py
│       └── helpers.py
├── assets/                  # Assets directory (icons, images)
├── tests/                   # Test files
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── .gitignore              # Git ignore file
```

## Technical Details

### Dependencies

- **pandas**: Data manipulation and file processing
- **openpyxl**: Excel file support (.xlsx)
- **xlrd**: Legacy Excel file support (.xls)
- **Pillow**: Image processing for color picker
- **ttkthemes**: Enhanced tkinter themes (optional)

### Key Features

- **Threaded Operations**: Long-running file operations run in background threads to prevent UI freezing
- **Progress Tracking**: Visual feedback for lengthy operations
- **Error Handling**: Comprehensive validation and user-friendly error messages
- **Type Hints**: Full type hint support for better code maintainability
- **Modular Design**: Clean separation of concerns with dedicated modules

## Configuration

Edit `src/config.py` to customize:
- Window dimensions
- Color scheme
- Default chunk sizes
- Font settings
- File size limits

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **File Permission Errors**: Ensure you have write permissions for output directories

3. **Large File Processing**: For very large files (>100MB), increase chunk size or available memory

4. **Excel File Errors**: Ensure openpyxl and xlrd are properly installed

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is provided as-is for educational and personal use.

## Credits

- Inspired by the Wizard Tools Tampermonkey script
- Theme inspired by Whole Foods Market's natural aesthetic
- Built with Python and tkinter

## Version History

- **v1.0.0** (2024) - Initial release
  - File Chunker tool
  - File Combiner tool
  - Text Tools
  - Color Picker
  - Calculator
  - Whole Foods theme

## Support

For issues, questions, or suggestions, please open an issue on the project repository.

---

**Wizard Tools** - Making data manipulation and utility tasks simple and beautiful.