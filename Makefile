TARGET=main
HEX=LEDMATRIX
BOARD=16f1938
MP_AS="C:\Program Files (x86)\Microchip\MPLABX\v5.00\mpasmx\mpasmx.exe"
MP_LD="C:\Program Files (x86)\Microchip\MPLABX\v5.00\mpasmx\mplink.exe"
ASM_DIR=asm
BUILD_DIR=build

$(BUILD_DIR)/$(TARGET).o: $(ASM_DIR)/$(TARGET).asm
# コマンドの最初に@をつけるとコマンドの内容が表示されなくなる
	@mkdir $(BUILD_DIR) -p
# -qオプションでエラーがでなくなる
	@${MP_AS} -q -p$(BOARD) -l"./$(BUILD_DIR)/$(TARGET).lst" -e"./$(BUILD_DIR)/$(TARGET).err" -o"./$(BUILD_DIR)/$(TARGET).o" "$(ASM_DIR)/$(TARGET).asm"
	@${MP_LD} -q -p$(BOARD) -m"./$(BUILD_DIR)/$(HEX).map" -o"./$(BUILD_DIR)/$(HEX).hex" "./$(BUILD_DIR)/$(TARGET).o"

clean:
	rm -rf $(BUILD_DIR)
all:
	make