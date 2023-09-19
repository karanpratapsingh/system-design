import random
from collections import deque
from enum import Enum
from time import sleep

class ShellType(Enum):
	EMPTY = 1
	SNAKE = 2
	FOOD = 3


class Direction(Enum):
	LEFT = 1
	RIGHT = -1
	TOP = 2
	DOWN = -2


class Shell:
	def __init__(self, row: int, column: int):
		self.row = row
		self.col = column
		self.shell_type = ShellType.EMPTY

	def get_row(self):
		return self.row

	def get_column(self):
		return self.col

	def set_shell_type(self, shell_type: ShellType):
		self.shell_type = shell_type

	def get_shell_tpe(self):
		return self.shell_type


class Snake:

	def __init__(self, head: Shell):
		self.head = head
		self.head.set_shell_type(ShellType.SNAKE)
		self.snake = deque([self.head])
		self.direction = Direction.RIGHT

	def move(self, new_shell: Shell):
		print(f'Moving to {new_shell.row}-{new_shell.col}')
		if new_shell.shell_type != ShellType.FOOD:
			popped_shell = self.snake.pop()
			popped_shell.set_shell_type(ShellType.EMPTY)
		self.snake.append(new_shell)
		new_shell.set_shell_type(ShellType.SNAKE)
		self.head = new_shell

	def get_score(self):
		return len(self.snake)


class Board:

	def __init__(self, row_count, col_count):
		self.row_count = row_count
		self.col_count = col_count
		self.board = [[Shell(i, j) for j in range(col_count)] for i in range(row_count)]

	def already_have_food(self):
		for i in range(self.row_count):
			for j in range(self.col_count):
				if self.board[i][j].shell_type == ShellType.FOOD:
					return True
		return False

	def generate_food(self):
		while True:
			row = random.choice(range(self.row_count))
			col = random.choice(range(self.col_count))
			if self.board[row][col].shell_type == ShellType.EMPTY:
				self.board[row][col].set_shell_type(ShellType.FOOD)
				print(f'Food is at {row}-{col}')
				break

class Game:

	def __init__(self, row_count, col_count):
		self.board = Board(row_count, col_count)
		self.snake = Snake(Shell(0, 0))
		self.is_game_over = False

	def get_is_game_over(self):
		return self.is_game_over

	def get_safe_row(self, row):
		if row - 1 < 0:
			self.change_direction(Direction.DOWN)
			return row + 1
		self.change_direction(Direction.TOP)
		return row -1
	def get_safe_col(self, col):
		if col - 1 < 0:
			self.change_direction(Direction.RIGHT)
			return col + 1
		self.change_direction(Direction.LEFT)
		return col - 1

	def save_from_boundry(self, row, col):
		if row < 0:
			row += 1
			col = self.get_safe_col(col)
		elif row == self.board.row_count:
			row -= 1
			col = self.get_safe_col(col)
		elif col < 0:
			col += 1
			row = self.get_safe_row(row)
		elif col == self.board.col_count:
			col -= 1
			row = self.get_safe_row(row)
		return row, col

	def get_next_shell_cordinate(self):
		row = self.snake.head.row
		col = self.snake.head.col
		if self.snake.direction == Direction.RIGHT:
			col += 1
		elif self.snake.direction == Direction.LEFT:
			col -= 1
		if self.snake.direction == Direction.TOP:
			row -= 1
		elif self.snake.direction == Direction.DOWN:
			row += 1
		return self.save_from_boundry(row, col)

	def is_shell_safe(self, row, col):
		if row < 0 or row >= self.board.row_count or col < 0 or col >= self.board.col_count or self.board.board[row][col].shell_type == ShellType.SNAKE:
			return False
		return True

	def mark_game_over(self):
		self.is_game_over = True
		print(f'Your Score is {len(self.snake.snake)}')

	def play(self):
		time_count = 0
		while True:
			sleep(.2)
			time_count += 1
			if time_count%2 == 0:
				self.change_direction_random()
				not self.board.already_have_food() and self.board.generate_food()
			row, col = self.get_next_shell_cordinate()
			if self.is_shell_safe(row, col):
				self.snake.move(self.board.board[row][col])
			else:
				self.mark_game_over()
				break
	def change_direction_random(self):
		if self.snake.direction == Direction.TOP:
			self.change_direction(random.choice([Direction.TOP, Direction.LEFT, Direction.RIGHT]))
		elif self.snake.direction == Direction.DOWN:
			self.change_direction(random.choice([Direction.DOWN, Direction.LEFT, Direction.RIGHT]))
		elif self.snake.direction == Direction.LEFT:
			self.change_direction(random.choice([Direction.TOP, Direction.LEFT, Direction.DOWN]))
		elif self.snake.direction == Direction.RIGHT:
			self.change_direction(random.choice([Direction.TOP, Direction.RIGHT, Direction.RIGHT]))

	def change_direction(self, direction: Direction):
		print(f'Changing direction to {direction}')
		self.snake.direction = direction


game = Game(10, 10)
game.play()
