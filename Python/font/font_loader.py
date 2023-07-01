
class FontLoader:
	def __init__(self) -> None:
		self.__PixelSize = -1
		self.__dictionary = {}

	def load(self, font_path : str, pixel_size = 8) -> None:
		self.__dictionary = {}
		self.__PixelSize = pixel_size
		tmp_utf8_str = -1
		tmp_bitmap = [0] * self.__PixelSize
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
				tmp_bitmap = [0] * self.__PixelSize
				detect_start_bitmap = False
			elif(detect_start_bitmap == True):
				tmp_bitmap[tmp_bitmap_index] = int(s, 16)
				tmp_bitmap_index += 1
	
	def getPixelSize(self) -> int:
		return self.__PixelSize

	def getDictionary(self) -> dict:
		return self.__dictionary

if __name__ == '__main__':
	font = FontLoader()
	font.load('./misaki_gothic_2nd.bdf')
	d = font.getDictionary()
	print(d['0'])