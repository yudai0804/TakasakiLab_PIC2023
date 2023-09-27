LIST P=PIC16F1938
#include<p16f1938.inc>
__CONFIG	_CONFIG1, _FOSC_INTOSC & _WDTE_OFF & _PWRTE_ON & _MCLRE_OFF & _CP_OFF & _CPD_OFF & _BOREN_OFF & _CLKOUTEN_OFF & _IESO_OFF & _FCMEN_OFF
__CONFIG	_CONFIG2, _WRT_OFF & _VCAPEN_OFF & _PLLEN_OFF & _STVREN_OFF & _BORV_LO & _LVP_ON
MATRIX0	EQU	0x70
MATRIX1	EQU	0x71
MATRIX2	EQU	0x72
MATRIX3	EQU	0x73
MATRIX4	EQU	0x74
MATRIX5	EQU	0x75
MATRIX6	EQU	0x76
MATRIX7	EQU	0x77
CNT0	EQU	0x78
CNT1	EQU	0x79
CNT2	EQU	0x7a
LOOP_CNT	EQU	0x7b
SIZE_H	EQU	0x7c
SIZE_L	EQU	0x7d
ORG 0x0000
	BSF BSR, BSR0
	MOVLW B'01101000'
	MOVWF OSCCON
	CLRF TRISC
	CLRF TRISA
	BCF BSR, BSR0
	CLRF PORTC
	CLRF PORTA
	MOVLW HIGH LEDMATRIX_DATA
	MOVWF FSR0H
	MOVLW LOW LEDMATRIX_DATA
	MOVWF FSR0L
	CLRF FSR1H
	MOVLW 0x70
	MOVWF FSR1L
	CLRF MATRIX0
	CLRF MATRIX1
	CLRF MATRIX2
	CLRF MATRIX3
	CLRF MATRIX4
	CLRF MATRIX5
	CLRF MATRIX6
	CLRF MATRIX7
	CLRF SIZE_H
	CLRF SIZE_L
	GOTO LOOP
LOOP
	CALL LOAD
	MOVLW D'12'
	MOVWF LOOP_CNT
LOOP_JUMP0
	CALL LEDMATRIX
	DECFSZ LOOP_CNT
	GOTO LOOP_JUMP0
	GOTO LOOP
LEDMATRIX_DATA
	DT 0x0,0x0,0x0,0x0
	DT 0x0,0x0,0x0,0x0
	DT 0x24,0x2a,0x29,0x29
	DT 0x75,0x2c,0x20,0x0
	DT 0x1,0x6,0x18,0x68
	DT 0x6,0x1,0x6,0x0
	DT 0x8,0x2a,0x2d,0x69
	DT 0x39,0x6d,0x8,0x0
	DT 0x2,0x25,0x21,0x21
	DT 0x21,0x21,0x1,0x0
	DT 0x8,0x50,0x51,0x51
	DT 0x52,0x52,0xc,0x0
	DT 0x10,0x7e,0x11,0x11
	DT 0x15,0x7d,0x10,0x0
	DT 0x1,0x6,0x18,0x68
	DT 0x6,0x1,0x6,0x0
	DT 0x4,0x18,0x20,0x10
	DT 0x8,0x4,0x2,0x0
	DT 0x2,0x5,0x5,0x7e
	DT 0x24,0x22,0x1,0x0
	DT 0x8,0x50,0x51,0x51
	DT 0x52,0x52,0xc,0x0
	DT 0x2,0x25,0x21,0x21
	DT 0x21,0x21,0x1,0x0
	DT 0x8,0x48,0x5a,0x6d
	DT 0x49,0x49,0x8,0x0
	DT 0x0,0x0,0x0,0x0
	DT 0x0,0x0,0x0,0x0
LOAD
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
	MOVIW 0[FSR0]
	MOVWF MATRIX7
	ADDFSR FSR0, 0x01
	INCF SIZE_L, F
	BTFSC STATUS, Z
	INCF SIZE_H, F
	MOVLW 0x0
	SUBWF SIZE_H, W
	BTFSS STATUS, Z
	RETURN
	MOVLW 0x70
	SUBWF SIZE_L, W
	BTFSS STATUS, Z
	RETURN
	CLRF SIZE_H
	CLRF SIZE_L
	MOVLW HIGH LEDMATRIX_DATA
	MOVWF FSR0H
	MOVLW LOW LEDMATRIX_DATA
	MOVWF FSR0L
	RETURN
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
	MOVLW 0xef
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
	MOVLW 0xf7
	MOVWF PORTA
	CALL LED_DELAY
	MOVLW 0x70
	MOVWF FSR1L
	RETURN
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
