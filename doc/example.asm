;GitHub:https://github.com/yudai0804/TakasakiLab_PIC2023
LIST P=PIC16F1938
#include<p16f1938.inc>

__CONFIG	_CONFIG1, _FOSC_INTOSC & _WDTE_OFF & _PWRTE_ON & _MCLRE_OFF & _CP_OFF & _CPD_OFF & _BOREN_OFF & _CLKOUTEN_OFF & _IESO_OFF & _FCMEN_OFF
__CONFIG	_CONFIG2, _WRT_OFF & _VCAPEN_OFF & _PLLEN_OFF & _STVREN_OFF & _BORV_LO & _LVP_OFF

; LEDマトリクス描画用の一時変数
MATRIX0	EQU	0x70
MATRIX1	EQU	0x71
MATRIX2	EQU	0x72
MATRIX3	EQU	0x73
MATRIX4	EQU	0x74
MATRIX5	EQU	0x75
MATRIX6	EQU	0x76
MATRIX7	EQU	0x77
; delay生成用変数
CNT0	EQU	0x78
CNT1	EQU	0x79
CNT2	EQU	0x7a
; 描画更新周期用変数
LOOP_CNT	EQU	0x7b
; 文字データを読み出す際のオフセット用変数
OFFSET_L	EQU	0x7c
OFFSET_H	EQU	0x7d
; 現在のモードを保持する変数
MODE	EQU	0x7e

ORG 0x0000
	; OSCCONレジスタを操作して、制御周期を4MHzに設定
	; バンク1に切り替え
	BSF BSR, BSR0
	MOVLW B'01101000'
	MOVWF OSCCON
	; PORTA、PORTCを出力に設定
	CLRF TRISC
	CLRF TRISA
	; バンク0に切り替え
	BCF BSR, BSR0
	; 出力を0にする
	CLRF PORTC
	CLRF PORTA
	; FSR0レジスタをLEDMATRIX_DATA0番地に合わせる
	MOVLW LOW LEDMATRIX_DATA0
	MOVWF FSR0L
	MOVLW HIGH LEDMATRIX_DATA0
	MOVWF FSR0H
	; FSR1レジスタを0x70番地に合わせる
	CLRF FSR1H
	MOVLW 0x70
	MOVWF FSR1L
	; MATRIXを初期値に設定
	CLRF MATRIX0
	CLRF MATRIX1
	CLRF MATRIX2
	CLRF MATRIX3
	CLRF MATRIX4
	CLRF MATRIX5
	CLRF MATRIX6
	CLRF MATRIX7
	; OFFSETの初期値を設定
	CLRF OFFSET_H
	CLRF OFFSET_L
	; MODEの初期値を設定
	CLRF MODE
	; メインループに飛ぶ
	GOTO LOOP

; メインループ
LOOP
	; MODEを更新
	CALL UPDATE_MODE
	; 文字データを読み込む
	CALL LOAD
	; 描画更新周期を0.12[s]にするための遅延処理
	MOVLW D'12'
	MOVWF LOOP_CNT
LOOP_JUMP0
	CALL LEDMATRIX
	DECFSZ LOOP_CNT
	GOTO LOOP_JUMP0
	; メインループに戻る
	GOTO LOOP

; 文字列「さんぎこうせんへようこそ」のデータ
LEDMATRIX_DATA0
	DT 0x00,0x00,0x00,0x00
	DT 0x00,0x00,0x00,0x00
	DT 0x24,0x2a,0x29,0x29
	DT 0x75,0x2c,0x20,0x00
	DT 0x01,0x06,0x18,0x68
	DT 0x06,0x01,0x06,0x00
	DT 0x08,0x2a,0x2d,0x69
	DT 0x39,0x6d,0x08,0x00
	DT 0x02,0x25,0x21,0x21
	DT 0x21,0x21,0x01,0x00
	DT 0x08,0x50,0x51,0x51
	DT 0x52,0x52,0x0c,0x00
	DT 0x10,0x7e,0x11,0x11
	DT 0x15,0x7d,0x10,0x00
	DT 0x01,0x06,0x18,0x68
	DT 0x06,0x01,0x06,0x00
	DT 0x04,0x18,0x20,0x10
	DT 0x08,0x04,0x02,0x00
	DT 0x02,0x05,0x05,0x7e
	DT 0x24,0x22,0x01,0x00
	DT 0x08,0x50,0x51,0x51
	DT 0x52,0x52,0x0c,0x00
	DT 0x02,0x25,0x21,0x21
	DT 0x21,0x21,0x01,0x00
	DT 0x08,0x48,0x5a,0x6d
	DT 0x49,0x49,0x08,0x00
	DT 0x00,0x00,0x00,0x00
	DT 0x00,0x00,0x00,0x00

