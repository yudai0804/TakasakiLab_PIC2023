from pic_code_generator_delay import *
from led_matrix import *
class HardwareInformation:
  """
  PICCodeGeneratorを利用するにあたって，必要となるハードウェア情報を保持するクラス
  """
  def __init__( self,
                angle : int,
                row_port : str,
                row_pin : list[int], 
                column_port : str, 
                column_pin : list[int]):
    """
    Parameters
    ----------
    angle : LEDマトリクスの角度(0,90,180,270のどれか)
            rowとcolumnはangle度回転した後のもの
    row_port : rowのポート名
    row_pin : 0行目から7行目のピン名
    column_port : columnのポート名
    column_pin : 0列目から7列目のピン名
    """
    self.angle = angle
    self.row_port = row_port
    self.row_pin = row_pin
    self.column_port = column_port
    self.column_pin = column_pin

class PICCodeGenerator:
  """
  このクラスは基本抽象化は行わない方針，抽象化を行うのはLEDマトリクスの取付角度とピン配置のみ
  """
  def __init__(self, hardware : HardwareInformation, animation_hz : int):
    self.__hardware = hardware
    self.__animation_hz = animation_hz
    self.__one_cycle_ns = 1000
    self.__output = ""
    # 最後の要素の次のアドレス
    self.__end_addr = 0

  def __generateConfig( self,
                        led_matrix : LEDMatrix, 
                        is_row_direction_slide = None,
                        is_column_direction_slide = None,
                        is_no_slide = None):
    # configを設定
    self.__output += "LIST P=PIC16F1938\n"
    self.__output += "#include<p16f1938.inc>\n"
    self.__output += "__CONFIG\t_CONFIG1, _FOSC_INTOSC & _WDTE_OFF & _PWRTE_ON & _MCLRE_OFF & _CP_OFF & _CPD_OFF & _BOREN_OFF & _CLKOUTEN_OFF & _IESO_OFF & _FCMEN_OFF\n"
    self.__output += "__CONFIG\t_CONFIG2, _WRT_OFF & _VCAPEN_OFF & _PLLEN_OFF & _STVREN_OFF & _BORV_LO & _LVP_ON\n"
    for i in range(8):
      self.__output += "MATRIX" + str(i) + "\tEQU\t" + str(hex(112 + i) + "\n")
    for i in range(3):
      self.__output += "CNT" + str(i) + "\tEQU\t" + str(hex(120 + i) + "\n")
    # 書き込んだデータの末尾
    byte_size = 0
    mat = led_matrix.get()
    if is_row_direction_slide != None:
      byte_size = len(mat[0])
    elif is_column_direction_slide != None:
      byte_size = len(mat)
    elif is_no_slide != None:
      byte_size = len(mat[0]) * 8
    # 最後の要素の次のアドレス
    self.__end_addr = (byte_size // 80) * 128 + (byte_size % 80) + 32
  def __generateMatrixData( self,
                            led_matrix : LEDMatrix, 
                            is_row_direction_slide = None,
                            is_column_direction_slide = None,
                            is_no_slide = None):
    mat = led_matrix.get()
    byte = []
    output = ""
    org_cnt = 0
    # 条件に応じてbitからbyteに変換する
    if is_row_direction_slide != None:
      for i in range(len(mat[0]) // 8):
        split_bit = led_matrix.getSplitedMatrix(column_offset=8 * i)
        tmp_byte = convertMat_BitToByte(split_bit)
        for j in range(8):
          byte.append(tmp_byte[j])
    elif is_column_direction_slide != None:
      for i in range(len(mat) // 8):
        split_bit = led_matrix.getSplitedMatrix(row_offset=8 * i)
        tmp_byte = convertMat_BitToByte(split_bit)
        for j in range(8):
          byte.append(tmp_byte[j])
    elif is_no_slide != None:
      for i in range(len(mat[0])):
        split_bit = led_matrix.getSplitedMatrix(column_offset=i)
        tmp_byte = convertMat_BitToByte(split_bit)
        for j in range(8):
          byte.append(tmp_byte[j])
    # データを書き込む
    output = ""
    for i in range(len(byte)):
      if org_cnt % 80 == 0:
        if org_cnt != 0:
          output = output.rstrip(",")
        output += "\nORG\t" + str(hex((org_cnt // 80) * 128 + 32) + "\nDE\t")
      output += str(hex(byte[org_cnt])) + ","
      org_cnt += 1
    # 末尾の不要な文字を削除
    if output[-1] == ",":
      output = output.rstrip(",")
      output += "\n"
    self.__output += output
  def __generateInitialize(self):
    output = ""
    output += "ORG\t0x0000\n"
    # バンク1に切り替え
    output += "\tBSF BSR, BSR0\n"
    # OSCCONレジスタを捜査して，周期を4MHzにする
    output += "\tMOVLW B'01101000'\n"
    output += "\tMOVWF OSCCON\n"
    # PORTAを出力にする
    output += "\tCLRF TRISA\n"
    # PORTCを出力にする
    output += "\tCLRF TRISC\n"
    # バンク0に切り替え
    output += "\tBCF BSR, BSR0\n"
    # PORTAとPORTCの出力を0にする
    output += "\tCLRF PORTA\n"
    output += "\tCLRF PORTC\n"
    # FSRレジスタを0x020番地に合わせる
    output += "\tMOVWF FSR0H\n"
    output += "\tMOVLW 0x20\n"
    output += "\tMOVWF FSR0L\n"
    self.__output += output
  def __generateLoadData( self,
                          led_matrix : LEDMatrix, 
                          is_row_direction_slide = None,
                          is_column_direction_slide = None,
                          is_no_slide = None):
    output = "LOAD\n"
    if is_row_direction_slide != None or is_column_direction_slide != None:
      # データをシフト
      for i in range(1, 8):
        output += "\tMOVF MATRIX" + str(i) + ", W\n"
        output += "\tMOVWF MATRIX" + str(i - 1) + "\n"
      # MATRIX7のデータをFSR0から読む
      output += "\tMOVIW 0[FSR0]\n"
      output += "\tMOVWF MATRIX7\n"
      output += "\tADDFSR FSR0, 0x01\n"
    elif is_no_slide != None:
      # データをFSR0から読む
      for i in range(8):
        output += "\tMOVIW 0[FSR0]\n"
        output += "\tMOVWF MATRIX" + str(i) + "\n"
        output += "\tADDFSR FSR0, 0x01\n"
    # end_addrと一致していた場合はFSR0を0x20に戻す
    end_addr_h = self.__end_addr // 0xff
    end_addr_l = self.__end_addr & 0xff
    output += "\tMOVLW " + str(hex(end_addr_h)) + "\n"
    output += "\tSUBWF FSR0H, W\n"
    output += "\tBTFSS STATUS, Z\n"
    output += "\tRETURN\n"
    output += "\tMOVLW " + str(hex(end_addr_l)) + "\n"
    output += "\tSUBWF FSR0L, W\n"
    output += "\tBTFSS STATUS, Z\n"
    output += "\tRETURN\n"
    # FSR0がend_addrだったためFSR0を0x20にする
    output += "\tCLRF FSR0H\n"
    output += "\tMOVLW 0x20\n"
    output += "\tMOVWF FSR0L\n"
    output += "\tRETURN\n"
    self.__output += output

  def generate( self,
                led_matrix : LEDMatrix, 
                is_row_direction_slide = None,
                is_column_direction_slide = None,
                is_no_slide = None):
    mat = led_matrix.get()
    if len(mat) % 8 != 0 or len(mat[0]) % 8 != 0:
      print("led matrix error")
      return
    flag = 0
    if is_row_direction_slide != None:
      flag += 1
    if is_column_direction_slide != None:
      flag += 1
    if is_no_slide != None:
      flag += 1
    if flag != 1:
      print("argument error")
      return
    # PIC16F1938は960byte書き込むことができる
    if is_row_direction_slide != None or is_column_direction_slide != None:
      if len(mat) * len(mat[0]) > 960*8:
        return
    else:
      # 8*8*n < 960*8
      if 8*8*len(mat[0]) > 960*8:
        print(len(mat[0]))
        return
    
    self.__output = ""
    self.__generateConfig(led_matrix, is_row_direction_slide, 
                          is_column_direction_slide, is_no_slide)
    self.__generateMatrixData(led_matrix, is_row_direction_slide, 
                              is_column_direction_slide, is_no_slide)
    self.__generateInitialize()
    self.__generateLoadData(led_matrix, is_row_direction_slide, 
                            is_column_direction_slide, is_no_slide)

  def getHardwareInformation(is_suehiro = None, is_saito = None):
    if is_suehiro != None:
      h = HardwareInformation(90,
                              "PORTC",
                              [7,6,5,4,3,2,1,0],
                              "PORTA",
                              [0,6,1,3,5,2,7,4])
      return h
  def getOutput(self):
    return self.__output

if __name__ == '__main__':
  from font_converter_row_direction import *
  from font_loader import *
  from util import *
  f = FontLoader('./misaki_gothic_2nd.bdf')
  d = f.getDictionary()
  row_converter = FontConverter_RowDirection(d)
  # a = row_converter.convert('  WELCOME TMCIT')
  s = '  産技高専へようこそ！'
  s_len = getStringLendth(s)
  led = LEDMatrix(mat=row_converter.convert(s))
  # led.print()
  # print(led.get())
  m = led.get()
  print(len(m), len(m[0]))
  hw_info = PICCodeGenerator.getHardwareInformation(is_suehiro=True)
  pic = PICCodeGenerator(hw_info, 10)
  pic.generate(led, is_row_direction_slide=True)
  # pic.generate(led, is_no_slide=True)
  print(pic.getOutput())