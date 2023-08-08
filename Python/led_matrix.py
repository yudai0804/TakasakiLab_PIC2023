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
	def setBitMatrix(self, mat):
		self.__mat = mat
	def transpose(self):
		tmp = self.__mat
		# 転置行列(j行i列)
		self.__mat = [[0] * len(tmp) for i in range (len(tmp[0]))]
		for i in range(len(tmp)):
			for j in range(len(tmp[0])):
				self.__mat[j][i] = tmp[i][j]
	def rotate90(self):
		tmp = self.__mat
		for i in range(len(self.__mat)):
			for j in range(len(self.__mat[0])):
				self.__mat[i][j] = tmp[i][len(self.__mat[0]) - j - 1]
	def getSplitedMatrix(self, row_size, column_size, row_offset = 0, column_offset = 0):
		m = [[0] * column_size for i in range(row_size)]
		for i in range(row_size):
			for j in range(column_size):
				m[i][j] = self.__mat[i + row_offset][j + column_offset]
		return m
	def getBitMatrix(self):
		return self.__mat

def convertMatrix_BitToByte(mat):
	_mat = []
	m = []
	column = 0
	if (len(mat[0]) % 8) != 0:
		print('matrix error')
		return
	else:
		column = int(len(mat[0]) / 8)
	m = [[0] * column for i in range(len(mat))]
	_mat = [[0] * (column*8) for i in range(len(mat))]
	for i in range(len(mat)):
		for j in range(len(mat[0])):
			_mat[i][j] = mat[i][j]
	for i in range(len(mat)):
		for j in range(column):
			for k in range(8):
				if _mat[i][8 * j + k] == 1:
					m[i][j] += (0x80 >> k)
	return m

def convertMatrix_ByteToBit(mat):
	m = [[0] * (len(mat[0]) * 8) for i in range(len(mat))]
	for i in range(len(mat)):
		for j in range(len(mat[0])):
			for k in range(8):
				if mat[i][j] & (0x80 >> k) == (0x80 >> k):
					m[i][8*j+k] = 1
	return m

def viewBitMatrix(mat):
	for i in range(len(mat)):
		s = ''
		for j in range(len(mat[0])):
			if mat[i][j] == 1:
				s += '・'
			else:
				s += '　'
		print(s)

def viewByteMatrix(mat):
	for i in range(len(mat)):
		s = ''
		for j in range(8):
			if mat[i] & (0x80 >> j) == (0x80 >> j):
				s += '・'
			else:
				s += '　'
		print(s)

if __name__ == '__main__':
	m = LEDMatrix(8, 8)
	# bit = [[1, 1, 0, 0, 1, 1, 0, 0],
	# 			 [1, 1, 0, 0, 1, 1, 0, 0],
	# 			 [1, 0, 0, 0, 1, 1, 0, 0],
	# 			 [1, 1, 0, 0, 1, 1, 0, 0],
	# 			 [1, 1, 0, 0, 1, 1, 0, 0],
	# 			 [1, 1, 0, 0, 0, 1, 0, 0],
	# 			 [1, 1, 0, 0, 1, 1, 0, 0],
	# 			 [1, 1, 0, 0, 1, 1, 0, 0],]
	bit = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 1, 0, 0], [1, 0, 0, 0, 0, 0, 1, 0], [1, 0, 0, 0, 0, 0, 1, 0], [1, 0, 0, 0, 0, 0, 1, 0], [1, 0, 1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0]]
	m.setBitMatrix(bit)
	# m.transpose()
	m.rotate90()
	viewBitMatrix(m.getBitMatrix())