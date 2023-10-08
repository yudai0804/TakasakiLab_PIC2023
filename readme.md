# 概要
![pic-animation](https://github.com/yudai0804/TakasakiLab_PIC2023/assets/41527277/011d3b98-828a-40da-93be-2f485b1a4756)  

2023年度の高専祭で展示をした作品です。　　
LEDマトリクスに好きな文字を表示させることができ、マイコンは[PIC16F1938](http://ww1.microchip.com/downloads/jp/DeviceDoc/41574A_JP.pdf)、言語はアセンブラを使用しています。  
表示したい文字を入力すると、ソースコードをPythonで自動生成、コンパイルおよび書き込みまでを自動で行うのが特徴です。    
[自動生成されるソースコード例](https://github.com/yudai0804/TakasakiLab_PIC2023/blob/master/doc/example.asm)

![pic-change-animation](https://github.com/yudai0804/TakasakiLab_PIC2023/assets/41527277/ac24fd5d-c820-4d84-a660-ff61df089946)

右下のボタンを押すことで表示する文字を変えることもできます。  

LEDマトリクスに表示する文字は8x8フォントの[美咲フォント](https://littlelimit.net/misaki.htm)を使用しています。  
ひらがな、カタカナ、漢字(JIS 第一・第二水準)、記号が表示可能です。

# requirements
- Windows10,Windows11 or Ubuntu 22.04
- Python3
- MPLAB 5.00
- java(PICの書き込み用)
  - jre-1.8
  - ダウンロードリンク:https://www.java.com/ja/download/
  - javaの種類によっては動かないものがあるので注意
- shell(windowsの場合はgit bash必須)

# コマンド
```
sh run.sh オプション
```

## オプション
```
options:
  -h, --help            show this help message and exit
  --model {1,2}       型式を選択してください 1:末廣，2:齊藤
  --pattern_number {1,2,3,4,5}
                        表示したいパターン数を入力してください
  --mode {1,2,3}        1:横にスライド，2:縦にスライド，3:スライドしない
```
オプションの詳細はPython/src/main.pyを参照してください。  
LEDマトリクスの基板は2種類存在しているため、オプションで型式を指定できるようにしています。  

# makefile
PICのコンパイル、書き込みについては、以下のリンクのmakefileを使用しています。  
https://github.com/yudai0804/pic-makefile-template