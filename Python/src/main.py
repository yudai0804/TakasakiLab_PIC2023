from font_converter_row_direction import *
from font_loader import *
from util import *
import os
from pic_code_generator import *
import sys
import traceback

try:
    f = FontLoader('../../font/misaki_gothic_2nd.bdf')
    d = f.getDictionary()
    row_converter = FontConverter_RowDirection(d)
    print("型式を選択してください．")
    print("1:末廣，2:齊藤")
    model = int(input("型式:"))
    if model != 1 and model != 2:
        raise Exception("型式が範囲外です．")
    num = int(input("表示したいパターン数を入力してください:"))
    print("好きな文字を入力してください．")
    print("出力したい文字に迷ったら「さんぎこうせんへようこそ」がおすすめです．")
    s = []
    led = []
    for i in range(num):
        tmp = input("出力したい文字" + str(i+1) + ":")
        # 全角に変換
        tmp = convertHalfWordToWord(tmp)
        # 文字の最初と最後に全角スペースを追加
        s.append("　" + tmp + "　")
    print("モードを選択してください．")
    print("1:横にスライド，2:縦にスライド，3:スライドしない")
    mode = int(input("モード:"))
    if mode != 1 and mode != 2 and mode != 3:
        raise Exception("モードが範囲外です．")
    for i in range(num):
        s_len = getStringLendth(s[i])
        led.append(LEDMatrix(mat=row_converter.convert(s[i])))

    hw_info = None
    pic = PICCodeGenerator(hw_info, 8)

    if model == 1:
        hw_info = PICCodeGenerator.getHardwareInformation(is_suehiro=True)
    elif model == 2:
        hw_info = PICCodeGenerator.getHardwareInformation(is_saito=True)
    if mode == 1:
        # row slide
        pic = PICCodeGenerator(hw_info, 8)
        pic.generate(view_str=s, led_matrix=led, is_row_direction_slide=True)
    elif mode == 2:
        # column slide
        # column slideの実装ではなく，no_slideの実装を流用しているので注意
        led_column_slide = []
        pic = PICCodeGenerator(hw_info, 8)
        for i in range(num):
            led[i].verticalReading()
            led_column_slide.append(LEDMatrix(column_size=8, row_size=8))
            for j in range(1, len(led.get()) - 8):
                led_column_slide[i].add(mat=led[i].getSplitedMatrix(row_offset=j), add_row_last=True)
            led_column_slide[i].horizontalReading()
        pic.generate(view_str=s, led_matrix=led_column_slide, is_no_slide=True)
    elif mode == 3:
        # no_slide
        led_no_slide = []
        pic = PICCodeGenerator(hw_info, 1)
        for i in range(num):
            led_no_slide.append(LEDMatrix(mat = led[i].getSplitedMatrix()))
            for j in range(1, len(led[i].get()[0]) // 8):
                led_no_slide[i].add(mat = led[i].getSplitedMatrix(column_offset=8*j), add_column_last=True)
        pic.generate(view_str=s, led_matrix=led_no_slide, is_no_slide=True)

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
