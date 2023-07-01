font_path = './misaki_gothic_2nd.bdf'
NO_DETECT = 0
DETECT = 1
END = 2

STARTFONT = NO_DETECT
PIXEL_SIZE = 8
# 文字セグメント数
CHARS = -1
dictionary = {}
# フォントデータを読み込み
with open(font_path, encoding='utf-8') as f:
	# すべての行を取得
	# 行を取得した後に改行文字をすべて削除
	lines = [s.replace('\n', '') for s in f.readlines()]

tmp_utf8_str = -1
tmp_bitmap = [0] * PIXEL_SIZE
tmp_bitmap_index = 0
detect_start_bitmap = False
for s in lines:
	if(s.startswith('ENCODING ')):
		s = s.replace('ENCODING ', '')
		tmp_utf8_str = chr(int(s))
	elif('BITMAP' in s):
		# この後ビットマップ情報が来るため変数を初期化する
		detect_start_bitmap = True
	elif('ENDCHAR' in s):
		# 辞書型変数に値を追加する
		# print(tmp_utf8_str, tmp_bitmap)
		dictionary[tmp_utf8_str] = tmp_bitmap
		tmp_bitmap_index = 0
		tmp_bitmap = [0] * PIXEL_SIZE
		detect_start_bitmap = False
	elif(detect_start_bitmap == True):
		tmp_bitmap[tmp_bitmap_index] = int(s, 16)
		tmp_bitmap_index += 1
print(len(lines))
print(dictionary['0'])