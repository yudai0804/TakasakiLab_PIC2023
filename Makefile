# ターゲット名
TARGET := main
# ヘックスファイル名
HEX := LEDMATRIX
# ボード名
BOARD := 16F1938
# ソースコードのあるディレクトリ
SRC_DIR := asm
BUILD_DIR := build
IDE_VERSION := 5.35
# javaのパス
JAVA :=
#アセンブラのコンパイラのパス
MP_AS :=
# リンカのパス
MP_LD :=
# ipecmd(書き込みツール)のパス
MP_IPE :=
# OSに応じて，パスを設定
# インストール先のパスなどは各自の環境に合わせてください
# Mac OSはMPLAB v5.35が動かないため、非対応
ifeq ($(OS),Windows_NT)
# Windowsの場合
# これで動く理由はWindows環境にはOSという環境変数が存在しているから
	MP_AS := "C:\Program Files (x86)\Microchip\MPLABX\v$(IDE_VERSION)\mpasmx\mpasmx.exe"
	MP_LD := "C:\Program Files (x86)\Microchip\MPLABX\v$(IDE_VERSION)\mpasmx\mplink.exe"
	MP_IPE := "C:\Program Files (x86)\Microchip\MPLABX\v$(IDE_VERSION)\mplab_platform\mplab_ipe\ipecmd.jar"
	JAVA := java
else ifeq ($(shell uname),Linux)
# Linux
	MP_AS := "/opt/microchip/mplabx/v$(IDE_VERSION)/mpasmx/mpasmx"
	MP_LD := "/opt/microchip/mplabx/v$(IDE_VERSION)/mpasmx/mplink"
	MP_IPE := "/opt/microchip/mplabx/v$(IDE_VERSION)/mplab_platform/mplab_ipe/ipecmd.jar"
	JAVA := $$IPECMD_JAVA
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
	cd $(BUILD_DIR) && $(MP_AS) -q -p$(BOARD) -l"$(TARGET).lst" -e"$(TARGET).err" -o"$(TARGET).o" ../"$(SRC_DIR)/$(TARGET).asm"
	cd $(BUILD_DIR) && $(MP_LD) -q -p$(BOARD) -m"$(HEX).map" -o"$(HEX).hex" "$(TARGET).o"

all: clean build write

clean: 
	rm -rf $(BUILD_DIR)

build: $(BUILD_DIR)/$(HEX).hex

write:
# -OLは書き込み終了後にリセットをかけるオプション
	cd $(BUILD_DIR) && $(JAVA) -jar $(MP_IPE) -T$(PICKIT) -P$(BOARD) -F$(HEX).hex -M -W$(VOLTAGE) -OL 
# 書き込み時に生成されるログファイルを削除
	rm -f $(BUILD_DIR)/log.*
	rm -f $(BUILD_DIR)/MPLABXLog.xml*
