#!/usr/bin/env bash
set -e
cd `dirname $0`
cd Python/src
UNAME=`uname`
PYTHON=""
case "${UNAME}" in
    Linux*)     PYTHON=python3;;
    CYGWIN*)    PYTHON=python;;
    MINGW*)     PYTHON=python;;
    *)          echo "No support OS" && exit 1;;
esac
${PYTHON} main.py $@
cd ../..
make all
echo "プログラムの書き込みが完了しました"
