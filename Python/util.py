import unicodedata

def splitMatrix_BitInfo_RowDirection(mat, offset_bit, split_bit_size = 8):
	# offset_bitが範囲外の可能性があるので，範囲内にする
	offset_bit %= len(mat[0]) - 1
	m = [[0] * split_bit_size for i in range(split_bit_size)]
	for i in range(split_bit_size):
		for j in range(split_bit_size):
			index_j = (offset_bit + j) % (len(mat[0]) - 1)
			m[i][j] = mat[i][index_j]
	return m

def convertMat_BitToByte(mat):
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

def convertMat_ByteToBit(mat):
	m = [[0] * (len(mat[0]) * 8) for i in range(len(mat))]
	for i in range(len(mat)):
		for j in range(len(mat[0])):
			for k in range(8):
				if mat[i][j] & (0x80 >> k) == (0x80 >> k):
					m[i][8*j+k] = 1
	return m

def viewMatBitInfo(mat):
	for i in range(len(mat)):
		s = ''
		for j in range(len(mat[0])):
			if mat[i][j] == 1:
				s += '・'
			else:
				s += '　'
		print(s)

def viewMatByteInfo(mat):
	for i in range(len(mat)):
		s = ''
		for j in range(8):
			if mat[i] & (0x80 >> j) == (0x80 >> j):
				s += '・'
			else:
				s += '　'
		print(s)

def getStringLendth(text):
	"""
	参考:https://note.nkmk.me/python-unicodedata-east-asian-width-count/
	"""
	count = 0
	for c in text:
		if unicodedata.east_asian_width(c) in 'FWA':
			count += 2
		else:
			count += 1
	mod = count % 2
	count = count //2 + mod
	return count