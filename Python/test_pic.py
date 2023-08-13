import os
import time
from font_converter_row_direction import *
from font_loader import *
from led_matrix import *
from util import *
from pic_code_generator_delay import *

f = FontLoader('./misaki_gothic_2nd.bdf')
d = f.getDictionary()
row_converter = FontConverter_RowDirection(d)
# a = row_converter.convert('  WELCOME TMCIT')
s = '  産技高専へようこそ！'
s_len = getStringLendth(s)
m = LEDMatrix(mat=row_converter.convert(s))
m_mat = m.get()
bit = [[0] * 8 for i in range((s_len * 8))]
byte = []
# 80*12で最大960バイト、120文字
if len(bit) * len(bit[0]) > 960:
  print("size error")
org_cnt = 0
output = ''
for i in range(len(bit)):
  bit[i] = m.getSplitedMatrix(column_offset=i)
  tmp_byte = convertMat_BitToByte(bit[i])
  # print(tmp_byte)
  printByteMatrix(tmp_byte)
  byte.append(tmp_byte)
for i in range(len(byte)):
  for j in range(8):
    if org_cnt % 80 == 0:
      if org_cnt != 0:
        output = output.rstrip(",")
      output += "\nORG\t" + str(hex((org_cnt // 80) * 128 + 32) + "\nDE\t")
    output += str(hex(byte[org_cnt // 8][org_cnt % 8])) + ","
    org_cnt += 1
if output[-1] == ",":
  output = output.rstrip(",")
print(output)

print(byte)
print(org_cnt)
