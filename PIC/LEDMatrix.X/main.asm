LIST P=PIC16F1827
#include<p16f1827.inc>
;__CONFIG _FOSC_INTOSC & _WDTE_OFF & _PWRTE_ON & _MCLRE_OFF & _CP_OFF & _CPD_OFF & _BOREN_OFF & _IESO_OFF & _FCMEN_OFF
__CONFIG    _CONFIG1, _FOSC_INTOSC & _WDTE_OFF & _PWRTE_ON & _MCLRE_OFF & _CP_OFF & _CPD_OFF & _BOREN_OFF & _CLKOUTEN_OFF & _IESO_OFF & _FCMEN_OFF  
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
LOOP					
	GOTO 	LOOP			

END					