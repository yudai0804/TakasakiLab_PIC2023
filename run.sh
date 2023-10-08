#!/usr/bin/env bash
set -e
cd `dirname $0`
cd Python/src
python main.py $@
cd ../..
make all
echo "プログラムの書き込みが完了しました"
