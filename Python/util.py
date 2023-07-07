import unicodedata

def viewMat8x8(mat):
	for i in range(8):
		s = ''
		for j in range(8):
			if(mat[i] & (0x80 >> j) == (0x80 >> j)):
				s += '・'
			else:
				s += '　'
		print(s)
def viewMat8x8_BitInfo(mat):
	for i in range(8):
		s = ''
		for j in range(8):
			if(mat[i][j] == 1):
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