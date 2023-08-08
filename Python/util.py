import unicodedata
def getStringLendth(text):
	"""
	参考:https://note.nkmk.me/python-unicodedata-east-asian-width-count/
	"""
	count = 0
	for c in text:
		if unicodedata.east_asian_width(c) in 'FWA':
			count += 2
		else:
			count += 1
	mod = count % 2
	count = count //2 + mod
	return count