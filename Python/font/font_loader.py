
class FontLoader:
	def __init__(self, font_path : str) -> None:
		self.__dictionary = {}
		self.load(font_path)

	def load(self, font_path : str) -> None:
		self.__dictionary = {}
		tmp_utf8_str = -1
		tmp_bitmap = [0] * 8
		tmp_bitmap_index = 0
		detect_start_bitmap = False
		# フォントデータをファイルから取得
		with open(font_path, encoding='utf-8') as f:
			# すべての行を取得
			# 行を取得した後に改行文字をすべて削除
			lines = [s.replace('\n', '') for s in f.readlines()]
		# 辞書型に変換
		for s in lines:
			if(s.startswith('ENCODING ')):
				s = s.replace('ENCODING ', '')
				# 文字コードからstrに変換
				tmp_utf8_str = chr(int(s))
			elif('BITMAP' in s):
				# この後ビットマップ情報が来るため変数を初期化する
				detect_start_bitmap = True
			elif('ENDCHAR' in s):
				# 辞書型変数に値を追加する
				self.__dictionary[tmp_utf8_str] = tmp_bitmap
				tmp_bitmap_index = 0
				tmp_bitmap = [0] * 8
				detect_start_bitmap = False
			elif(detect_start_bitmap == True):
				tmp_bitmap[tmp_bitmap_index] = int(s, 16)
				tmp_bitmap_index += 1

	def getDictionary(self) -> dict:
		return self.__dictionary
	
	def fontPreview(self, _s : str) -> None:
		print('preview font = ' + _s)
		s = ''
		for i in range(8):
			s = ''
			for j in range(8):
				if(self.__dictionary[_s][i] & (0x80 >> j) == (0x80 >> j)):
					s += '・'
				else:
					s += '　'
			print(s)

if __name__ == '__main__':
	font = FontLoader('./misaki_gothic_2nd.bdf')
	d = font.getDictionary()
	font.fontPreview('山')
	font.fontPreview('口')
	font.fontPreview('雄')
	font.fontPreview('大')
