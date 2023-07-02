import os
import time
import font

f = font.FontLoader('./font/misaki_gothic_2nd.bdf')
d = f.getDictionary()
column_converter = font.FontConverter_ColumnDirection(d)
a = column_converter.convert('  WELCOME TMCIT  ')
# a = column_converter.convert('  産技高専へようこそ  ')
for i in range(10000):
  font.viewMat8x8(column_converter.get8x8Matrix(i))
  time.sleep(0.1)
  os.system('cls')