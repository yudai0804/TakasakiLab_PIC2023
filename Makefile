MP_AS="C:\Program Files (x86)\Microchip\MPLABX\v5.00\mpasmx\mpasmx.exe"
MP_PROCESSOR_OPTION=16f1938
TARGET="main"
BUILD="build"

${OBJECTDIR}/main.o: main.asm  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/main.o.d 
	@${RM} ${OBJECTDIR}/main.o 
	@${FIXDEPS} dummy.d -e "${OBJECTDIR}/main.err" $(SILENT) -c ${MP_AS} $(MP_EXTRA_AS_PRE) -q -p$(MP_PROCESSOR_OPTION)  -l\"${OBJECTDIR}/main.lst\" -e\"${OBJECTDIR}/main.err\" $(ASM_OPTIONS)    -o\"${OBJECTDIR}/main.o\" \"main.asm\" 
	@${DEP_GEN} -d "${OBJECTDIR}/main.o"
	@${FIXDEPS} "${OBJECTDIR}/main.o.d" $(SILENT) -rsi ${MP_AS_DIR} -c18 


${BUILD}/main.o: main.asm
	@${MP_AS}