from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Collect all submodules from the src directory
hiddenimports = collect_submodules('app')
hiddenimports += collect_submodules('config')
hiddenimports += collect_submodules('tools')
hiddenimports += collect_submodules('ui')
hiddenimports += collect_submodules('utils')

# Collect any data files if needed
datas = collect_data_files('app', include_py_files=True)
datas += collect_data_files('config', include_py_files=True)
datas += collect_data_files('tools', include_py_files=True)
datas += collect_data_files('ui', include_py_files=True)
datas += collect_data_files('utils', include_py_files=True)