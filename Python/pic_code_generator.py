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

  def __generateConfig(self):
    # configを設定
    self.__output += "LIST P=PIC16F1938\n"
    self.__output += "#include<p16f1938.inc>\n"
    self.__output += "__CONFIG\t_CONFIG1, _FOSC_INTOSC & _WDTE_OFF & _PWRTE_ON & _MCLRE_OFF & _CP_OFF & _CPD_OFF & _BOREN_OFF & _CLKOUTEN_OFF & _IESO_OFF & _FCMEN_OFF\n"
    self.__output += "__CONFIG\t_CONFIG2, _WRT_OFF & _VCAPEN_OFF & _PLLEN_OFF & _STVREN_OFF & _BORV_LO & _LVP_ON\n"
    for i in range(8):
      self.__output += "MATRIX" + str(i) + "\tEQU " + str(hex(112 + i) + "\n")
    for i in range(3):
      self.__output += "CNT" + str(i) + "\tEQU" + str(hex(120 + i) + "\n")
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
  def generate( self,
                led_matrix : LEDMatrix, 
                is_row_direction_slide = None,
                is_column_direction_slide = None,
                is_no_slide = None):
    # TODO 最初に引数チェックを必ず行う
    self.__output = ""
    self.__generateConfig()
    self.__generateMatrixData(led_matrix, is_row_direction_slide, 
                              is_column_direction_slide, is_no_slide)

  def getHardwareInformation(is_suehiro = None, is_saito = None):
    if is_suehiro != None:
      h = HardwareInformation(90,
                              "PORTC",
                              [7,6,5,4,3,2,1,0],
                              "PORTA",
                              [0,6,1,3,5,2,7,4])
      return h
