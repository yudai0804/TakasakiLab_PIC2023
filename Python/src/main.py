from font_converter_row_direction import *
from font_loader import *
from util import *
import os
from pic_code_generator import *
import sys
import traceback
import argparse

try:
    # コマンドライン引数を処理
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=int, choices=range(1,3), default=0, help="型式を選択してください\n1:末廣，2:齊藤")
    parser.add_argument("--pattern_number", type=int, choices=range(1,6), default=0, help="表示したいパターン数を入力してください")
    parser.add_argument("--mode", type=int, choices=range(1,4), default=0, help="1:横にスライド，2:縦にスライド，3:スライドしない")

    args = parser.parse_args()
    font_loader = FontLoader('../../font/misaki_gothic_2nd.bdf')
    dictionary = font_loader.getDictionary()
    row_converter = FontConverter_RowDirection(dictionary)
    model = 0
    pattern_number = 0
    mode = 0
    led_str = []
    led_matrix = []

# コマンドライン引数から入力された情報を表示する
    print("コマンドライン引数から入力された情報を表示します")
    if args.model:
        model = args.model
        if model == 1:
            print("型式は1:末廣です")
        elif model == 2:
            print("型式は2:斎藤です")
    if args.pattern_number:
        pattern_number = args.pattern_number
        print("表示するパターン数は" + str(pattern_number) + "個です")
    if args.mode:
        mode = args.mode
        if mode == 1:
            print("モードは1:横にスライドです")
        elif mode == 2:
            print("モードは2:縦にスライドです")
        elif mode == 3:
            print("モードは3:スライドしないです")
    print("コマンドライン引数から入力された情報の表示を終了します\n")

# 文字の入力処理
    if model == 0:
        print("型式を選択してください．")
        print("1:末廣，2:齊藤")
        model = int(input("型式:"))
        if model != 1 and model != 2:
            raise Exception("型式が範囲外です．")
    if pattern_number == 0:
        pattern_number = int(input("表示したいパターン数を入力してください:"))
    if mode == 0:
        print("モードを選択してください．")
        print("1:横にスライド，2:縦にスライド，3:スライドしない")
        mode = int(input("モード:"))
        if mode != 1 and mode != 2 and mode != 3:
            raise Exception("モードが範囲外です．")
    print("好きな文字を入力してください．")
    print("出力したい文字に迷ったら「さんぎこうせんへようこそ」がおすすめです．") 
    for i in range(pattern_number):
        tmp = input("出力したい文字" + str(i+1) + ":")
        # 全角に変換
        tmp = convertHalfWordToWord(tmp)
        # 文字の最初と最後に全角スペースを追加
        led_str.append("　" + tmp + "　")

    for i in range(pattern_number):
        s_len = getStringLendth(led_str[i])
        led_matrix.append(LEDMatrix(mat=row_converter.convert(led_str[i])))

    hw_info = None
    pic = PICCodeGenerator(hw_info, 8)

    if model == 1:
        hw_info = PICCodeGenerator.getHardwareInformation(is_suehiro=True)
    elif model == 2:
        hw_info = PICCodeGenerator.getHardwareInformation(is_saito=True)
    if mode == 1:
        # row slide
        pic = PICCodeGenerator(hw_info, 8)
        pic.generate(view_str=led_str, led_matrix=led_matrix, is_row_direction_slide=True)
    elif mode == 2:
        # column slide
        # column slideの実装ではなく，no_slideの実装を流用しているので注意
        led_column_slide = []
        pic = PICCodeGenerator(hw_info, 8)
        for i in range(pattern_number):
            led_matrix[i].verticalReading()
            led_matrix_column_slide.append(LEDMatrix(column_size=8, row_size=8))
            for j in range(1, len(led_matrix.get()) - 8):
                led_column_slide[i].add(mat=led_matrix[i].getSplitedMatrix(row_offset=j), add_row_last=True)
            led_column_slide[i].horizontalReading()
        pic.generate(view_str=led_str, led_matrix=led_column_slide, is_no_slide=True)
    elif mode == 3:
        # no_slide
        led_no_slide = []
        pic = PICCodeGenerator(hw_info, 1)
        for i in range(pattern_number):
            led_no_slide.append(LEDMatrix(mat = led_matrix[i].getSplitedMatrix()))
            for j in range(1, len(led_matrix[i].get()[0]) // 8):
                led_no_slide[i].add(mat = led_matrix[i].getSplitedMatrix(column_offset=8*j), add_column_last=True)
        pic.generate(view_str=led_str, led_matrix=led_no_slide, is_no_slide=True)

    # アセンブラディレクトリにアセンブラのコードを生成
    os.makedirs("../../asm", exist_ok=True)
    with open("../../asm/main.asm", mode="w") as f:
        f.write(pic.getOutput())
    if pic.getOutput() != "":
        print("アセンブラの自動生成が完了しました")
    else:
        raise Exception
except:
    # print("アセンブラの自動生成に失敗しました")
    traceback.print_exc()
    sys.exit(1)
