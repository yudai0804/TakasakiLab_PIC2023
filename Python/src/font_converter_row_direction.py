from util import *
"""フォントデータを8行 len(self.__s)*8列の配列に変換する"""
class FontConverter_RowDirection:
	def __init__(self, d : dict) -> None:
		self.__d = d
		self.__s = ''
		self.__matrix = []

	def convert(self, s : str):
		# バイトに圧縮した情報で計算し，最後にビット情報に変換する
		self.__s = s
		# 8行 len(self.__s)列の配列
		matrix = [[0] * len(self.__s) for i in range (8)]
		index = 0
		half_word_counter = 0
		for i in range(len(self.__s)):
			d_matrix = self.__d[s[i]]
			if ord(s[i]) < 128:
				if half_word_counter % 2 == 1:
					for j in range(8):
						matrix[j][index] += (d_matrix[j] & 0xf0) >> 4
					half_word_counter += 1  
					index += 1
				else:
					for j in range(8):
						# indexは加算しない
						matrix[j][index] = d_matrix[j]
					half_word_counter += 1
			else:
				if half_word_counter % 2 == 1:
					for j in range(8):
						matrix[j][index] += (d_matrix[j] & 0xf0) >> 4
						matrix[j][index+1] += (d_matrix[j] & 0x0f) << 4
					index += 1
				else:
					for j in range(8):
						matrix[j][index] = d_matrix[j]
					index += 1
		if index != len(self.__s):
			# 最後に不要な要素を削除
			for j in range(8):
				if half_word_counter % 2 == 1:
					del matrix[j][index+1:]
				else:
					del matrix[j][index:]
		# バイトから8行8*n列のビットに変換
		self.__matrix = [[0] * (len(matrix[0]) * 8) for i in range(len(matrix))]
		for i in range(len(matrix)):
			for j in range(len(matrix[0])):
				for k in range(8):
					if matrix[i][j] & (0x80 >> k) == (0x80 >> k):
						self.__matrix[i][8*j+k] = 1

		return self.__matrix    

	def getMatrix_BitInfo(self):
		return self.__matrix

if __name__ == '__main__':
	import font_loader
	from led_matrix import *
	from util import *
	font = font_loader.FontLoader('../../font/misaki_gothic_2nd.bdf')
	d = font.getDictionary()
	row_converter = FontConverter_RowDirection(d)
	a = row_converter.convert('あいうえおABC')
	m = LEDMatrix(mat=a)
	for i in range(100):
		printBitMatrix(m.getSplitedMatrix(column_offset=i))

