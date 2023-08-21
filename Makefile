MP_AS="C:\Program Files (x86)\Microchip\MPLABX\v5.00\mpasmx\mpasmx.exe"
MP_LD="C:\Program Files (x86)\Microchip\MPLABX\v5.00\mpasmx\mplink.exe"
PROJECT_NAME=LEDMATRIX
ASM=./asm/main.asm
BOARD=16f1938

${BUILDDIR}/main.o: $(ASM)
# コマンドの最初に@をつけるとコマンドの内容が表示されなくなる
	@rm -rf build
	@mkdir build -p
# -qオプションでエラーがでなくなる
	@${MP_AS} -q -p$(BOARD) -l"./build/main.lst" -e"./build/main.err" -o"./build/main.o" "$(ASM)"
	@${MP_LD} -q -p$(BOARD) -m"./build/$(PROJECT_NAME).map" -o"./build/$(PROJECT_NAME).hex" "./build/main.o"