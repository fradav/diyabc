#!/bin/bash

# script à exécuter sur la machine virtuelle osxqt

packageDir="./lastDiyabc"
diyabc_git="../"

rm -rf $packageDir
cd $diyabc_git

make clean
CCVERSION="" make 

cp ./src-JMC-C++/general ./gui/data/bin/diyabc-comput-mac-i386

cd ./build/

./mac_generation.sh ./pyinstaller_1355/pyinstaller.py ../gui/data/icons/coccicon.icns $packageDir  ../gui/src/diyabc.py
rm -rf $packageDir/*.app


