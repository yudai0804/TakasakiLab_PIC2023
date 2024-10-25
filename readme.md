# 概要
![pic-animation](https://github.com/yudai0804/TakasakiLab_PIC2023/assets/41527277/011d3b98-828a-40da-93be-2f485b1a4756)  

LEDマトリクスに好きな文字を表示させることができ、マイコンは[PIC16F1938](http://ww1.microchip.com/downloads/jp/DeviceDoc/41574A_JP.pdf)、言語はアセンブラを使用しています。  
表示させたい文字を入力すると、ソースコードをPythonで自動生成、コンパイルおよび書き込みまでを自動で行うのが特徴です。    
[自動生成されるソースコード例](https://github.com/yudai0804/TakasakiLab_PIC2023/blob/master/doc/example.asm)

![pic-change-animation](https://github.com/yudai0804/TakasakiLab_PIC2023/assets/41527277/ac24fd5d-c820-4d84-a660-ff61df089946)

右下のボタンを押すことで表示する文字を変えることもできます。  

LEDマトリクスに表示する文字は8x8フォントの[美咲フォント](https://littlelimit.net/misaki.htm)を使用しています。  
ひらがな、カタカナ、漢字(JIS 第一・第二水準)、記号が表示可能です。

# Command
```
sh run.sh [Option]
```
or
```
./run.sh [Option]
```
## Option
```
options:
  -h, --help            show this help message and exit
  --model {1,2}       型式を選択してください 1:末廣，2:齊藤
  --pattern_number {1,2,3,4,5}
                        表示したいパターン数を入力してください
  --mode {1,2,3}        1:横にスライド，2:縦にスライド，3:スライドしない
```
オプションの詳細はPython/src/main.pyを参照してください。  
オプションがない場合は対話形式で必要なパラメータが質問されるので、それに答える形になります。  
LEDマトリクスの基板は2種類存在しているため、オプションで型式を指定できるようにしています。  

# Environment
動作確認済み環境
- Windows10、11、Debian12、Ubuntu22
- Python3.11
- MPLAB 5.35
- Oracle JRE 8
- make

Dockerにも対応しています。  
Dockerを使える環境であれば、Dockerを使うのが一番楽だと思います。

## 注意事項
- MPLABのバージョンは必ず5.35以下にしてください。5.35よりはPICのアセンブラ(MPASM)が付属していないからです。特に理由がなければ、5.35を使用することを強く推奨します。
- Javaの実行環境(JRE)にはOracle JREとOpenJRE(OpenJDK)の2種類がありますが、前者でしか動作確認を行っていません。
- Java 8を使用しているため、将来的に動かなくなる可能性が非常に高いです。
- パスが異なる場合は、必要に応じてMakefileや環境変数を変更してください。

## Setup(Windows)
### Python、make、Git Bashをインストール
Python、make、Git Bashは各自好きな方法でインストールしてください  

scoopの場合

scoopをインストール(インストール済みであれば不要)  
PowerShellで以下のコマンドを実行
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```
Python make git bashをインストール
```
scoop install git python make
```

### MPLABをインストール  
MPLAB 5.35のインストーラーをリンクから取得、実行
https://www.microchip.com/en-us/tools-resources/archives/mplab-ecosystem

### Oracle JREをインストール
https://www.java.com/ja/download/windows_manual.jsp

### clone
Git Bashを起動したらcloneする。  
cloneするディレクトリはどこでも大丈夫です。
```
git clone https://github.com/yudai0804/TakasakiLab_PIC2023.git
```
```
cd TakasakiLab_PIC2023
```
実行
```
bash run.sh
```

### Windowsで利用可能な文字について
Windowsの文字コードがShift JISであることが原因で、プログラムの都合上、一部記号(☆、♡)などが使用できないことがあります。その場合、Windowsの文字コードをShift JISからUTF-8に変更してください。文字コードの変更を行うと、他のアプリケーションに文字化け等の影響を与える可能性があるので、注意してください。

文字コード変更のやり方は自分で調べてください...  

## Setup(Linux)
### MPLABをインストール
インストールリンク
https://www.microchip.com/en-us/tools-resources/archives/mplab-ecosystem
```
dpkg --add-architecture i386
apt-get update && apt-get install -y libc6:i386 libx11-6:i386 libxext6:i386 libstdc++6:i386 libexpat1:i386
```
```
tar -xvf MPLABX-v5.35-linux-installer.tar
sudo ./MPLABX-v5.35-linux-installer.sh
```
参考:https://developerhelp.microchip.com/xwiki/bin/view/software-tools/ides/x/archive/linux/

### Oracle JREをインストール
https://www.java.com/ja/download/
```
tar zxvf jre-8u73-linux-x64.tar.gz
```
73の部分はダウンロードしたもののバージョンに合わせてください。

環境変数の追加

Makefileで`IPECMD_JAVA`という環境変数を使用するため、ダウンロードしたOracle JREを環境変数に設定してください。  
例(.bashrc)
```
export IPECMD_JAVA="$HOME/jre1.8.0_431/bin/java"
```
```
source ~/.bashrc
```

### clone
Git Bashを起動したらcloneする。  
cloneするディレクトリはどこでも大丈夫です。
```
git clone https://github.com/yudai0804/TakasakiLab_PIC2023.git
```
```
cd TakasakiLab_PIC2023
```
実行
```
bash run.sh
```

## Setup(Docker)
実行(推奨)
```
docker run -it --privileged -v .:/app -v /dev/bus/usb:/dev/bus/usb yudai0804/takasakilab_pic2023:latest bash run.sh
```

### 自分でbuildしたい人向け

build
```
docker build -t takasakilab_pic2023 .
```

buildしたものを実行
```
docker run -it --privileged -v .:/app -v /dev/bus/usb:/dev/bus/usb takasakilab_pic2023 bash run.sh
```

# Makefile
PICのコンパイル、書き込みについては、以下のリンクのmakefileを使用しています。  
https://github.com/yudai0804/pic-makefile-template

# License
MIT License
