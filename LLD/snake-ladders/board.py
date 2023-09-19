class Board():

	def __init__(self, size) -> None:
		self.ladders = []
		self.snakes = []
		self.size = size

	def is_ladder_present(self, pos):
		for ladder in self.ladders:
			if (ladder.start == pos):
				return True

	def place_ladder(self, ladder):
		self.ladders.append(ladder)

	def get_ladder_dest(self, pos):
		for ladder in self.ladders:
			if (ladder.start == pos):
				return ladder.end

	def is_snake_present(self, pos):
		for snake in self.snakes:
			if (snake.head == pos):
				return True

	def place_snake(self, snake):
		self.snakes.append(snake)

	def get_snake_tail(self, pos):
		for snake in self.snakes:
			if (snake.head == pos):
				return snake.tail