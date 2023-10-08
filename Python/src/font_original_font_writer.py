import os

def writeOriginalFont(font_name,mat,dir='./original_font'):
	"""
	font_nameはファイル名になる
	"""
	os.makedirs(dir, exist_ok=True)
	with open(os.path.join(dir, font_name + '.original_font'), 'w') as f:
		# 1行目はフォントのサイズ情報
		s = str(len(mat)) + ',' + str(len(mat[0])) + '\n'
		f.write(s)
		# 以降はフォントのデータ
		for i in range(len(mat)):
			s = ''
			for j in range(len(mat[0])):
				s += str(mat[i][j]) + ','
			# 一番右の文字を削除
			s = s.rstrip(',')
			s += '\n'
			f.write(s)