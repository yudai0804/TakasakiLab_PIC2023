2023年度高専祭で展示するPIC用リポジトリ

## フォント
LEDマトリクスのフォントは[美咲フォント](https://littlelimit.net/misaki.htm)を使用(misaki_gothic_2nd)  
ファイル形式はBDF形式のものを使用している．  

# requirements
- Windows10,Windows11
- MPLAB 5.00
- java
  - jre-1.8
  - ダウンロードリンク:https://www.java.com/ja/download/
  - javaの種類によっては動かないものがあるので注意
- shell(windowsの場合はgit bash必須)

## コマンド
```
sh run.sh オプション
```

### オプション
```
options:
  -h, --help            show this help message and exit
  --model {0,1,2}       型式を選択してください 1:末廣，2:齊藤
  --pattern_number {1,2}
                        表示したいパターン数を入力してください
  --mode {1,2,3}        1:横にスライド，2:縦にスライド，3:スライドしない
```

[makefileの詳細](https://github.com/yudai0804/pic-makefile-template)

## 使うPIC
[PIC16F1938](http://ww1.microchip.com/downloads/jp/DeviceDoc/41574A_JP.pdf)
