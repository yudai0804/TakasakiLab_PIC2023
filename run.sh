#!/usr/bin/env bash
set -e
cd `dirname $0`
cd Python
python pic_code_generator_cli.py
cd ..
make all
echo "プログラムの書き込みが完了しました"