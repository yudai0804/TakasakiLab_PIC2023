class FontLoader:
	def __init__(self) -> None:
		self.name = ""
	def getName(self) -> str:
		return self.name
	def setName(self, name:str) -> None:
		self.name = name
	def print(self) -> None:
		print(self.name)

a = FontLoader()
a.setName("Tanaka")
a.print()
b = a.getName()
b = "yamada"
a.print()