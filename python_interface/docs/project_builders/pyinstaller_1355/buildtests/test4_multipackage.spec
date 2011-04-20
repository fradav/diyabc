# -*- mode: python -*-

print "TESTING MULTIPROCESS FEATURE: file A (onedir pack) depends on file B (onedir pack)."

__testname__ = 'test4_multipackage'
__testdep__ = 'test4_multipackage_B'

a = Analysis([os.path.join(HOMEPATH,'support', '_mountzlib.py'), os.path.join(HOMEPATH,'support', 'useUnicode.py'), __testname__ + '.py'],
             pathex=['.'])
b = Analysis([os.path.join(HOMEPATH,'support', '_mountzlib.py'), os.path.join(HOMEPATH,'support', 'useUnicode.py'), __testdep__ + '.py'],
             pathex=['.'])

MERGE((b, __testdep__, os.path.join(__testdep__, __testdep__ + '.exe')),
      (a, __testname__, os.path.join(__testname__, __testname__ + '.exe')))

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.dependencies,
          exclude_binaries=1,
          name=os.path.join('build', 'pyi.linux2', __testname__, __testname__ + '.exe'),
          debug=False,
          strip=False,
          upx=True,
          console=1 )

coll = COLLECT( exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=True,
        name=os.path.join('dist', __testname__))

pyzB = PYZ(b.pure)
exeB = EXE(pyzB,
          b.scripts,
          b.dependencies,
          exclude_binaries=1,
          name=os.path.join('build', 'pyi.linux2', __testdep__,__testdep__ + '.exe'),
          debug=False,
          strip=False,
          upx=True,
          console=1 )

coll = COLLECT( exeB,
        b.binaries,
        b.zipfiles,
        b.datas,
        strip=False,
        upx=True,
        name=os.path.join('dist', __testdep__))

