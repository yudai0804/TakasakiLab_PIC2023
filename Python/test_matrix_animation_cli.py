import os
import time
from font_converter_column_direction import *
from font_loader import *

f = FontLoader('./misaki_gothic_2nd.bdf')
d = f.getDictionary()
column_converter = FontConverter_ColumnDirection(d)
a = column_converter.convert('  WELCOME TMCIT  ')
# a = column_converter.convert('  産技高専へようこそ  ')
for i in range(10000):
  viewMat8x8(column_converter.get8x8Matrix(i))
  time.sleep(0.1)
  os.system('cls')