; 文字列「たかさきけんへようこそ」のデータ
LEDMATRIX_DATA1
	DT 0x00,0x00,0x00,0x00
	DT 0x00,0x00,0x00,0x00
	DT 0x23,0x2c,0x70,0x22
	DT 0x15,0x11,0x11,0x00
	DT 0x23,0x2c,0x71,0x21
	DT 0x1e,0x20,0x18,0x00
	DT 0x24,0x2a,0x29,0x29
	DT 0x75,0x2c,0x20,0x00
	DT 0x08,0x2a,0x2d,0x69
	DT 0x39,0x2d,0x08,0x00
	DT 0x7e,0x00,0x20,0x21
	DT 0x7e,0x20,0x20,0x00
	DT 0x01,0x06,0x18,0x68
	DT 0x06,0x01,0x06,0x00
	DT 0x04,0x18,0x20,0x10
	DT 0x08,0x04,0x02,0x00
	DT 0x02,0x05,0x05,0x7e
	DT 0x24,0x22,0x01,0x00
	DT 0x08,0x50,0x51,0x51
	DT 0x52,0x52,0x0c,0x00
	DT 0x02,0x25,0x21,0x21
	DT 0x21,0x21,0x01,0x00
	DT 0x08,0x48,0x5a,0x6d
	DT 0x49,0x49,0x08,0x00
	DT 0x00,0x00,0x00,0x00
	DT 0x00,0x00,0x00,0x00

; 文字列「こうせんさい２０２３」のデータ
LEDMATRIX_DATA2
	DT 0x00,0x00,0x00,0x00
	DT 0x00,0x00,0x00,0x00
	DT 0x02,0x25,0x21,0x21
	DT 0x21,0x21,0x01,0x00
	DT 0x08,0x50,0x51,0x51
	DT 0x52,0x52,0x0c,0x00
	DT 0x10,0x7e,0x11,0x11
	DT 0x15,0x7d,0x10,0x00
	DT 0x01,0x06,0x18,0x68
	DT 0x06,0x01,0x06,0x00
	DT 0x24,0x2a,0x29,0x29
	DT 0x75,0x2c,0x20,0x00
	DT 0x3e,0x01,0x02,0x00
	DT 0x00,0x20,0x1c,0x00
	DT 0x00,0x23,0x45,0x45
	DT 0x49,0x49,0x31,0x00
	DT 0x00,0x3e,0x45,0x49
	DT 0x49,0x51,0x3e,0x00
	DT 0x00,0x23,0x45,0x45
	DT 0x49,0x49,0x31,0x00
	DT 0x00,0x22,0x41,0x49
	DT 0x49,0x49,0x36,0x00
	DT 0x00,0x00,0x00,0x00
	DT 0x00,0x00,0x00,0x00

; スイッチが押されたら描画する文字を変更するサブルーチン
UPDATE_MODE
	; スイッチが押されているかを確認
	BTFSC PORTE, 3
	RETURN
	; MATRIXを初期値にする
	CLRF MATRIX0
	CLRF MATRIX1
	CLRF MATRIX2
	CLRF MATRIX3
	CLRF MATRIX4
	CLRF MATRIX5
	CLRF MATRIX6
	CLRF MATRIX7
	; LEDマトリクスを消灯させる
	CALL LEDMATRIX
	; スイッチが離されるまで待機
UPDATE_MODE_JUMP_WAIT
	BTFSS PORTE, 3
	GOTO UPDATE_MODE_JUMP_WAIT
	; OFFSETをクリア
	CLRF OFFSET_L
	CLRF OFFSET_H
	; 次のモードに移行する
	; 計算GOTO
	MOVF MODE, W
	BRW
	GOTO UPDATE_MODE_JUMP_0
	GOTO UPDATE_MODE_JUMP_1
	GOTO UPDATE_MODE_JUMP_2
UPDATE_MODE_JUMP_0
	INCF MODE
	MOVLW LOW LEDMATRIX_DATA1
	MOVWF FSR0L
	MOVLW HIGH LEDMATRIX_DATA1
	MOVWF FSR0H
	RETURN
UPDATE_MODE_JUMP_1
	INCF MODE
	MOVLW LOW LEDMATRIX_DATA2
	MOVWF FSR0L
	MOVLW HIGH LEDMATRIX_DATA2
	MOVWF FSR0H
	RETURN
UPDATE_MODE_JUMP_2
	CLRF MODE
	MOVLW LOW LEDMATRIX_DATA0
	MOVWF FSR0L
	MOVLW HIGH LEDMATRIX_DATA0
	MOVWF FSR0H
	RETURN

