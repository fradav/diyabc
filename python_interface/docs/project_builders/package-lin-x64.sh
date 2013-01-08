#!/bin/bash

# script à exécuter sur une machine linux 64bits qui comporte PyQt4, PyQwt5, g++

packageDir="./lastDiyabc"
diyabc_git="../../../"

cd $diyabc_git

make clean
make 

cp $diyabc_git/src-JMC-C++/general $diyabc_git/python_interface/docs/executables/diyabc-comput-linux-x64

cd ./python_interface/docs/project_builders/

./linux_generation.sh ./pyinstaller_1743/pyinstaller.py $packageDir  ../../diyabc.py
zip -r diyabc.zip lastDiyabc



