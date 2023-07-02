import tkinter

class Tkinter_Frame_LEDMatrix:
	def __init__(self, frame : tkinter.Frame, canvas : tkinter.Canvas, num : int, circle_size = 10, circle_space = 25) -> None:
		# 変数を初期化
		self.__frame = frame
		self.__canvas = canvas
		self.__num = num
		self.__circle_size = circle_size
		self.__circle_space = circle_space
		self.__matrix_click_status = [[0] * self.__num for i in range(self.__num)]
		self.__matrix_led_status = [[0] * self.__num for i in range(self.__num)]
		# frameにLEDを配置
		#canvasを作成
		self.__canvas.create_oval(10, 10, 100, 100, fill='#ff0000')
	

if __name__ == '__main__':
	
	root = tkinter.Tk()
	root.title('tkinterの使い方')
	root.geometry('500x500')
	root.resizable(False, False)
	frame = tkinter.Frame(root, width=500, height=250, borderwidth=2, relief='solid')
	# frame.propagate(False)
	frame.grid(row=0, column=0)
	canvas = tkinter.Canvas(root, background="#ffffff",width=150, height=150)
	# canvas.pack()
	led_matrix = Tkinter_Frame_LEDMatrix(frame, canvas, 8)
	print("hello")
	root.mainloop()