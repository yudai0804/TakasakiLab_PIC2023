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
            rowとcolumnはLEDMatrixのデータシート準拠
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
    self.__one_flame_us = int(1 / animation_hz * 1e6)
    self.__one_cycle_ns = 1000
    self.__led_delay_us = 1250
    self.__output = ""
    if self.__one_flame_us < 8 * self.__led_delay_us:
      self.__one_flame_us = int(8 * self.__led_delay_us)
    if self.__one_flame_us % ( 8 * self.__led_delay_us) != 0:
      self.__one_flame_us -= self.__one_flame_us % (8 * self.__led_delay_us)
    if self.__one_flame_us // (8 * self.__led_delay_us) > 255:
      print("error")
    # データの大きさ
    self.__data_size = 0

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
    self.__output += "LOOP_CNT\tEQU\t0x7b\n"
    self.__output += "SIZE_H\tEQU\t0x7c\n"
    self.__output += "SIZE_L\tEQU\t0x7d\n"
  def __generateMatrixData( self,
                            led_matrix : LEDMatrix, 
                            is_row_direction_slide = None,
                            is_column_direction_slide = None,
                            is_no_slide = None):
    mat = led_matrix.get()
    byte = []
    output = ""
    org_cnt = 0
    if self.__hardware.angle == 0:
      print("未実装")
    elif self.__hardware.angle == 90:
      # 条件に応じてbitからbyteに変換する
      if is_row_direction_slide != None or is_no_slide != None:
        for i in range(len(mat[0]) // 8):
          split_bit = led_matrix.getSplitedMatrix(column_offset=8 * i)
          split_led = LEDMatrix(mat = split_bit)
          for i in range(8):
            tmp_byte = 0
            for j in range(8):
              tmp_byte += split_bit[7-j][i] << j
            byte.append(tmp_byte)
      elif is_column_direction_slide != None:
        print("実装中")
        # for i in range(len(mat) // 8):
        #   split_bit = led_matrix.getSplitedMatrix(row_offset=8 * i)
        #   split_led = LEDMatrix(mat = split_bit)
        #   bit = split_led.getRotate(self.__hardware.angle)
        #   for i in range(8):
        #     tmp_byte = 0
        #     for j in range(8):
        #       tmp_byte += bit[i][j] << self.__hardware.row_pin[j]
        #     byte.append(tmp_byte)
    elif self.__hardware.angle == 180:
      print("未実装")
    elif self.__hardware.angle == 270:
      print("未実装")
    # データを書き込む
    # 理由はわからないが，DTは4バイトずづで区切るとうまくいく
    # 参考:http://www.picfun.com/pic18/tech18x02.html
    output = "LEDMATRIX_DATA\n\tDT "
    for i in range(len(byte)):
      if i % 4 == 0 and i != 0:
        if output[-1] == ",":
          output = output.rstrip(",")
          output += "\n"
          output += "\tDT "
      output += str(hex(byte[i])) + ","
    if output[-1] == ",":
      output = output.rstrip(",")
      output += "\n"
    self.__output += output
    self.__data_size = len(byte)
  def __generateInitialize(self):
    output = ""
    output += "ORG 0x0000\n"
    # バンク1に切り替え
    output += "\tBSF BSR, BSR0\n"
    # OSCCONレジスタを捜査して，周期を4MHzにする
    output += "\tMOVLW B'01101000'\n"
    output += "\tMOVWF OSCCON\n"
    # PORTを出力にする
    tris_col = self.__hardware.column_port
    tris_row = self.__hardware.row_port
    tris_col = tris_col.replace("PORT", "")
    tris_row = tris_row.replace("PORT", "")
    output += "\tCLRF TRIS" + tris_col + "\n"
    output += "\tCLRF TRIS" + tris_row + "\n"
    # バンク0に切り替え
    output += "\tBCF BSR, BSR0\n"
    # 出力を0にする
    output += "\tCLRF " + self.__hardware.column_port + "\n"
    output += "\tCLRF " + self.__hardware.row_port + "\n"
    # FSR0レジスタをLEDMATRIX_DATA番地に合わせる
    output += "\tMOVLW HIGH LEDMATRIX_DATA\n"
    output += "\tMOVWF FSR0H\n"
    output += "\tMOVLW LOW LEDMATRIX_DATA\n"
    output += "\tMOVWF FSR0L\n"
    # FSR1レジスタを0x70番地に合わせる
    output += "\tCLRF FSR1H\n"
    output += "\tMOVLW 0x70\n"
    output += "\tMOVWF FSR1L\n"
    # MATRIXの初期値に0を代入
    for i in range(8):
      output += "\tCLRF MATRIX" + str(i) + "\n"
    # SIZEの初期値に0を代入
    output += "\tCLRF SIZE_H\n"
    output += "\tCLRF SIZE_L\n"
    # メインループに飛ぶ
    output += "\tGOTO LOOP\n"
    self.__output += output
  def __generateMainLoop( self,
                          led_matrix : LEDMatrix, 
                          is_row_direction_slide = None,
                          is_column_direction_slide = None,
                          is_no_slide = None):
    output = "LOOP\n"
    output += "\tCALL LOAD\n"
    loop_cnt = self.__one_flame_us // (8 * self.__led_delay_us)
    output += "\tMOVLW D'" + str(loop_cnt) + "'\n"
    output += "\tMOVWF LOOP_CNT\n"
    output += "LOOP_JUMP0\n"
    output += "\tCALL LEDMATRIX\n"
    output += "\tDECFSZ LOOP_CNT\n"
    output += "\tGOTO LOOP_JUMP0\n"
    output += "\tGOTO LOOP\n"
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
      # SIZEを更新
      output += "\tINCF SIZE_L, F\n"
      output += "\tBTFSC STATUS, Z\n"
      output += "\tINCF SIZE_H, F\n"
    elif is_no_slide != None:
      # データをFSR0から読む
      for i in range(8):
        output += "\tMOVIW 0[FSR0]\n"
        output += "\tMOVWF MATRIX" + str(i) + "\n"
        output += "\tADDFSR FSR0, 0x01\n"
        # SIZEを更新
        output += "\tINCF SIZE_L, F\n"
        output += "\tBTFSC STATUS, Z\n"
        output += "\tINCF SIZE_H, F\n"
    # FSR0で読んだデータの大きさがSIZEと等しいかを確認する
    output += "\tMOVLW " + str(hex(self.__data_size // 256)) + "\n"
    output += "\tSUBWF SIZE_H, W\n"
    output += "\tBTFSS STATUS, Z\n"
    output += "\tRETURN\n"
    output += "\tMOVLW " + str(hex(self.__data_size % 256)) + "\n"
    output += "\tSUBWF SIZE_L, W\n"
    output += "\tBTFSS STATUS, Z\n"
    output += "\tRETURN\n"
    # SIZEを0にする
    output += "\tCLRF SIZE_H\n"
    output += "\tCLRF SIZE_L\n"
    # FSR0がデータの末尾だった場合はFSR0をLEDMATRIX_DATAに合わせる
    output += "\tMOVLW HIGH LEDMATRIX_DATA\n"
    output += "\tMOVWF FSR0H\n"
    output += "\tMOVLW LOW LEDMATRIX_DATA\n"
    output += "\tMOVWF FSR0L\n"
    output += "\tRETURN\n"
    self.__output += output

  def __generateLightLEDMatrix( self,
                                led_matrix : LEDMatrix, 
                                is_row_direction_slide = None,
                                is_column_direction_slide = None,
                                is_no_slide = None):
    output = "LEDMATRIX\n"
    if self.__hardware.angle == 0:
      print("未実装")
    elif self.__hardware.angle == 90:
      for i in range(8):
        output += "\tMOVIW FSR1++\n"
        if is_column_direction_slide != None:
          print("実装中")
          # output += "\tMOVWF " + self.__hardware.row_port + "\n"
          # output += "\tMOVLW " + str(hex(self.__hardware.column_pin[i])) + "\n"
          # output += "\tMOVWF " + self.__hardware.column_port + "\n"
        else:
          output += "\tMOVWF " + self.__hardware.column_port + "\n"

          output += "\tMOVLW " + str(hex(255 - (1 << self.__hardware.row_pin[i]))) + "\n"
          output += "\tMOVWF " + self.__hardware.row_port + "\n"
        output += "\tCALL LED_DELAY\n"
    elif self.__hardware.angle == 180:
      print("未実装")
    elif self.__hardware.angle == 270:
      print("未実装")
    # FSR1を0x70に戻す
    output += "\tMOVLW 0x70\n"
    output += "\tMOVWF FSR1L\n"
    output += "\tRETURN\n"
    delay = PICCodeGenerator_Delay(self.__one_cycle_ns, label_name="LED_DELAY_JUMP")
    delay_str = delay.generateDelay(self.__led_delay_us, "us", "LED_DELAY")
    if delay_str == "":
      print("delay generate error")
      return
    self.__output += output
    self.__output += delay_str

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
    
    self.__output = ""
    self.__generateConfig(led_matrix, is_row_direction_slide, 
                          is_column_direction_slide, is_no_slide)
    self.__generateInitialize()
    self.__generateMainLoop(led_matrix, is_row_direction_slide, 
                            is_column_direction_slide, is_no_slide)
    self.__generateMatrixData(led_matrix, is_row_direction_slide, 
                              is_column_direction_slide, is_no_slide)
    self.__generateLoadData(led_matrix, is_row_direction_slide, 
                            is_column_direction_slide, is_no_slide)
    self.__generateLightLEDMatrix(led_matrix, is_row_direction_slide, 
                                  is_column_direction_slide, is_no_slide)
    # 末尾にENDを追加
    self.__output += "END\n"

  def getHardwareInformation(is_suehiro = None, is_saito = None):
    if is_suehiro != None:
      h = HardwareInformation(90,
                              "PORTA",
                              [0,6,1,3,5,2,7,4],
                              "PORTC",
                              [0,1,2,3,4,5,6,7])
      return h
  def getOutput(self):
    return self.__output

if __name__ == '__main__':
  from font_converter_row_direction import *
  from font_loader import *
  from util import *
  import os
  f = FontLoader('./misaki_gothic_2nd.bdf')
  d = f.getDictionary()
  row_converter = FontConverter_RowDirection(d)
  # a = row_converter.convert('  WELCOME TMCIT')
  # s = '  さんぎこうせんあらかわキャンパスへようこそ'
  s = '  じょうほうつうしんこうがくコース'
  s_len = getStringLendth(s)
  led = LEDMatrix(mat=row_converter.convert(s))
  m = led.get()
  hw_info = PICCodeGenerator.getHardwareInformation(is_suehiro=True)
  # pic = PICCodeGenerator(hw_info, 8)
  # pic.generate(led, is_row_direction_slide=True)
  pic = PICCodeGenerator(hw_info, 1)
  pic.generate(led, is_no_slide=True)
  os.makedirs("tmp", exist_ok=True)
  with open("tmp/test.asm", mode="w") as f:
    f.write(pic.getOutput())

  # print(pic.getOutput())