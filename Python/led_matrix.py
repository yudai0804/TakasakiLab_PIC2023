import copy

class LEDMatrix:
	def __init__(self, mat = None, row_size = None, column_size = None):
		"""
		row_sizeとcolumn_sizeで指定した大きさの行列が生成される
		引数のmatrixに値が入っている場合はクラス内部の行列にmatrixの値代入される。
		その場合は、引数のrow_sizeとcolumn_sizeは無視される。
		"""
		self.__mat = []
		if mat != None:
			self.__mat = mat
		elif row_size != None and column_size != None:
			self.__mat = [[0] * column_size for i in range (row_size)]
	
	def setMatrix(self, mat):
		self.__mat = mat
	
	def add(self, mat = None, led_matrix = None, add_row_last = None, add_column_last = None):
		if led_matrix != None:
			mat = led_matrix.get()
		if mat == None:
			print("matrix error")
			return
		if add_row_last != None:
			row_size = len(self.__mat[0])
			if len(mat[0]) > row_size:
				row_size = len(mat[0])
			tmp = [[0] * row_size for i in range(len(self.__mat) + len(mat))]
			for i in range(len(self.__mat)):
				for j in range(len(self.__mat[0])):
					tmp[i][j] = self.__mat[i][j]
			for i in range(len(mat)):
				for j in range(len(mat[0])):
					tmp[i + len(self.__mat)][j] = mat[i][j]
			self.__mat = tmp
		elif add_column_last != None:
			column_size = len(self.__mat)
			if len(mat) > column_size:
				column_size = len(mat)
			tmp = [[0] * (len(self.__mat[0]) + len(mat[0])) for i in range(column_size)]
			for i in range(len(self.__mat)):
				for j in range(len(self.__mat[0])):
					tmp[i][j] = self.__mat[i][j]
			for i in range(len(mat)):
				for j in range(len(mat[0])):
					tmp[i][j + len(self.__mat[0])] = mat[i][j]
			self.__mat = tmp
	
	def rotate90(self):
		new_m = [[0] * len(self.__mat) for i in range(len(self.__mat[0]))]
		for i in range(len(self.__mat)):
			for j in range(len(self.__mat[0])):
				new_m[len(self.__mat[0]) - j - 1][i] = self.__mat[i][j]
		self.__mat = new_m
	
	def rotate180(self):
		new_m = [[0] * len(self.__mat[0]) for i in range(len(self.__mat))]
		for i in range(len(self.__mat)):
			for j in range(len(self.__mat[0])):
				new_m[len(self.__mat) - i - 1][len(self.__mat[0]) - j - 1] = self.__mat[i][j]
		self.__mat = new_m
	
	def rotate270(self):
		new_m = [[0] * len(self.__mat) for i in range(len(self.__mat[0]))]
		for i in range(len(self.__mat)):
			for j in range(len(self.__mat[0])):
				new_m[j][len(self.__mat) - i - 1] = self.__mat[i][j]
		self.__mat = new_m

	def verticalReading(self, char_size = 8):
		"""横読みを縦読みに変換する"""
		# 大きさが利用可能かを確認
		if len(self.__mat) % char_size != 0 or len(self.__mat[0]) % char_size != 0:
			print("verticalReading error")
			return
		tmp = LEDMatrix(mat = self.getSplitedMatrix(row_size=char_size, column_size=char_size))
		for i in range(1, len(self.__mat[0]) // char_size):
			tmp_char = self.getSplitedMatrix(row_size=char_size, column_size=char_size, column_offset=char_size*i)
			tmp.add(tmp_char, add_row_last=True)
		self.__mat = tmp.get()
	
	def horizontalReading(self, char_size = 8):
		"""縦読みを横読みに変換する"""
		# 大きさが利用可能かを確認
		if len(self.__mat) % char_size != 0 or len(self.__mat[0]) % char_size != 0:
			print("verticalReading error")
			return
		tmp = LEDMatrix(mat = self.getSplitedMatrix(row_size=char_size, column_size=char_size))
		for i in range(1, len(self.__mat) // char_size):
			tmp_char = self.getSplitedMatrix(row_size=char_size, column_size=char_size, row_offset=char_size*i)
			tmp.add(tmp_char, add_column_last=True)
		self.__mat = tmp.get()
	
	def split(self, row_size = 8, column_size = 8, row_offset = 0, column_offset = 0):
		"""
		row_sizeとcolumn_sizeには切り抜きたい行列の大きさを指定する
		横移動させたいときはcolumn_offsetを変更する
		縦移動させたいときはrow_offsetを変更する
		"""
		tmp = [[0] * column_size for i in range(row_size)]
		# offset_bitが範囲外の可能性があるので，範囲内にする
		row_offset %= len(self.__mat) - 1
		column_offset %= len(self.__mat[0]) - 1
		for i in range(row_size):
			for j in range(column_size):
				i_index = (row_offset + i) % len(self.__mat)
				j_index = (column_offset + j) % len(self.__mat[0])
				tmp[i][j] = self.__mat[i_index][j_index]
		self.__mat = tmp

	def print(self):
		printBitMatrix(self.get())

	def get(self):
		return self.__mat

	def getAddedMatrix(self, mat = None, led_matrix = None, add_row_last = None, add_column_last = None):
		tmp = copy.deepcopy(self)
		tmp.add(mat = mat, led_matrix=led_matrix, add_row_last=add_row_last, add_column_last=add_column_last)
		return tmp.get()

	def getRotate90(self):
		tmp = copy.deepcopy(self)
		tmp.rotate90()
		return tmp.get()

	def getRotate180(self):
		tmp = copy.deepcopy(self)
		tmp.rotate180()
		return tmp.get()

	def getRotate270(self):
		tmp = copy.deepcopy(self)
		tmp.rotate270()
		return tmp.get()

	def getVerticalReading(self, char_size = 8):
		"""横読みを縦読みに変換する"""
		tmp = copy.deepcopy(self)
		tmp.verticalReading(char_size=char_size)
		return tmp.get()

	def getHorizontalReading(self, char_size = 8):
		"""縦読みを横読みに変換する"""
		tmp = copy.deepcopy(self)
		tmp.horizontalReading(char_size=char_size)
		return tmp.get()

	def getSplitedMatrix(self, row_size = 8, column_size = 8, row_offset = 0, column_offset = 0):
		"""
		row_sizeとcolumn_sizeには切り抜きたい行列の大きさを指定する
		横移動させたいときはcolumn_offsetを変更する
		縦移動させたいときはrow_offsetを変更する
		"""
		tmp = copy.deepcopy(self)
		tmp.split(row_size=row_size, column_size=column_size, row_offset=row_offset, column_offset=column_offset)
		return tmp.get()

def convertMat_BitToByte(mat):
	"""ビットで表された8x8の行列を8バイトに変換する"""
	m = []
	column = 0
	if len(mat) % 8 != 0 and (len(mat[0]) % 8) != 0:
		print('matrix error')
		return
	m = [0] * 8
	for i in range(len(mat)):
		for j in range(len(mat[0])):
			if mat[i][j] == 1:
				m[i] += 1 << (7 - j)
	return m

if __name__ == '__main__':
	import os
	import time
	from util import *
	bit =[[0, 0, 0, 0, 0, 0, 0, 0], 
				[0, 0, 0, 0, 0, 0, 0, 0],
				[1, 0, 0, 0, 0, 1, 0, 0],
				[1, 0, 0, 0, 0, 0, 1, 0],
				[1, 0, 0, 0, 0, 0, 1, 0], 
				[1, 0, 0, 0, 0, 0, 1, 0],
				[1, 0, 1, 0, 0, 0, 0, 0],
				[0, 1, 0, 0, 0, 0, 0, 0]]
	m = LEDMatrix(bit)
	m1 = LEDMatrix(bit)
	m.add(led_matrix=m1, add_column_last=True)
	m.print()
	printBitMatrix(m.getRotate90())
	printBitMatrix(m.getRotate180())
	printBitMatrix(m.getRotate270())
	printBitMatrix(m.getVerticalReading())