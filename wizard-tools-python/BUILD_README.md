# WizardTools - Executable Build

## Executable Location

The standalone executable has been built and is located at:
```
wizard-tools-python/dist/WizardTools.exe
```

## Running the Application

Simply double-click `WizardTools.exe` to run the application. No Python installation is required!

## File Size

The executable is a single-file bundle that includes:
- Python runtime
- All required libraries (pandas, openpyxl, xlrd, tkinter)
- All application code

This makes it portable and easy to distribute.

## Features

The application includes 4 tools:
1. **📄 File Chunker** - Split large CSV/Excel files into smaller chunks
2. **🔗 File Combiner** - Combine multiple files using Union or Join operations
3. **📝 Text Tools** - Transform and analyze text
4. **🎨 Color Picker** - Pick and convert colors

## Distribution

You can distribute the `WizardTools.exe` file to anyone running Windows. They don't need:
- Python installed
- Any dependencies installed
- Any configuration

Just copy the .exe file and run it!

## Rebuilding

To rebuild the executable after making code changes:
```bash
cd wizard-tools-python
pyinstaller WizardTools.spec --clean
```

The new executable will be in the `dist` folder.

## Build Configuration

The build is configured in `WizardTools.spec` with:
- Single-file executable (all dependencies bundled)
- No console window (GUI only)
- All required hidden imports included
- Optimized with UPX compression

## Troubleshooting

If the executable doesn't run:
1. Make sure you're on Windows (this is a Windows executable)
2. Check Windows Defender or antivirus - they sometimes flag PyInstaller executables
3. Try running from command line to see any error messages:
   ```
   cd dist
   WizardTools.exe
   ```

## File Size Optimization

The current build includes matplotlib and PyQt5 for potential future features. To reduce file size, you can:
1. Remove unused imports from the code
2. Update the spec file to exclude unnecessary packages
3. Rebuild with `pyinstaller WizardTools.spec --clean`