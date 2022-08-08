class Zone():
	def __init__(self):
		self.__farmid = None
		self.__zoneid = None
		self.__gmd = None
		self.__recoverytime = None
		self.__amountcattlesuport = None
		self.__lastexit = None
		self.__inputzone = None

	def set_farmid(self, farmid):
		self.__farmid = farmid

	def set_zoneid(self, zoneid):
		self.__zoneid = zoneid

	def set_gmd(self, gmd):
		self.__gmd = gmd

	def set_recoverytime(self, recoverytime):
		self.__recoverytime = recoverytime

	def set_amountcattlesuport(self, amountcattlesuport):
		self.__amountcattlesuport = amountcattlesuport

	def set_lastexit(self, lastexit):
		self.__lastexit = lastexit

	def set_inputzone(self, inputzone):
		self.__inputzone = inputzone

	def get_farmid(self):
		return self.__farmid 

	def get_zoneid(self):
		return self.__zoneid 

	def get_gmd(self):
		return self.__gmd 

	def get_recoverytime(self):
		return self.__recoverytime 

	def get_amountcattlesuport(self):
		return self.__amountcattlesuport 

	def get_lastexit(self):
		return self.__lastexit 

	def get_inputzone(self):
		return self.__inputzone 

