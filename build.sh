#!/usr/bin/env bash
cd `dirname $0`
CURRENT=$(pwd)
mkdir build -p
cd ./build
ls | grep -v -E 'main.asm' | xargs rm -rf
$(cmd.exe //c taskkill //im notepad.exe)
$(mpasmx.exe ./main.asm) 
echo "hello"
$(cmd.exe //c taskkill //im mpasmx.exe)