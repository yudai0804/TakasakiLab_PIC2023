import tkinter
import math

class LEDMatrix(tkinter.Canvas):
	def __init__(self, master, radius, row, column, space_ratio = 0.1):
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
		# self.bind("<Motion>", self.onMotion)
		# self.bind("<ButtonRelease-1>", self.onClick)		
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
				self.create_oval(x0, y0, x1, y1, fill='white')
	def output(self, output_matrix):
		if(len(output_matrix) == self.__row and len(output_matrix[0]) == self.__column):
			for i in range(self.__row):
				for j in range(self.__column):
					color = 'white'
					self.__matrix_output[i][j] = 0
					if(output_matrix[i][j] == 1):
						color = 'red'
						self.__matrix_output[i][j] = 1
						# print(color, self.__matrix_x0[i][j], self.__matrix_y0[i][j], self.__matrix_x1[i][j], self.__matrix_y1[i][j])
					# print(color)
					self.create_oval(self.__matrix_x0[i][j], self.__matrix_y0[i][j], self.__matrix_x1[i][j], self.__matrix_y1[i][j], fill=color)
		else:
			print("matrix error")
		
	def onMotion(self, event):
		print('x=' + str(event.x) + 'y = ' + str(event.y))
	def onClick(self, event):
		print('onClick')
		print('x=' + str(event.x) + 'y = ' + str(event.y))
	def getCanvasSize(self):
		return self.__canvas_width, self.__canvas_height
#ラベルの表示
if __name__ == "__main__":
	from font_converter_row_direction import *
	from font_loader import *
	from util import *
	import os
	root = tkinter.Tk()
	root.geometry('800x450')
	s = '  WELCOME TMCIT  '
	print(getStringLendth(s))
	mat_8x8 = LEDMatrix(root, radius=12, row=8, column=8, space_ratio=0.4)
	mat_8xn = LEDMatrix(root, radius=4, row=8, column=getStringLendth(s)*8, space_ratio=0.4)
	loader = FontLoader('./misaki_gothic_2nd.bdf')
	converter = FontConverter_RowDirection(loader.getDictionary())
	converter.convert(s)
	print('8xn')
	mat_8xn.output(converter.getMatrix_BitInfo())
	# print(converter.getMatrix_BitInfo())
	mat_8xn.pack()
	print('8x8')
	viewMat8x8(converter.get8x8Matrix_ByteInfo(0))
	mat_8x8.output(converter.get8x8Matrix_BitInfo(0))
	mat_8x8.pack()

	class OnUpdate:
		def __init__(self, max_count):
			self.__max_count = max_count
			self.__count = 0
		def onUpdate(self):
			os.system('cls')
			# viewMat8x8(converter.get8x8Matrix_ByteInfo(self.__count))
			# print(self.__count)
			mat_8x8.output(converter.get8x8Matrix_BitInfo(self.__count))
			self.__count += 1
			self.__count %= self.__max_count
			root.after(100, self.onUpdate)

	o = OnUpdate(getStringLendth(s)*8 - 8)
	root.after(100, o.onUpdate())
	root.mainloop()