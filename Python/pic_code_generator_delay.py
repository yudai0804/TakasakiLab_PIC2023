class PICCodeGenerator_Delay:
	def __init__(self, one_cycle_ns : int, max_nop = 5, label_name = "JUMP", variable_name = "CNT"):
		self.__one_cycle_ns = one_cycle_ns
		self.__max_nop = max_nop
		self.__label_name = label_name
		self.__variable_name = variable_name
		self.__result = ";Generate Failed\n"
		self.__max_str_len = 10000
	def __delayOneLoop(self, delay_cycle : int, subroutine_name : str):
		# 最適なNOPと繰り返し回数を計算
		nop_sum = self.__max_nop
		tmp = [-1] * 3
		for a in range(self.__max_nop):
				x = delay_cycle - a - 5
				if(x < 3):
					break
				for c in range(1, 256):
					if(x % c != 0):
						continue
					b = x // c - 3
					if(b < 0):
						break
					sum = a + b
					if(sum < nop_sum):
						nop_sum = sum
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
	def __delayTwoLoop(self, delay_cycle : int, subroutine_name : str):
		# 最適なNOPと繰り返し回数を計算
		nop_sum = self.__max_nop
		tmp = [-1] * 5
		for a in range(self.__max_nop):
			x = delay_cycle - a - 5
			if(x < 7):
				break
			for d in range(1, 256):
				if(x % d != 0):
					continue
				for b in range(self.__max_nop):
					y = x // d - b - 4
					if(y < 3):
						break
					for e in range(1, 256):
						if(y % e != 0):
							continue
						c = y // e - 3
						if(c < 0):
							break
						sum = a + b + c
						if(sum < nop_sum):
							nop_sum = sum
							tmp[0] = a
							tmp[1] = b
							tmp[2] = c
							tmp[3] = d
							tmp[4] = e
		# コードを生成
		if(tmp[0] == -1):
			return ""
		result = subroutine_name + "\n"
		for i in range(tmp[0]):
			result += "\tNOP\n"
		result += "\tMOVLW D'" + str(tmp[3]) + "'\n"
		result += "\tMOVWF " + self.__variable_name + "1\n"
		result += self.__label_name + "1\n"
		for i in range(tmp[1]):
			result += "\tNOP\n"
		result += "\tMOVLW D'" + str(tmp[4]) + "'\n"
		result += "\tMOVWF " + self.__variable_name + "2\n"
		result += self.__label_name + "2\n"
		for i in range(tmp[2]):
			result += "\tNOP\n"
		result += "\tDECFSZ " + self.__variable_name + "2, F\n"
		result += "\tGOTO " + self.__label_name + "2\n"
		result += "\tDECFSZ " + self.__variable_name + "1, F\n"
		result += "\tGOTO " + self.__label_name + "1\n"
		result += "\tRETURN"
		return result
	def __delayThreeLoop(self, delay_cycle : int, subroutine_name : str):
		# 最適なNOPと繰り返し回数を計算
		nop_sum = self.__max_nop
		tmp = [-1] * 7
		for a in range(self.__max_nop):
			x = delay_cycle - a - 5
			if(x < 11):
				break
			for e in range(1, 256):
				if(x % e != 0):
					continue
				for b in range(self.__max_nop):
					y = x // e - b - 4
					if(y < 7):
						break
					for f in range(1, 256):
						if(y % f != 0):
							continue
						for c in range(self.__max_nop):
							z = y // f - c - 4
							if(z < 3):
								break
							for g in range(1, 256):
								if(z % g != 0):
									continue
								d = z // g - 3
								if(d < 0):
									break
								sum = a + b + c + d
								if(sum < nop_sum):
									nop_sum = sum
									tmp[0] = a
									tmp[1] = b
									tmp[2] = c
									tmp[3] = d
									tmp[4] = e
									tmp[5] = f
									tmp[6] = g

		# コードを生成
		if(tmp[0] == -1):
			return ""
		result = subroutine_name + "\n"
		for i in range(tmp[0]):
			result += "\tNOP\n"
		result += "\tMOVLW D'" + str(tmp[4]) + "'\n"
		result += "\tMOVWF " + self.__variable_name + "1\n"
		result += self.__label_name + "1\n"
		for i in range(tmp[1]):
			result += "\tNOP\n"
		result += "\tMOVLW D'" + str(tmp[5]) + "'\n"
		result += "\tMOVWF " + self.__variable_name + "1\n"
		result += self.__label_name + "2\n"
		for i in range(tmp[2]):
			result += "\tNOP\n"
		result += "\tMOVLW D'" + str(tmp[6]) + "'\n"
		result += "\tMOVWF " + self.__variable_name + "3\n"
		result += self.__label_name + "3\n"
		for i in range(tmp[3]):
			result += "\tNOP\n"
		result += "\tDECFSZ " + self.__variable_name + "3, F\n"
		result += "\tGOTO " + self.__label_name + "3\n"
		result += "\tDECFSZ " + self.__variable_name + "2, F\n"
		result += "\tGOTO " + self.__label_name + "2\n"
		result += "\tDECFSZ " + self.__variable_name + "1, F\n"
		result += "\tGOTO " + self.__label_name + "1\n"
		result += "\tRETURN"
		return result
	def generateDelay(self, delay : int, delay_unit : str, subroutine_name : str):
		if(delay <= 0):
			self.__result = ";Generate Failed\n"
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
		delay_cycle = delay_ns // self.__one_cycle_ns
		# 1重ループから3重ループまでの計算結果を比較する
		res = [""] * 3
		MAX_WEIGHT = 10000
		res_weight = MAX_WEIGHT
		res[0] = self.__delayOneLoop(delay_cycle, subroutine_name)
		res[1] = self.__delayTwoLoop(delay_cycle, subroutine_name)
		res[2] = self.__delayThreeLoop(delay_cycle, subroutine_name)
		# 生成に成功しているものの中で，一番文字数が少ないものを求める
		# ラベルは文字数に含まないように考慮している
		for i in range(3):
			w = len(res[i]) - (i+2)
			if(0 < w < res_weight):
				res_weight = w
		if(res_weight == MAX_WEIGHT):
			# 生成に失敗していた場合は文字列を空にしてreturn
			return ";Generate Failed\n"
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
	result = pic.generateDelay(1000, "us", "Timer")
	print(result)