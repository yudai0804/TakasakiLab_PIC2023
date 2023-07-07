from font_converter_row_direction import *
from font_loader import *
from util import *
from tkinter_led_matrix import *
from font_original_font_writer import *
import os

root = tkinter.Tk()
root.geometry('800x450')
s = '  WELCOME TMCIT'

mat_8x8 = LEDMatrix(root, radius=6, row=8, column=8, space_ratio=0.4, click_protect=False)
mat_8xn = LEDMatrix(root, radius=4, row=8, column=getStringLendth(s)*8, space_ratio=0.4)
loader = FontLoader('./misaki_gothic_2nd.bdf')
converter = FontConverter_RowDirection(loader.getDictionary())
converter.convert(s)
mat_8xn.output(converter.getMatrix_BitInfo())
mat_8xn.pack()
mat_8x8.pack()
def generate():
	viewMatBitInfo(mat_8x8.getMatrixOutput())
	name = input('ファイル名を入力してください:')
	writeOriginalFont(name, mat_8x8.getMatrixOutput())
def clear():
	os.system('cls')
	mat_8x8.clear()

button = tkinter.Button(root, text='generate', command= generate)
button.pack()
clear_button = tkinter.Button(root, text='clear', command=clear)
clear_button.pack()
mode = tkinter.IntVar()
mode.set(0)
radio_button_mode_generator = tkinter.Radiobutton(root, value = 0, variable=mode, text='任意の文字を生成する', command=clear)
radio_button_mode_animator = tkinter.Radiobutton(root, value = 1, variable=mode, text='アニメーションを再生する', command=clear)
radio_button_mode_generator.pack()
radio_button_mode_animator.pack()

class OnUpdate:
	def __init__(self, max_count):
		self.__max_count = max_count
		self.__count = 0
	def onUpdate(self):
		if mode.get() == 1:
			self.shiftMatrix()
		root.after(100, self.onUpdate)
	def shiftMatrix(self):
		os.system('cls')
		split_matrix = splitMatrix_BitInfo_RowDirection(converter.getMatrix_BitInfo(), self.__count)
		viewMatBitInfo(split_matrix)
		mat_8x8.output(split_matrix)
		self.__count += 1
		self.__count %= self.__max_count

o = OnUpdate(getStringLendth(s)*8 - 8)
root.after(100, o.onUpdate())
root.mainloop()