# BDFファイルの仕様書:https://adobe-type-tools.github.io/font-tech-notes/pdfs/5005.BDF_Spec.pdf

class FontLoader:
	def __init__(self, font_path : str) -> None:
		self.__dictionary = {}
		self.load(font_path)

	def load(self, font_path : str) -> None:
		self.__dictionary = {}
		tmp_utf8_str = -1
		tmp_bitmap = []
		detect_start_bitmap = False
		offset_x = 0
		offset_y = 0
		# フォントデータをファイルから取得
		with open(font_path, encoding='utf-8') as f:
			# すべての行を取得
			# 行を取得した後に改行文字をすべて削除
			lines = [s.replace('\n', '') for s in f.readlines()]
		# 辞書型に変換
		for s in lines:
			if s.startswith('ENCODING '):
				s = s.replace('ENCODING ', '')
				# 文字コードからstrに変換
				tmp_utf8_str = chr(int(s))
				tmp_bitmap = []
			elif 'BBX' in s:
				tmp_list = s.split()
				offset_x = int(tmp_list[3])
				offset_y = int(tmp_list[4])
			elif 'BITMAP' in s:
				# この後ビットマップ情報が来るため変数を初期化する
				detect_start_bitmap = True
			elif 'ENDCHAR' in s:
				# offsetの処理
				for i in range(len(tmp_bitmap)):
					tmp_bitmap[i] = tmp_bitmap[i] >> offset_x
				for i in range(offset_y):
					tmp_bitmap.append(0)
				# ビットマップ情報が省略されている場合は先頭バイトのものから順に省略されているため，それの処理
				length = len(tmp_bitmap)
				for i in range(8 - length):
					tmp_bitmap.insert(0, 0)
				# 辞書型変数に値を追加する				
				self.__dictionary[tmp_utf8_str] = tmp_bitmap
				tmp_bitmap = [0] * 8
				detect_start_bitmap = False
			elif detect_start_bitmap == True:
				tmp_bitmap.append(int(s, 16))

	def getDictionary(self) -> dict:
		return self.__dictionary

if __name__ == '__main__':
	from util import *
	font = FontLoader('../../font/misaki_gothic_2nd.bdf')
	d = font.getDictionary()
	
	s = '山口雄大'
	printByteMatrix(d['山'])
	printByteMatrix(d['口'])
	printByteMatrix(d['雄'])
	printByteMatrix(d['大'])
	printByteMatrix(d['-'])
	printByteMatrix(d['.'])
