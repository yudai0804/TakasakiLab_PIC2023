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
s = '産技高専へようこそ'
s_len = getStringLendth(s)
m = LEDMatrix(mat=row_converter.convert(s))
m_mat = m.getMatrix()
bit = [[0] * 8 for i in range(s_len)]
byte = []
for i in range(s_len):
  bit[i] = m.getSplitedMatrix(column_offset=i*8)
  tmp_byte = convertMat_BitToByte(bit[i])
  
  print(tmp_byte)
  printByteMatrix(tmp_byte)
  byte.append(tmp_byte)
print(byte)
