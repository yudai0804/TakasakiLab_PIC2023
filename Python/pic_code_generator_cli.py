from font_converter_row_direction import *
from font_loader import *
from util import *
import os
from pic_code_generator import *

f = FontLoader('./misaki_gothic_2nd.bdf')
d = f.getDictionary()
row_converter = FontConverter_RowDirection(d)
print("型式を選択してください．")
print("1:末廣，2:齊藤")
model = int(input("型式:"))
print("好きな文字を入力してください．")
print("出力したい文字に迷ったら「さんぎこうせんへようこそ」がおすすめです．")
s = input("出力したい文字:")
# 全角に変換
s = convertHalfWordToWord(s)
# 文字の最初と最後に全角スペースを追加
s = "　" + s + "　"
print("モードを選択してください．")
print("1:横にスライド，2:縦にスライド，3:スライドしない")
mode = int(input("モード:"))
s = convertHalfWordToWord(s)
s_len = getStringLendth(s)
led = LEDMatrix(mat=row_converter.convert(s))
hw_info = None
pic = PICCodeGenerator(hw_info, 8)
if model == 1 or model == 2:
  if model == 1:
    hw_info = PICCodeGenerator.getHardwareInformation(is_suehiro=True)
  elif model == 2:
    hw_info = PICCodeGenerator.getHardwareInformation(is_saito=True)

  if mode == 1:
    # row slide
    pic = PICCodeGenerator(hw_info, 8)
    pic.generate(led, is_row_direction_slide=True)
  elif mode == 2:
    # column slide
    # column slideの実装ではなく，no_slideの実装を流用しているので注意
    pic = PICCodeGenerator(hw_info, 8)
    led.verticalReading()
    led_column_slide = LEDMatrix(column_size=8, row_size=8)
    for i in range(1, len(led.get()) - 8):
      led_column_slide.add(mat=led.getSplitedMatrix(row_offset=i), add_row_last=True)
    led_column_slide.horizontalReading()
    pic.generate(led_column_slide, is_no_slide=True)
  elif mode == 3:
    # no_slide
    pic = PICCodeGenerator(hw_info, 1)
    led_no_slide = LEDMatrix(mat = led.getSplitedMatrix())
    for i in range(1, len(led.get()[0]) // 8):
      led_no_slide.add(mat = led.getSplitedMatrix(column_offset=8*i), add_column_last=True)
    pic.generate(led_matrix=led_no_slide, is_no_slide=True)
  else:
    print("モードエラーです")
else:
  print("型式エラーです")
# アセンブラディレクトリにアセンブラのコードを生成
os.makedirs("../asm", exist_ok=True)
with open("../asm/main.asm", mode="w") as f:
  f.write(pic.getOutput())
if pic.getOutput() != "":
  print("アセンブラの自動生成が完了しました")
else:
  print("アセンブラの自動生成に失敗しました")