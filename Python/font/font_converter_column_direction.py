# import font_loader
"""フォントデータを8行 len(self.__s)*8列の配列に変換する"""
class FontConverter_ColumnDirection:
  def __init__(self, d : dict) -> None:
    self.__d = d
    self.__s = ''
    self.__matrix = []

  def convert(self, s : str):
    self.__s = s
    # 8行 len(self.__s)列の配列
    self.__matrix = [[0] * len(self.__s) for i in range (8)]
    index = 0
    half_word_counter = 0
    for i in range(len(self.__s)):
      d_matrix = self.__d[s[i]]

      if ord(s[i]) < 128:
        if half_word_counter % 2 == 1:
          for j in range(8):
            self.__matrix[j][index] += (d_matrix[j] & 0xf0) >> 4
          half_word_counter += 1  
          index += 1
        else:
          for j in range(8):
            # indexは加算しない
            self.__matrix[j][index] = d_matrix[j]
          half_word_counter += 1
      else:
        if half_word_counter % 2 == 1:
          for j in range(8):
            self.__matrix[j][index] += (d_matrix[j] & 0xf0) >> 4
            self.__matrix[j][index+1] += (d_matrix[j] & 0x0f) << 4
          index += 1
        else:
          for j in range(8):
            self.__matrix[j][index] = d_matrix[j]
          index += 1
    if(index != len(self.__s)):
      # 最後に不要な要素を削除
      for j in range(8):
        if half_word_counter % 2 == 1:
          del self.__matrix[j][index+1:]
        else:
          del self.__matrix[j][index:]
    return self.__matrix
  
  def get8x8Matrix(self, offset_bit:int) -> list:
    mat8x8 = [0] * 8
    # offset_bitが範囲外の可能性ががあるので，範囲内にする
    offset_bit %= 8*(len(self.__matrix[0]) - 1)
    offset_byte = offset_bit // 8
    offset_remainder = offset_bit % 8
    mask = 1
    for i in range(offset_remainder):
       mask = (mask << 1) + 1
    for i in range(8):
        mat8x8[i] = (self.__matrix[i][offset_byte] << offset_remainder) & 0xff
        mat8x8[i] |= (self.__matrix[i][offset_byte + 1] >> (8 - offset_remainder)) & mask
    return mat8x8
    
  def getMatrix(self):
    return self.__matrix
  
  def fontPreview(self):
    print('str=' + self.__s)
    for i in range(8):
      s = ''
      for j in range(len(self.__matrix[0])):
        for k in range(8):
          if(self.__matrix[i][j] & (0x80 >> k) == (0x80 >> k)):
             s += '・'
          else:
            s += '　'
      print(s)

def viewMat8x8(mat):
	for i in range(8):
		s = ''
		for j in range(8):
			if(mat[i] & (0x80 >> j) == (0x80 >> j)):
				s += '・'
			else:
				s += '　'
		print(s)


if __name__ == '__main__':
  import font_loader
  font = font_loader.FontLoader('./misaki_gothic_2nd.bdf')
  d = font.getDictionary()
  column_converter = FontConverter_ColumnDirection(d)
  a = column_converter.convert('あいうえおABC')
  for i in range(100):
     viewMat8x8(column_converter.get8x8Matrix(i))


