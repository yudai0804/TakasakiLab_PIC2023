# ターゲット名
TARGET := main
# ヘックスファイル名
HEX := LEDMATRIX
# ボード名
BOARD := 16F1938
# ソースコードのあるディレクトリ
SRC_DIR := asm
BUILD_DIR := build
# javaのパス
JAVA :=
#アセンブラのコンパイラのパス
MP_AS :=
# リンカのパス
MP_LD :=
# ipecmd(書き込みツール)のパス(
MP_IPE :=

# OSに応じて，パスを設定
# インストール先のパスなどは各自の環境に合わせてください
ifeq ($(OS),Windows_NT)
# Windowsの場合
	MP_AS := "C:\Program Files (x86)\Microchip\MPLABX\v5.00\mpasmx\mpasmx.exe"
	MP_LD := "C:\Program Files (x86)\Microchip\MPLABX\v5.00\mpasmx\mplink.exe"
	MP_IPE := "C:\Program Files (x86)\Microchip\MPLABX\v5.00\mplab_platform\mplab_ipe\ipecmd.jar"
	JAVA := java
else
# linux
	MP_AS := "/opt/microchip/mplabx/v5.00/mpasmx/mpasmx"
	MP_LD :="/opt/microchip/mplabx/v5.00/mpasmx/mplink"
	MP_IPE := "/opt/microchip/mplabx/v6.00/mplab_platform/mplab_ipe/ipecmd.jar"
	JAVA := /home/yudai/jre1.8.0_381/bin/java
endif

# PICKIT3の場合はPPK3,PICKIT4の場合はPPK4
# PICKIT := PPK3
PICKIT := PPK4

# 出力電圧
VOLTAGE := 4.5

.PHONY: clean all write

$(BUILD_DIR)/$(HEX).hex: $(SRC_DIR)/$(TARGET).asm
	mkdir $(BUILD_DIR) -p
# -qオプションでエラーがでなくなる
	$(MP_AS) -q -p$(BOARD) -l"./$(BUILD_DIR)/$(TARGET).lst" -e"./$(BUILD_DIR)/$(TARGET).err" -o"./$(BUILD_DIR)/$(TARGET).o" "$(SRC_DIR)/$(TARGET).asm"
	$(MP_LD) -q -p$(BOARD) -m"./$(BUILD_DIR)/$(HEX).map" -o"./$(BUILD_DIR)/$(HEX).hex" "./$(BUILD_DIR)/$(TARGET).o"

all: clean build write

clean: 
	rm -rf $(BUILD_DIR)

build: $(BUILD_DIR)/$(HEX).hex

write:
# -OLは書き込み終了後にリセットをかけるオプション
	$(JAVA) -jar $(MP_IPE) -T$(PICKIT) -P$(BOARD) -F./$(BUILD_DIR)/$(HEX).hex -M -W$(VOLTAGE) -OL 
# 書き込み時に生成されるログファイルを削除
	rm -f log.*
	rm -f MPLABXLog.xml*
