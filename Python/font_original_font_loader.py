import os
import glob

class OriginalFontLoader:
	def __init__(self, dir_name='original_font'):
		self.__dir = dir_name
		self.__d = {}
		self.load()
	def load(self):
		path = glob.glob(self.__dir + '/*.original_font')
		for p in path:
			with open(p,encoding='utf-8') as f:
				lines = [s.replace('\n', '') for s in f.readlines()]
				mat_size = lines[0].split(',')
				mat_row_size = int(mat_size[0])
				mat_column_size = int(mat_size[1])
				mat = [[0] * mat_column_size for i in range(mat_row_size)]
				#最初に1行読んでいるのでindexは1
				index = 1
				while(True):
					mat[index-1] = lines[index].split(',')
					#str型からint型にキャスト
					for j in range(mat_column_size):
						mat[index-1][j] = int(mat[index-1][j])
					index += 1
					if index == mat_row_size + 1:
						break
				s = os.path.basename(p)
				s = s.replace('.original_font', '')
				self.__d[s] = mat
		return self.__d
	def getDictionary(self):
		return self.__d

if __name__ == '__main__':
	from led_matrix import *
	loader = OriginalFontLoader()
	d = loader.getDictionary()
	for k in d.keys():
		print(k)
		viewBitMatrix(d[k])