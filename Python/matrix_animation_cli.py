import os
import time
import font

f = font.FontLoader('./font/misaki_gothic_2nd.bdf')
d = f.getDictionary()
row_converter = font.FontConverter_RowDirection(d)
a = row_converter.convert('  WELCOME TMCIT  ')
# a = row_converter.convert('  産技高専へようこそ  ')
for i in range(10000):
  font.viewMat8x8(row_converter.get8x8Matrix(i))
  time.sleep(0.1)
  os.system('cls')