; 文字データを読み込むサブルーチン
LOAD
	; データをシフト
	MOVF MATRIX1, W
	MOVWF MATRIX0
	MOVF MATRIX2, W
	MOVWF MATRIX1
	MOVF MATRIX3, W
	MOVWF MATRIX2
	MOVF MATRIX4, W
	MOVWF MATRIX3
	MOVF MATRIX5, W
	MOVWF MATRIX4
	MOVF MATRIX6, W
	MOVWF MATRIX5
	MOVF MATRIX7, W
	MOVWF MATRIX6
	; MATRIX7のデータをFSR0から読む
	MOVIW 0[FSR0]
	MOVWF MATRIX7
	ADDFSR FSR0, 0x01
	; OFFSETを更新
	INCF OFFSET_L, F
	BTFSC STATUS, Z
	INCF OFFSET_H, F
	; OFFSETが文字データの末尾に到達しているかを確認する
	; 計算GOTO
	MOVF MODE, W
	BRW
	GOTO LOAD_JUMP_0
	GOTO LOAD_JUMP_1
	GOTO LOAD_JUMP_2
LOAD_JUMP_0
	; OFFSETが文字データの末尾に到達しているか確認
	MOVLW 0x70
	SUBWF OFFSET_L, W
	BTFSS STATUS, Z
	RETURN
	MOVLW 0x00
	SUBWF OFFSET_H, W
	BTFSS STATUS, Z
	RETURN
	; OFFSETを0にする
	CLRF OFFSET_L
	CLRF OFFSET_H
	; FSR0をOFFSETの位置に戻す
	MOVLW LOW LEDMATRIX_DATA0
	MOVWF FSR0L
	MOVLW HIGH LEDMATRIX_DATA0
	MOVWF FSR0H
	RETURN
LOAD_JUMP_1
	; OFFSETが文字データの末尾に到達しているか確認
	MOVLW 0x68
	SUBWF OFFSET_L, W
	BTFSS STATUS, Z
	RETURN
	MOVLW 0x00
	SUBWF OFFSET_H, W
	BTFSS STATUS, Z
	RETURN
	; OFFSETを0にする
	CLRF OFFSET_L
	CLRF OFFSET_H
	; FSR0をOFFSETの位置に戻す
	MOVLW LOW LEDMATRIX_DATA1
	MOVWF FSR0L
	MOVLW HIGH LEDMATRIX_DATA1
	MOVWF FSR0H
	RETURN
LOAD_JUMP_2
	; OFFSETが文字データの末尾に到達しているか確認
	MOVLW 0x60
	SUBWF OFFSET_L, W
	BTFSS STATUS, Z
	RETURN
	MOVLW 0x00
	SUBWF OFFSET_H, W
	BTFSS STATUS, Z
	RETURN
	; OFFSETを0にする
	CLRF OFFSET_L
	CLRF OFFSET_H
	; FSR0をOFFSETの位置に戻す
	MOVLW LOW LEDMATRIX_DATA2
	MOVWF FSR0L
	MOVLW HIGH LEDMATRIX_DATA2
	MOVWF FSR0H
	RETURN

; LEDマトリクスを描画するサブルーチン
LEDMATRIX
	MOVIW FSR1++
	MOVWF PORTC
	MOVLW 0xfe
	MOVWF PORTA
	CALL LED_DELAY
	MOVIW FSR1++
	MOVWF PORTC
	MOVLW 0xbf
	MOVWF PORTA
	CALL LED_DELAY
	MOVIW FSR1++
	MOVWF PORTC
	MOVLW 0xfd
	MOVWF PORTA
	CALL LED_DELAY
	MOVIW FSR1++
	MOVWF PORTC
	MOVLW 0xf7
	MOVWF PORTA
	CALL LED_DELAY
	MOVIW FSR1++
	MOVWF PORTC
	MOVLW 0xdf
	MOVWF PORTA
	CALL LED_DELAY
	MOVIW FSR1++
	MOVWF PORTC
	MOVLW 0xfb
	MOVWF PORTA
	CALL LED_DELAY
	MOVIW FSR1++
	MOVWF PORTC
	MOVLW 0x7f
	MOVWF PORTA
	CALL LED_DELAY
	MOVIW FSR1++
	MOVWF PORTC
	MOVLW 0xef
	MOVWF PORTA
	CALL LED_DELAY
	MOVLW 0x70
	MOVWF FSR1L
	RETURN

; 1.25[ms]のdelay
LED_DELAY
	MOVLW D'249'
	MOVWF CNT0
LED_DELAY_JUMP0
	NOP
	NOP
	DECFSZ CNT0, F
	GOTO LED_DELAY_JUMP0
	RETURN

END