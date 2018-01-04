# -*- mode: python -*-

block_cipher = None


##### include mydir in distribution #######
def extra_datas(mydir):
   def rec_glob(p, files):
       import os
       import glob
       for d in glob.glob(p):
           if os.path.isfile(d):
               files.append(d)
           rec_glob("%s/*" % d, files)
   files = []
   rec_glob("%s/*" % mydir, files)
   extra_datas = []
   for f in files:
       extra_datas.append((f, f, 'DATA'))

   return extra_datas


a = Analysis(['cqcad.py'],
             pathex=['/home/jwright/Downloads/repos/cqcad/cqcad'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

# Include directories with dynamically loaded scripts
a.datas += extra_datas('c_collections')
a.datas += extra_datas('components')
a.datas += extra_datas('content')
a.datas += extra_datas('extensions')
a.datas += extra_datas('layouts')
a.datas += extra_datas('templates')

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='cqcad',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='cqcad')
