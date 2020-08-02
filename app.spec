import os
import sys
import json

# because of py3 absolute imports changes PyInstaller is not able to find
# a `go_drive` package in the current folder
sys.path.insert(0, os.path.abspath('.'))

sys.path.append(os.path.dirname(os.path.abspath('../../')))

import src

IS_WINDOWS = bool(sys.platform.startswith('win32'))

src_dir = os.path.dirname(src.__file__)
src_dir = os.path.normpath(src_dir)
print("src_dir=" + src_dir)
spec_dir = os.path.join(src_dir, "spec")
print("spec_dir=" + spec_dir)

options = [('v', None, 'OPTION')]

datas = [


    ('src/gui/icons_svg/*', './icons_svg/'),
    ('src/gui/icons_svg/icon.svg', '.')
]

hidden_imports = [
    "py._code.code",
    "py._builtin"
]

hidden_imports.append("PySide2.QtWebEngineWidgets")

print("hidden_imports = " + json.dumps(hidden_imports, indent=2))

a = Analysis(['src/gui/main.py'],
             binaries=[('/usr/local/bin/ffmpeg', '.')],
             datas=datas,
             hiddenimports=hidden_imports,
             runtime_hooks=None,
             excludes=['FixTk', 'tcl', 'tk', '_tkinter', 'tkinter', 'Tkinter'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False)

pyz = PYZ(a.pure,
          a.zipped_data)

version_info = None

# NOTE: for OSx the 'console' value should always be True.
# For Windows we will ship 2 binaries:
# - one with disabled console (used by normal users),
# - another one with console enabled, to be used by developers for debugging

console_default_value = True
if IS_WINDOWS:
    console_default_value = False

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='file_converter',
          debug=False,
          strip=False,
          upx=False,
          console=console_default_value,
          version="1.0.0")

fileConverter = EXE(pyz,
                   a.scripts,
                   exclude_binaries=True,
                   name='File Converter',
                   debug=False,
                   strip=False,
                   upx=False,
                   console=console_default_value,
                   version=version_info)

console_exe = EXE(pyz,
                  a.scripts,
                  exclude_binaries=True,
                  name='file_converter_console_exe',
                  debug=False,
                  strip=False,
                  upx=False,
                  console=True,
                  version=version_info)

file_converter_console = EXE(pyz,
                          a.scripts,
                          exclude_binaries=True,
                          name='file_converter_console',
                          debug=False,
                          strip=False,
                          upx=False,
                          console=True,
                          version=version_info)

# NOTE: for OSx we only need 2 files, because console is always enabled.
# For Windows each exe file is duplicated, with 'console' enabled/disabled

executables_to_collect = [exe, fileConverter]
if IS_WINDOWS:
    executables_to_collect += [console_exe, file_converter_console]

coll = COLLECT(*executables_to_collect,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='file_converter')

if sys.platform.startswith("darwin"):
    app = BUNDLE(coll,
                 name='File Converter.app',
                 icon='icon.icns',
                 bundle_identifier='com.demetri.bairaktaris.file-converter',
                 info_plist={
                     'LSUIElement': '1',
                     'NSHighResolutionCapable': '1',
                     'BundleIsRelocatable': 0,
                     'CFBundleVersion': "1.0.0",
                     'CFBundleShortVersionString': "1.0.0",
                 })
