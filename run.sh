#!/usr/bin/env bash
cd `dirname $0`
cd Python
python pic_code_generator_cli.py
cd ..
bash build.sh -w