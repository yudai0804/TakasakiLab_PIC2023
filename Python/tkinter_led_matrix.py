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
		self.__matrix = [[0] * self.__column for i in range (self.__row)]
		print(self.__matrix[0])
		# bind
		# self.bind("<Motion>", self.onMotion)
		# self.bind("<ButtonRelease-1>", self.onClick)		
		# 円を描画
		x0 = y0 = x1 = y1 = 0
		for i in range (self.__column):
			y0 = y1 = 0
			x0 = space + x1
			x1 = x0 + 2 * radius			
			for j in range (self.__row):
				tag = 'led[' + str(i) + '][' + str(j) + ']'
				y0 = space + y1
				y1 = y0 + 2 * radius
				# print(x0, y0, x1, y1)
				self.create_oval(x0, y0, x1, y1, tags=tag)

	def onMotion(self, event):
		print('x=' + str(event.x) + 'y = ' + str(event.y))
	def onClick(self, event):
		print('onClick')
		print('x=' + str(event.x) + 'y = ' + str(event.y))
	def getCanvasSize(self):
		return self.__canvas_width, self.__canvas_height
#ラベルの表示
if __name__ == "__main__":
	root = tkinter.Tk()
	root.geometry('800x450')
	mat = LEDMatrix(root, radius=16, row=10, column=8, space_ratio=0.4)
	mat.pack()
	print(mat.getCanvasSize())
	root.mainloop()