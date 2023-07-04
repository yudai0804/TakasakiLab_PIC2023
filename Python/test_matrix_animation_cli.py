import os
import time
from font_converter_row_direction import *
from font_loader import *
from util import *

f = FontLoader('./misaki_gothic_2nd.bdf')
d = f.getDictionary()
row_converter = FontConverter_RowDirection(d)
a = row_converter.convert('  WELCOME TMCIT  ')
# a = row_converter.convert('  産技高専へようこそ  ')
for i in range(10000):
  viewMat8x8(row_converter.get8x8Matrix_LinearArray(i))
  time.sleep(0.1)
  os.system('cls')