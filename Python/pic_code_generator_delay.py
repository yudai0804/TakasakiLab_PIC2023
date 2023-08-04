class PICCodeGenerator_Delay:
	def __init__(self, one_cycle_ns : int, max_nop = 5, label_name = "JUMP"):
		self.__one_cycle_ns = one_cycle_ns
		self.__max_nop = max_nop
		self.__label_name = "JUMP"
		self.__result = ""
	def __delayOneLoop(self, delay_ns : int):
		print("a")
	def __delayTwoLoop(self, delay_ns : int):
		print("a")
	def __delayThreeLoop(self, delay_us : int):
		print("a")
	def generateDelay(self, delay : int, delay_unit : str):
		if(delay <= 0):
			self.__is_success = False
			return
		# 生成したいdelayの時間を計算
		delay_ns = delay
		#delay_unit == "ns"のときは何もしなくてよい
		if(delay_unit == "us"):
			delay_ns *= 1000
		elif(delay_unit == "ms"):
			delay_ns *= 1000000
		elif(delay_unit == "s"):
			delay_ns *= 1000000000
		
		# 1重ループから3重ループまでの計算結果を比較する
		is_success = [0] * 3
		res = [0] * 3
		res_weight = 1000
		is_success[0], res[0] = self.__delayOneLoop(delay_ns)
		is_success[1], res[1] = self.__delayTwoLoop(delay_ns)
		is_success[2], res[2] = self.__delayThreeLoop(delay_ns)
		# 生成に成功しているものの中で，一番文字数が少ないものを求める
		# ラベルは文字数に含まないように考慮している
		for i in range(3):
			w = len(res[i]) - (i+1)
			if(is_success[i] == True and w < res_weight):
				res_weight = w
		if(res_weight == 1000):
			# 生成に失敗していた場合は文字列を空にしてreturn
			self.__result = ""
			return
		
		# 同じ重みを持っているパラメーターがあればresultに代入
		for i in range(3):
			w = len(res[i]) - (i+1)
			if(w == res_weight):
				self.__result = res[i]
				return

	def getResult(self):
		return self.__result
