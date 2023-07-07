import tkinter
import math

class LEDMatrix(tkinter.Canvas):
	def __init__(self, master, radius, row, column, space_ratio = 0.1, click_protect = True):
		self.__radius = radius
		self.__row = row
		self.__column = column
		self.__space_ratio = space_ratio
		space = math.floor(self.__radius * self.__space_ratio)
		self.__canvas_width = (2 * radius + space) * column + space
		self.__canvas_height = (2 * radius + space) * row + space
		super().__init__(master=master, width=self.__canvas_width, height=self.__canvas_height)
		self.__matrix_output = [[0] * self.__column for i in range (self.__row)]
		self.__matrix_x0 = [[0] * self.__column for i in range (self.__row)]
		self.__matrix_x1 = [[0] * self.__column for i in range (self.__row)]
		self.__matrix_y0 = [[0] * self.__column for i in range (self.__row)]
		self.__matrix_y1 = [[0] * self.__column for i in range (self.__row)]
		# bind
		if click_protect == False:
			self.bind("<ButtonRelease-1>", self.onClick)		
		# 円を描画
		x0 = y0 = x1 = y1 = 0
		for i in range (self.__row):
			x0 = x1 = 0
			y0 = space + y1
			y1 = y0 + 2 * radius			
			for j in range (self.__column):
				x0 = space + x1
				x1 = x0 + 2 * radius
				# print(x0, y0, x1, y1)
				# print(len(self.__matrix_x0))
				# print(i, j)
				self.__matrix_x0[i][j] = x0
				self.__matrix_y0[i][j] = y0
				self.__matrix_x1[i][j] = x1
				self.__matrix_y1[i][j] = y1
				s = 'led[' + str(i) + '][' + str(j) + ']' 
				self.create_oval(x0, y0, x1, y1, fill='white', tags=s)
	def output(self, output_matrix):
		if(len(output_matrix) == self.__row and len(output_matrix[0]) == self.__column):
			for i in range(self.__row):
				for j in range(self.__column):
					color = 'white'
					if(output_matrix[i][j] == 1):
						color = 'red'
					s = 'led[' + str(i) + '][' + str(j) + ']'
					# 前回の色から変化があった場合のみ再度塗りつぶしを行う
					if output_matrix[i][j] != self.__matrix_output[i][j]:
						self.itemconfig(s, fill=color)
			self.__matrix_output = output_matrix
			# print(len(self.find_all()))
		else:
			print("matrix error")
	def clear(self):
		mat = [[0] * self.__column for i in range (self.__row)]
		self.output(mat)
	def onClick(self, event):
		for i in range(self.__row):
			for j in range(self.__column):
				if((self.__matrix_x0[i][j] <= event.x <= self.__matrix_x1[i][j]) and (self.__matrix_y0[i][j] <= event.y <= self.__matrix_y1[i][j])):
					# print(i, j)
					if(self.__matrix_output[i][j] == 1):
						self.__matrix_output[i][j] = 0
						s = 'led[' + str(i) + '][' + str(j) + ']' 
						self.itemconfig(s, fill='white')
					else:
						self.__matrix_output[i][j] = 1
						s = 'led[' + str(i) + '][' + str(j) + ']' 
						self.itemconfig(s, fill='red')
	def getCanvasSize(self):
		return self.__canvas_width, self.__canvas_height
	def getMatritxOutput(self):
		return self.__matrix_output

if __name__ == "__main__":
	from font_converter_row_direction import *
	from font_loader import *
	from util import *
	import os
	root = tkinter.Tk()
	root.geometry('800x450')
	s = '  WELCOME TMCIT  '
	mat_8x8 = LEDMatrix(root, radius=6, row=8, column=8, space_ratio=0.4, click_protect=False)
	mat_8xn = LEDMatrix(root, radius=4, row=8, column=getStringLendth(s)*8, space_ratio=0.4)
	loader = FontLoader('./misaki_gothic_2nd.bdf')
	converter = FontConverter_RowDirection(loader.getDictionary())
	converter.convert(s)
	mat_8xn.output(converter.getMatrix_BitInfo())
	mat_8xn.pack()
	viewMat8x8(converter.get8x8Matrix_ByteInfo(0))
	mat_8x8.output(converter.get8x8Matrix_BitInfo(0))
	mat_8x8.pack()
	def generate():
		viewMat8x8_BitInfo(mat_8x8.getMatritxOutput())
		
	button = tkinter.Button(root, text='generate', command= generate)
	button.pack()

	class OnUpdate:
		def __init__(self, max_count):
			self.__max_count = max_count
			self.__count = 0
		def onUpdate(self):
			self.shiftMatrix()
			root.after(100, self.onUpdate)
		def shiftMatrix(self):
			os.system('cls')
			viewMat8x8(converter.get8x8Matrix_ByteInfo(self.__count))
			mat_8x8.output(converter.get8x8Matrix_BitInfo(self.__count))
			self.__count += 1
			self.__count %= self.__max_count

	# テスト用
	test_mode = ''
	# test_mode = 'enable_animation'

	if(test_mode == 'enable_animation'):
		o = OnUpdate(getStringLendth(s)*8 - 8)
		root.after(100, o.onUpdate())
	root.mainloop()