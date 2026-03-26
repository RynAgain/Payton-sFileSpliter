# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=['src'],
    binaries=[],
    datas=[
        ('src/app.py', '.'),
        ('src/config.py', '.'),
        ('src/tools/*.py', 'tools'),
        ('src/ui/*.py', 'ui'),
        ('src/utils/*.py', 'utils'),
    ],
    hiddenimports=[
        'pandas',
        'openpyxl',
        'xlrd',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.colorchooser',
        'app',
        'config',
        'tools',
        'tools.file_chunker',
        'tools.file_combiner',
        'tools.text_tools',
        'tools.color_picker',
        'tools.calculator',
        'ui',
        'ui.main_window',
        'ui.theme',
        'ui.widgets',
        'utils',
        'utils.file_processor',
        'utils.helpers',
        'utils.validators',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='WizardTools',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False to hide console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one
)