import font_loader
"""フォントデータを8行 len(self.__s)*8列の配列に変換する"""
class FontConverter_RowDirection:
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
          
if __name__ == '__main__':
  font = font_loader.FontLoader('./misaki_gothic_2nd.bdf')
  d = font.getDictionary()
  row_converter = FontConverter_RowDirection(d)
  a = row_converter.convert('あいうえおABC')
  print(a)
  row_converter.fontPreview()


