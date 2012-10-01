#!/bin/bash

packageDir="/c/lastDiyabc"
diyabc_git="/c/DiyabcGit/diyabc"
MinGw_bindir='/c/MinGw/bin/'

rm -rf $packageDir
cd $diyabc_git

git checkout .
git pull --rebase 
$MinGw_bindir/mingw32-make.exe clean
$MinGw_bindir/mingw32-make.exe
cp $MinGw_bindir/*.dll $diyabc_git/python_interface/docs/executables/
cp $diyabc_git/src-JMC-C++/general.exe $diyabc_git/python_interface/docs/executables/diyabc-comput-win-i386
cp $diyabc_git/src-JMC-C++/general.exe $diyabc_git/python_interface/docs/executables/diyabc-comput-win-x64


cd $diyabc_git/python_interface/docs/project_builders/
./windows_generation.sh ./pyinstaller_1355/pyinstaller.py ../icons/coccicon.ico $packageDir ../../diyabc.py


