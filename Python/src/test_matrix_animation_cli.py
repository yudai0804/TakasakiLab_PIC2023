import os
import time
from font_converter_row_direction import *
from font_loader import *
from led_matrix import *
from util import *

f = FontLoader('../../font/misaki_gothic_2nd.bdf')
d = f.getDictionary()
row_converter = FontConverter_RowDirection(d)
# a = row_converter.convert('  WELCOME TMCIT')
m = LEDMatrix(mat=row_converter.convert('  産技高専へようこそ'))
for i in range(10000):
    printBitMatrix(m.getSplitedMatrix(column_offset=i))
    time.sleep(0.1)
    # windowsの場合
    os.system('cls')
    # linuxの場合
    # os.system('clear')

