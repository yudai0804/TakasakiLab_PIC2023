from pic_code_generator_delay import *
from led_matrix import *
class HardwareInformation:
    """
    PICCodeGeneratorを利用するにあたって，必要となるハードウェア情報を保持するクラス
    """
    def __init__(self,
                 row_port : str,
                 row_pin : list[int],
                 column_port : str,
                 column_pin : list[int]):
        """
        Parameters
        ----------
        row_port : rowのポート名
        row_pin : 0行目から7行目のピン名
        column_port : columnのポート名
        column_pin : 0列目から7列目のピン名
        """
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
        self.__data_size = []

    def __generateConfig(self,
                         led_matrix : list[LEDMatrix], 
                         is_row_direction_slide = None,
                         is_column_direction_slide = None,
                         is_no_slide = None):
        # configを設定
        self.__output += ";GitHub:https://github.com/yudai0804/TakasakiLab_PIC2023\n"
        self.__output += "LIST P=PIC16F1938\n"
        self.__output += "#include<p16f1938.inc>\n"
        self.__output += "\n"
        self.__output += "__CONFIG\t_CONFIG1, _FOSC_INTOSC & _WDTE_OFF & _PWRTE_ON & _MCLRE_OFF & _CP_OFF & _CPD_OFF & _BOREN_OFF & _CLKOUTEN_OFF & _IESO_OFF & _FCMEN_OFF\n"
        self.__output += "__CONFIG\t_CONFIG2, _WRT_OFF & _VCAPEN_OFF & _PLLEN_OFF & _STVREN_OFF & _BORV_LO & _LVP_OFF\n"
        self.__output += "\n"
        self.__output += "; LEDマトリクス描画用の一時変数\n"
        for i in range(8):
            self.__output += "MATRIX" + str(i) + "\tEQU\t" + format(112 + i, "#04x") + "\n"
        self.__output += "; delay生成用変数\n"
        for i in range(3):
            self.__output += "CNT" + str(i) + "\tEQU\t" + format(120 + i, "#04x") + "\n"
        self.__output += "; 描画更新周期用変数\n"
        self.__output += "LOOP_CNT\tEQU\t0x7b\n"
        self.__output += "; 文字データを読み出す際のオフセット用変数\n"
        self.__output += "OFFSET_L\tEQU\t0x7c\n"
        self.__output += "OFFSET_H\tEQU\t0x7d\n"
        self.__output += "; 現在のモードを保持する変数\n"
        self.__output += "MODE\tEQU\t0x7e\n"
        self.__output += "\n"
    def __generateMatrixData(self,
                             view_str : list[str],
                             led_matrix : list[LEDMatrix],
                             is_row_direction_slide = None,
                             is_column_direction_slide = None,
                             is_no_slide = None):
        output = ""
        for i in range(len(led_matrix)):
            byte = []
            mat = led_matrix[i].get()
            # 条件に応じてbitからbyteに変換する
            if is_row_direction_slide != None or is_no_slide != None:
                for j in range(len(mat[0]) // 8):
                    split_bit = led_matrix[i].getSplitedMatrix(column_offset=8 * j)
                    for k in range(8):
                        tmp_byte = 0
                        for l in range(8):
                            tmp_byte += split_bit[7 - l][k] << self.__hardware.column_pin[l]
                        byte.append(tmp_byte)
            elif is_column_direction_slide != None:
                for j in range(len(mat) // 8):
                    split_bit = led_matrix[i].getSplitedMatrix(row_offset=8 * j)
                    for k in range(8):
                        tmp_byte = 0
                        for l in range(8):
                            # rowはカソード側のためビットを反転
                            if split_bit[k][l] == 0:
                                tmp_byte += 1 << self.__hardware.row_pin[l]
                        byte.append(tmp_byte)
            # データを書き込む
            # 理由はわからないが，DTは4バイトずづで区切るとうまくいく
            # 参考:http://www.picfun.com/pic18/tech18x02.html
            output = "; 文字列「" + view_str[i][1:-1] + "」のデータ\n"
            output += "LEDMATRIX_DATA" + str(i) + "\n"
            output += "\tDT "
            for j in range(len(byte)):
                if j % 4 == 0 and j != 0:
                    if output[-1] == ",":
                        output = output.rstrip(",")
                        output += "\n"
                        output += "\tDT "
                output += format(byte[j], "#04x") + ","
            if output[-1] == ",":
                output = output.rstrip(",")
                output += "\n"
            output += "\n"
            self.__output += output
            self.__data_size.append(len(byte))

    def __generateInitialize(self,
                             led_matrix : list[LEDMatrix], 
                             is_row_direction_slide = None,
                             is_column_direction_slide = None,
                             is_no_slide = None):
        output = ""
        output += "ORG 0x0000\n"
        output += "\t; OSCCONレジスタを操作して、制御周期を4MHzに設定\n"
        output += "\t; バンク1に切り替え\n"
        # バンク1に切り替え
        output += "\tBSF BSR, BSR0\n"
        # OSCCONレジスタを操作して，周期を4MHzにする
        output += "\tMOVLW B'01101000'\n"
        output += "\tMOVWF OSCCON\n"
        # PORTを出力にする
        output += "\t; PORTA、PORTCを出力に設定\n"
        tris_col = self.__hardware.column_port
        tris_row = self.__hardware.row_port
        tris_col = tris_col.replace("PORT", "")
        tris_row = tris_row.replace("PORT", "")
        output += "\tCLRF TRIS" + tris_col + "\n"
        output += "\tCLRF TRIS" + tris_row + "\n"
        # バンク0に切り替え
        output += "\t; バンク0に切り替え\n"
        output += "\tBCF BSR, BSR0\n"
        # 出力を0にする
        output += "\t; 出力を0にする\n"
        output += "\tCLRF " + self.__hardware.column_port + "\n"
        output += "\tCLRF " + self.__hardware.row_port + "\n"
        # FSR0レジスタをLEDMATRIX_DATA0番地に合わせる
        output += "\t; FSR0レジスタをLEDMATRIX_DATA0番地に合わせる\n"
        output += "\tMOVLW LOW LEDMATRIX_DATA0\n"
        output += "\tMOVWF FSR0L\n"
        output += "\tMOVLW HIGH LEDMATRIX_DATA0\n"
        output += "\tMOVWF FSR0H\n"
        # FSR1レジスタを0x70番地に合わせる
        output += "\t; FSR1レジスタを0x70番地に合わせる\n"
        output += "\tCLRF FSR1H\n"
        output += "\tMOVLW 0x70\n"
        output += "\tMOVWF FSR1L\n"
        output += "\t; MATRIXを初期値に設定\n"
        if is_column_direction_slide != None:
            # MATRIXの初期値に255を代入
            output += "\tMOVLW 0xff\n"
            for i in range(8):
                output += "\tMOVWF MATRIX" + str(i) + "\n"
        elif is_row_direction_slide != None or is_no_slide != None:
            # MATRIXの初期値に0を代入
            for i in range(8):
                output += "\tCLRF MATRIX" + str(i) + "\n"
        # OFFSETの初期値を設定
        output += "\t; OFFSETの初期値を設定\n"
        output += "\tCLRF OFFSET_H\n"
        output += "\tCLRF OFFSET_L\n"
        # MODEの初期値を設定
        output += "\t; MODEの初期値を設定\n"
        output += "\tCLRF MODE\n"
        # メインループに飛ぶ
        output += "\t; メインループに飛ぶ\n"
        output += "\tGOTO LOOP\n"
        output += "\n"
        self.__output += output
    def __generateMainLoop(self,
                           led_matrix : list[LEDMatrix], 
                           is_row_direction_slide = None,
                           is_column_direction_slide = None,
                           is_no_slide = None):
        output = "; メインループ\n"
        output += "LOOP\n"
        output += "\t; MODEを更新\n"
        output += "\tCALL UPDATE_MODE\n"
        output += "\t; 文字データを読み込む\n"
        output += "\tCALL LOAD\n"
        loop_cnt = self.__one_flame_us // (8 * self.__led_delay_us)
        output += "\t; 描画更新周期を" + str(self.__one_flame_us / 1e6) + "[s]にするための遅延処理\n"
        output += "\tMOVLW D'" + str(loop_cnt) + "'\n"
        output += "\tMOVWF LOOP_CNT\n"
        output += "LOOP_JUMP0\n"
        output += "\tCALL LEDMATRIX\n"
        output += "\tDECFSZ LOOP_CNT\n"
        output += "\tGOTO LOOP_JUMP0\n"
        output += "\t; メインループに戻る\n"
        output += "\tGOTO LOOP\n"
        output += "\n"
        self.__output += output

    def __generateUpdateMode(self,
                             led_matrix : list[LEDMatrix], 
                             is_row_direction_slide = None,
                             is_column_direction_slide = None,
                             is_no_slide = None):
        output = "; スイッチが押されたら描画する文字を変更するサブルーチン\n"
        output += "UPDATE_MODE\n"
        # スイッチが押されていなかった場合はRETURN
        output += "\t; スイッチが押されているかを確認\n"
        output += "\tBTFSC PORTE, 3\n"
        output += "\tRETURN\n"
        # MATRIXを初期値にする
        output += "\t; MATRIXを初期値にする\n"
        if is_column_direction_slide != None:
            # MATRIXの初期値に255を代入
            output += "\tMOVLW 0xff\n"
            for i in range(8):
                output += "\tMOVWF MATRIX" + str(i) + "\n"
        elif is_row_direction_slide != None or is_no_slide != None:
            # MATRIXの初期値に0を代入
            for i in range(8):
                output += "\tCLRF MATRIX" + str(i) + "\n"
        # LEDを消灯させる
        # FSR0に過去の値が残った状態で呼び出しているが問題ない
        output += "\t; LEDマトリクスを消灯させる\n"
        output += "\tCALL LEDMATRIX\n"
        # スイッチが離されるまで待機
        output += "\t; スイッチが離されるまで待機\n"
        output += "UPDATE_MODE_JUMP_WAIT\n"
        output += "\tBTFSS PORTE, 3\n"
        output += "\tGOTO UPDATE_MODE_JUMP_WAIT\n"
        # OFFSETをクリア
        output += "\t; OFFSETをクリア\n"
        output += "\tCLRF OFFSET_L\n"
        output += "\tCLRF OFFSET_H\n"
        # 次のモードに移行する
        output += "\t; 次のモードに移行する\n"
        output += "\t; 計算GOTO\n"
        output += "\tMOVF MODE, W\n"
        output += "\tBRW\n"
        for i in range(len(self.__data_size)):
            output += "\tGOTO UPDATE_MODE_JUMP_" + str(i) + "\n"

        for i in range(len(self.__data_size)):
            output += "UPDATE_MODE_JUMP_" + str(i) + "\n"
            if i != len(self.__data_size) - 1:
                output += "\tINCF MODE\n"
                output += "\tMOVLW LOW LEDMATRIX_DATA" + str(i+1) + "\n"
                output += "\tMOVWF FSR0L\n"
                output += "\tMOVLW HIGH LEDMATRIX_DATA" + str(i+1) + "\n"
                output += "\tMOVWF FSR0H\n"
                output += "\tRETURN\n"
            else:
                output += "\tCLRF MODE\n"
                output += "\tMOVLW LOW LEDMATRIX_DATA0\n"
                output += "\tMOVWF FSR0L\n"
                output += "\tMOVLW HIGH LEDMATRIX_DATA0\n"
                output += "\tMOVWF FSR0H\n"
                output += "\tRETURN\n"
        output += "\n"
        self.__output += output
    def __generateLoadData(self,
                           led_matrix : list[LEDMatrix], 
                           is_row_direction_slide = None,
                           is_column_direction_slide = None,
                           is_no_slide = None):
        output = "; 文字データを読み込むサブルーチン\n"
        output += "LOAD\n"
        if is_row_direction_slide != None or is_column_direction_slide != None:
            # データをシフト
            output += "\t; データをシフト\n"
            for i in range(1, 8):
                output += "\tMOVF MATRIX" + str(i) + ", W\n"
                output += "\tMOVWF MATRIX" + str(i - 1) + "\n"
            # MATRIX7のデータをFSR0から読む
            output += "\t; MATRIX7のデータをFSR0から読む\n"
            output += "\tMOVIW 0[FSR0]\n"
            output += "\tMOVWF MATRIX7\n"
            output += "\tADDFSR FSR0, 0x01\n"
            # OFFSETを更新
            output += "\t; OFFSETを更新\n"
            output += "\tINCF OFFSET_L, F\n"
            output += "\tBTFSC STATUS, Z\n"
            output += "\tINCF OFFSET_H, F\n"
        elif is_no_slide != None:
            # データをFSR0から読む
            output += "\t; データをFSR0から読む\n"
            for i in range(8):
                output += "\tMOVIW 0[FSR0]\n"
                output += "\tMOVWF MATRIX" + str(i) + "\n"
                output += "\tADDFSR FSR0, 0x01\n"
                # OFFSETを更新
                output += "\tINCF OFFSET_L, F\n"
                output += "\tBTFSC STATUS, Z\n"
                output += "\tINCF OFFSET_H, F\n"
        # OFFSETが文字データの末尾に到達しているかを確認する
        # 計算GOTO
        output += "\t; OFFSETが文字データの末尾に到達しているかを確認する\n"
        output += "\t; 計算GOTO\n"
        output += "\tMOVF MODE, W\n"
        output += "\tBRW\n"
        for i in range(len(self.__data_size)):
            output += "\tGOTO LOAD_JUMP_" + str(i) + "\n"
        for i in range(len(self.__data_size)):
            output += "LOAD_JUMP_" + str(i) + "\n"
            output += "\t; OFFSETが文字データの末尾に到達しているか確認\n"
            output += "\tMOVLW " + format(self.__data_size[i] % 256, "#04x") + "\n"
            output += "\tSUBWF OFFSET_L, W\n"
            output += "\tBTFSS STATUS, Z\n"
            output += "\tRETURN\n"
            output += "\tMOVLW " + format(self.__data_size[i] // 256, "#04x") + "\n"
            output += "\tSUBWF OFFSET_H, W\n"
            output += "\tBTFSS STATUS, Z\n"
            output += "\tRETURN\n"
            # OFFSETを0にする
            output += "\t; OFFSETを0にする\n"
            output += "\tCLRF OFFSET_L\n"
            output += "\tCLRF OFFSET_H\n"
            # FSR0をOFFSETの位置に戻す
            output += "\t; FSR0をOFFSETの位置に戻す\n"
            output += "\tMOVLW LOW LEDMATRIX_DATA" + str(i) + "\n"
            output += "\tMOVWF FSR0L\n"
            output += "\tMOVLW HIGH LEDMATRIX_DATA" + str(i) + "\n"
            output += "\tMOVWF FSR0H\n"
            output += "\tRETURN\n"
        output += "\n"
        self.__output += output

    def __generateLightLEDMatrix(self,
                                 led_matrix : list[LEDMatrix], 
                                 is_row_direction_slide = None,
                                 is_column_direction_slide = None,
                                 is_no_slide = None):
        output = "; LEDマトリクスを描画するサブルーチン\n"
        output += "LEDMATRIX\n"
        for i in range(8):
            if is_column_direction_slide != None:
                output += "\tMOVLW " + format(1 << self.__hardware.column_pin[7 - i], "#04x") + "\n"
                output += "\tMOVWF " + self.__hardware.column_port + "\n"
                output += "\tMOVIW FSR1++\n"
                output += "\tMOVWF " + self.__hardware.row_port + "\n"
            else:
                output += "\tMOVIW FSR1++\n"
                output += "\tMOVWF " + self.__hardware.column_port + "\n"
                output += "\tMOVLW " + format(255 - (1 << self.__hardware.row_pin[i]), "#04x") + "\n"
                output += "\tMOVWF " + self.__hardware.row_port + "\n"
            output += "\tCALL LED_DELAY\n"
        # FSR1を0x70に戻す
        "\t; FSR1を0x70に戻す\n"
        output += "\tMOVLW 0x70\n"
        output += "\tMOVWF FSR1L\n"
        output += "\tRETURN\n"
        delay = PICCodeGenerator_Delay(self.__one_cycle_ns, label_name="LED_DELAY_JUMP")
        delay_str = delay.generateDelay(self.__led_delay_us, "us", "LED_DELAY")
        if delay_str == ";Generate Failed\n":
            Exception("delay generate error")
            return
        self.__output += output
        self.__output += "\n; 1.25[ms]のdelay\n"
        self.__output += delay_str

    def generate(self,
                 view_str : list[str],
                 led_matrix : list[LEDMatrix], 
                 is_row_direction_slide = None,
                 is_column_direction_slide = None,
                 is_no_slide = None):
        for i in range(len(led_matrix)):
            mat = led_matrix[i].get()
            if len(mat) % 8 != 0 or len(mat[0]) % 8 != 0:
                print("led matrix error")
                raise Exception("led matrix error")
        flag = 0
        if is_row_direction_slide != None:
            flag += 1
        if is_column_direction_slide != None:
            flag += 1
        if is_no_slide != None:
            flag += 1
        if flag != 1:
            raise Exception("argument error")

        self.__output = ""
        self.__generateConfig(led_matrix, is_row_direction_slide, 
                              is_column_direction_slide, is_no_slide)
        self.__generateInitialize(led_matrix, is_row_direction_slide, 
                                  is_column_direction_slide, is_no_slide)
        self.__generateMainLoop(led_matrix, is_row_direction_slide, 
                                is_column_direction_slide, is_no_slide)
        self.__generateMatrixData(view_str, led_matrix, is_row_direction_slide, 
                                  is_column_direction_slide, is_no_slide)
        self.__generateUpdateMode(led_matrix, is_row_direction_slide, 
                                  is_column_direction_slide, is_no_slide)
        self.__generateLoadData(led_matrix, is_row_direction_slide, 
                                is_column_direction_slide, is_no_slide)
        self.__generateLightLEDMatrix(led_matrix, is_row_direction_slide, 
                                      is_column_direction_slide, is_no_slide)
        # 末尾にENDを追加
        self.__output += "\nEND\n"

    def getHardwareInformation(is_suehiro = None, is_saito = None):
        if is_suehiro != None:
            h = HardwareInformation("PORTA",
                                    [0,6,1,3,5,2,7,4],
                                    "PORTC",
                                    [0,1,2,3,4,5,6,7])
            return h
        elif is_saito != None:
            h = HardwareInformation("PORTA",
                                    [0,6,1,4,5,2,7,3],
                                    "PORTC",
                                    [0,1,2,3,4,5,6,7])
            return h
        else:
            raise Exception("argument error")
    def getOutput(self):
        return self.__output
