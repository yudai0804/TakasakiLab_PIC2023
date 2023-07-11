LIST P=PIC16F1827
#include<p16f1827.inc>
__CONFIG    _CONFIG1, _FOSC_INTOSC & _WDTE_OFF & _PWRTE_ON & _MCLRE_OFF & _CP_OFF & _CPD_OFF & _BOREN_OFF & _CLKOUTEN_OFF & _IESO_OFF & _FCMEN_OFF  
__CONFIG    _CONFIG2, _WRT_OFF & _PLLEN_OFF & _STVREN_OFF & _BORV_LO & _LVP_ON

MATRIX_ROW_0	EQU 0x20
MATRIX_ROW_1	EQU 0x21
MATRIX_ROW_2	EQU 0x22
MATRIX_ROW_3	EQU 0x23
MATRIX_ROW_4	EQU 0x24
MATRIX_ROW_5	EQU 0x25
MATRIX_ROW_6	EQU 0x26
MATRIX_ROW_7	EQU 0x27
DELAY_CNT0	EQU 0x28
DELAY_CNT1	EQU 0x29

ORG	0x0000				
	;バンク1に切り替え
	BSF	BSR, BSR0
	;OSCCONレジスタを操作して、周期を4MHzに変更する
	MOVLW	B'01101000'
	MOVWF	OSCCON
	;TRISAを設定して、PORTA 5以外を出力にする
	MOVLW	B'00100000'
	MOVWF	TRISA
	;TRISBを設定して、PORTBをすべて出力にする
	MOVLW	B'00000000'
	MOVWF	TRISB
	;バンク0に切り替える
	BCF	BSR, BSR0
	;PORTB(アノード)とPORTA(カソード)の出力を0にする
	MOVLW	B'00000000'
	MOVWF	PORTB
	MOVLW	B'11111111'
	MOVWF	PORTA
LOOP					
	
	GOTO 	LOOP			

TEST
	ANDLW	0x0f
	ADDWF	PCL,F
	
	
LIGHT_MATRIX
	;MATRIX_ROW_0は使用していない
	
	;MATRIX_ROW_1
	MOVF	MATRIX_ROW_1, W
	MOVWF	PORTB
	MOVLW	B'01111111'
	MOVWF	PORTA
	CALL	LED_DELAY_JUMP0
	;MATRIX_ROW_2
	MOVF	MATRIX_ROW_2, W
	MOVWF	PORTB
	MOVLW	B'10111111'
	MOVWF	PORTA
	CALL	LED_DELAY_JUMP0
	;MATRIX_ROW_3
	MOVF	MATRIX_ROW_3, W
	MOVWF	PORTB
	MOVLW	B'11101111'
	MOVWF	PORTA
	CALL	LED_DELAY_JUMP0
	;MATRIX_ROW_4
	MOVF	MATRIX_ROW_4, W
	MOVWF	PORTB
	MOVLW	B'11110111'
	MOVWF	PORTA
	CALL	LED_DELAY_JUMP0
	;MATRIX_ROW_5
	MOVF	MATRIX_ROW_5, W
	MOVWF	PORTB
	MOVLW	B'11111011'
	MOVWF	PORTA
	CALL	LED_DELAY_JUMP0
	;MATRIX_ROW_6
	MOVF	MATRIX_ROW_6, W
	MOVWF	PORTB
	MOVLW	B'11111101'
	MOVWF	PORTA
	CALL	LED_DELAY_JUMP0
	;MATRIX_ROW_7
	MOVF	MATRIX_ROW_7, W
	MOVWF	PORTB
	MOVLW	B'11111110'
	MOVWF	PORTA
	CALL	LED_DELAY_JUMP0
	RETURN
LED_DELAY
	MOVLW	0x00
	MOVWF	DELAY_CNT0
LED_DELAY_JUMP0
	DECFSZ	DELAY_CNT0, F
	GOTO	LED_DELAY_JUMP0
	RETURN
TIMER
	MOVLW	0x00
	MOVWF	DELAY_CNT0
TIMER_JUMP0
	MOVLW	0x00
	MOVWF	DELAY_CNT1
TIMER_JUMP1
	DECFSZ	DELAY_CNT0, F
	GOTO	TIMER_JUMP1
	DECFSZ	DELAY_CNT1, F
	GOTO	TIMER_JUMP0
	RETURN
END
