# -*- mode: python -*-

import os


# one file installation, nice but application has a slow start as each execution is related to unpacking of ~10MB archive
a = Analysis([os.path.join('mcpartools','generatemc.py')],
             pathex=['.'],
             binaries=[],
             datas=[ ('mcpartools/mcengine/data/*', 'mcpartools/mcengine/data' ), 
                     ('mcpartools/scheduler/data/*', 'mcpartools/scheduler/data' )],
             hiddenimports=['appdirs', 'packaging', 'packaging.version', 'packaging.specifiers', 'packaging.requirements'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=None)


pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='generatemc',
          debug=False,
          strip=False,
          upx=False,
          console=False )
