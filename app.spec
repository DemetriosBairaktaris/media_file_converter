import os
import sys

block_cipher = None

# noinspection PyUnresolvedReferences
a = Analysis()

# noinspection PyUnresolvedReferences
pyz = PYZ(a.pure, a.zipped_data)

# noinspection PyUnresolvedReferences
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='file_converter' + ('.exe' if sys.platform == 'win32' else ''),
          upx=True,
          console=False)

# noinspection PyUnresolvedReferences
coll = COLLECT(exe,
               a.binaries + [('msvcp100.dll', 'C:\\Windows\\System32\\msvcp100.dll', 'BINARY'),
                   ('msvcr100.dll', 'C:\\Windows\\System32\\msvcr100.dll', 'BINARY')]
               if sys.platform == 'win32' else a.binaries,
               a.zipfiles,
               a.datas,
               upx=True,
               name='PySteamAuth' + ('.exe' if sys.platform == 'win32' else ''))

if sys.platform == 'darwin':
    # noinspection PyUnresolvedReferences
    app = BUNDLE(exe, name='File Converter.app', icon=None, bundle_identifier='com.demetri.bairaktaris.file-converter')
