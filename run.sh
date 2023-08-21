#!/usr/bin/env bash
set -e
cd `dirname $0`
cd Python
python pic_code_generator_cli.py
cd ..
bash build.sh -w
echo "プログラムの書き込みが完了しました"