class Ladder():

	# { 3: 22, 5: 8, 11: 26, 20: 29 }
	def __init__(self, start, end) -> None:
		self.start = start
		self.end = end

	def __eq__(self, other):
		return self.start == other.end and self.start == other.end

	def get_start(self):
		return self.start
	
	def get_end(self):
		return self.end
