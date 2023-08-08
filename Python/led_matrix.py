class LEDMatrix:
	def __init__(self, row_size = None, column_size = None, mat = None):
		"""
		row_sizeとcolumn_sizeで指定した大きさの行列が生成される
		引数のmatrixに値が入っている場合はクラス内部の行列にmatrixの値代入される。
		その場合は、引数のrow_sizeとcolumn_sizeは無視される。
		"""
		self.__mat = []
		if mat != None:
			self.__mat = mat
		elif row_size != None and column_size != None:
			self.__mat = [[0] * 8 for i in range (row_size)]
	def setMatrix(self, mat):
		self.__mat = mat
	def add(self):
		# TODO add関数実装する
		print("")
	def rotate90(self):
		new_m = [[0] * len(self.__mat) for i in range(len(self.__mat[0]))]
		for i in range(len(self.__mat)):
			for j in range(len(self.__mat[0])):
				new_m[len(self.__mat[0]) - j - 1][i] = self.__mat[i][j]
		self.__mat = new_m
		return self.__mat
	def rotate180(self):
		new_m = [[0] * len(self.__mat[0]) for i in range(len(self.__mat))]
		for i in range(len(self.__mat)):
			for j in range(len(self.__mat[0])):
				new_m[len(self.__mat) - i - 1][len(self.__mat[0]) - j - 1] = self.__mat[i][j]
		self.__mat = new_m
		return self.__mat
	def rotate270(self):
		new_m = [[0] * len(self.__mat) for i in range(len(self.__mat[0]))]
		for i in range(len(self.__mat)):
			for j in range(len(self.__mat[0])):
				new_m[j][len(self.__mat) - i - 1] = self.__mat[i][j]
		self.__mat = new_m
		return self.__mat
	def getSplitedMatrix(self, row_size = 8, column_size = 8, row_offset = 0, column_offset = 0):
		"""
		row_sizeとcolumn_sizeには切り抜きたい行列の大きさを指定する
		横移動させたいときはcolumn_offsetを変更する
		縦移動させたいときはrow_offsetを変更する
		"""
		m = [[0] * column_size for i in range(row_size)]
		# offset_bitが範囲外の可能性があるので，範囲内にする
		row_offset %= len(self.__mat) - 1
		column_offset %= len(self.__mat[0]) - 1
		for i in range(row_size):
			for j in range(column_size):
				i_index = (row_offset + i) % len(self.__mat)
				j_index = (column_offset + j) % len(self.__mat[0])
				m[i][j] = self.__mat[i_index][j_index]
		return m
	def getMatrix(self):
		return self.__mat

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
	m = [LEDMatrix(8, 8)] * 4
	bit =[[0, 0, 0, 0, 0, 0, 0, 0], 
				[0, 0, 0, 0, 0, 0, 0, 0],
				[1, 0, 0, 0, 0, 1, 0, 0],
				[1, 0, 0, 0, 0, 0, 1, 0],
				[1, 0, 0, 0, 0, 0, 1, 0], 
				[1, 0, 0, 0, 0, 0, 1, 0],
				[1, 0, 1, 0, 0, 0, 0, 0],
				[0, 1, 0, 0, 0, 0, 0, 0]]
	for i in range(4):
		m[i].setMatrix(bit)
	# printBitMatrix(m[0].getSplitedMatrix())
	# printBitMatrix(m[0].getMatrix())
	printByteMatrix(convertMat_BitToByte(m[0].getMatrix()))
	printBitMatrix(m[1].rotate90())
	printBitMatrix(m[2].rotate180())
	printBitMatrix(m[3].rotate270())