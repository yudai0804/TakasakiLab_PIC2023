class PICCodeGenerator_Delay:
	def __init__(self, one_cycle_ns : int, max_nop = 5, label_name = "JUMP", variable_name = "CNT"):
		self.__one_cycle_ns = one_cycle_ns
		self.__max_nop = max_nop
		self.__label_name = label_name
		self.__variable_name = variable_name
		self.__result = ""
		self.__MAX_NOP = 10000
		self.__MAX_STR_LEN = 10000
	def __delayOneLoop(self, cycle : int, subroutine_name : str):
		# 最適なNOPと繰り返す回数を計算
		nop_sum = self.__MAX_NOP
		tmp = [-1] * 3
		for a in range(self.__max_nop):
			for b in range(self.__max_nop):
					for c in range(256):
						if(a + c * (b + 3) == cycle - 5 and (a + b) < nop_sum):
							nop_sum = a+b
							tmp[0] = a
							tmp[1] = b
							tmp[2] = c
		# コードを生成
		if(tmp[0] == -1):
			return ""
		result = subroutine_name + "\n"
		for i in range(tmp[0]):
			result += "\tNOP\n"
		result += "\tMOVLW D'" + str(tmp[2]) + "'\n"
		result += "\tMOVWF " + self.__variable_name + "1\n"
		result += self.__label_name + "1\n"
		for i in range(tmp[1]):
			result += "\tNOP\n"
		result += "\tDECFSZ " + self.__variable_name + "1, F\n"
		result += "\tGOTO " + self.__label_name + "1\n"
		result += "\tRETURN"
		return result
	def __delayTwoLoop(self, cycle : int, subroutine_name : str):
		return ""
	def __delayThreeLoop(self, cycle : int, subroutine_name : str):
		return ""
	def generateDelay(self, delay : int, delay_unit : str, subroutine_name : str):
		if(delay <= 0):
			self.__result = ""
			return
		# 生成したいcycle数を計算
		delay_ns = delay
		#delay_unit == "ns"のときは何もしなくてよい
		if(delay_unit == "ns" or delay_unit == "n"):
			dummy = 0
			# 何もしない
		if(delay_unit == "us" or delay_unit == "u"):
			delay_ns *= 1000
		elif(delay_unit == "ms" or delay_unit == "m"):
			delay_ns *= 1000000
		elif(delay_unit == "s"):
			delay_ns *= 1000000000
		else:
			return
		cycle = delay_ns // self.__one_cycle_ns
		# 1重ループから3重ループまでの計算結果を比較する
		res = [""] * 3
		res_weight = self.__MAX_STR_LEN
		res[0] = self.__delayOneLoop(cycle, subroutine_name)
		res[1] = self.__delayTwoLoop(cycle, subroutine_name)
		res[2] = self.__delayThreeLoop(cycle, subroutine_name)
		# 生成に成功しているものの中で，一番文字数が少ないものを求める
		# ラベルは文字数に含まないように考慮している
		for i in range(3):
			w = len(res[i]) - (i+2)
			if(0 < w < res_weight):
				res_weight = w
		if(res_weight == self.__MAX_STR_LEN):
			# 生成に失敗していた場合は文字列を空にしてreturn
			return ""
		# 同じ重みを持っているパラメーターがあればresultに代入
		for i in range(3):
			w = len(res[i]) - (i+2)
			if(w == res_weight):
				self.__result = res[i]
				return self.__result

	def getResult(self):
		return self.__result

if __name__ == '__main__':
	pic = PICCodeGenerator_Delay(1000)
	result = pic.generateDelay(1000, "us", "CNT")
	print(result)