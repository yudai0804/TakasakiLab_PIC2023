def viewMat8x8(mat):
	for i in range(8):
		s = ''
		for j in range(8):
			if(mat[i] & (0x80 >> j) == (0x80 >> j)):
				s += '・'
			else:
				s += '　'
		print(s)