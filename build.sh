#!/usr/bin/env bash
set -e
cd `dirname $0`
make clean
make
if [ $1 = "-w" ]; then
	java -jar "C:\Program Files (x86)\Microchip\MPLABX\v5.00\mplab_platform\mplab_ipe\ipecmd.jar" -TPPK4 -P16F1938 -F"./build/LEDMATRIX.hex" -M -W4.5
else
	:
fi
# 書き込み時に生成されるログファイルを削除
rm -f log.*
rm -f MPLABXLog.xml*