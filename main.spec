# -*- mode: python -*-


# add current dir to PYTHONPATH, to enable importing mcpartools package
import sys
DIR = os.path.realpath(".")
sys.path.append(DIR)
import mcpartools
# get version string
version = mcpartools.__version__

# hardcode the version in the __init__ file
with open('mcpartools\__init__.py', "a") as fd:
    fd.write("\n__version__ = \'{:s}\'".format(version))

# one file installation, nice but application has a slow start as each execution is related to unpacking of ~10MB archive
a = Analysis(['mcpartools/generatemc.py'],
             pathex=['.'],
             binaries=[],
             datas=[ ('mcpartools/mcengine/data/*', 'mcengine/data' )],
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
          upx=True,
          console=False )
