import tkinter

class LEDMatrix(tkinter.Canvas):
	def __init__(self, master, canvas_width, canvas_height, radius, row, column):
		super().__init__(master=master, width=canvas_width, height=canvas_height)
		self.__radius = radius
		self.__row = row
		self.__column = column
		self.__matrix = [[0] * column for i in range (row)]
		# bind
		self.bind("<Motion>", self.onMotion)
		self.bind("<ButtonRelease-1>", self.onClick)		
		# 円を描画
		width_offset = canvas_width // (column + 1)
		height_offset = canvas_height // (row + 1)
		for i in range (row):
			for j in range (column):
				tag = 'led[' + str(i) + '][' + str(j) + ']'
				x0 = width_offset*(i+1) + radius
				y0 = height_offset*(j+1) + radius
				x1 = width_offset*(i+1) - radius
				y1 = height_offset*(j+1) - radius
				self.create_oval(x0, y0, x1, y1, tags=tag)

	def onMotion(self, event):
		print('x=' + str(event.x) + 'y = ' + str(event.y))
	def onClick(self, event):
		print('onClick')
		print('x=' + str(event.x) + 'y = ' + str(event.y))

#ラベルの表示
if __name__ == "__main__":
	root = tkinter.Tk()
	root.geometry('800x450')
	mat = LEDMatrix(root, 400, 400, 20, 8, 8)
	
	mat.pack()
	root.mainloop()