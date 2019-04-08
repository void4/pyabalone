from collections import Counter
from copy import deepcopy

UPLEFT,UPRIGHT,RIGHT,DOWNRIGHT,DOWNLEFT,LEFT = range(6)

deltas = {
UPLEFT: [0,1,-1],
UPRIGHT: [1,0,-1],
RIGHT: [1,-1,0],
DOWNRIGHT: [0,-1,1],
DOWNLEFT: [-1,0,1],
LEFT: [-1,1,0]
}

class Field:
	def __init__(self, board, coords, xycoords, color=None):
		self.board = board
		self.coords = coords
		self.color = color
		self.xycoords = xycoords

	def to(self, direction):
		delta = deltas[direction]
		newcoords = [self.coords[0]+delta[0], self.coords[1]+delta[1], self.coords[2]+delta[2]]
		for field in self.board:
			if field.coords == newcoords:
				return field
		return None

	def __repr__(self):
		return str(self.xycoords) + ":" + str(self.color)


class Game:

	def __init__(self):#n players?
		# Cube coordinates
		# https://www.redblobgames.com/grids/hexagons/
		self.next_color = 0

		self.board = []
		self.out = Counter()

		self.rowlength = [5,6,7,8,9,8,7,6,5]

		self.xcoord = [0,-1,-2,-3,-4,-4,-4,-4,-4]
		self.ycoord = [4,4,4,4,4,3,2,1,0]
		for y in range(9):
			for x in range(self.rowlength[y]):
				coords = [self.xcoord[y]+x,self.ycoord[y]-x,-4+y]
				#print(coords)
				assert sum(coords) == 0
				color = None
				if y in [0,1] or (y == 2 and x in [2,3,4]):
					color = 0
				elif y in [7,8] or (y == 6 and x in [2,3,4]):
					color = 1
				self.board.append(Field(self.board, coords, [x,y], color))


	def at(self, x, y):
		fields = [field for field in self.board if field.xycoords == [x,y]]
		if len(fields) == 0:
			return None
		return fields[0]

	def printcoords(self):
		index = 0
		for y in range(9):
			for x in range(self.rowlength[y]):
				print(self.board[index].coords, end=" ")
				index += 1
			print("")

	def print(self):
		s = ""
		index = 0
		for y in range(9):
			s += " " * (9 - self.rowlength[y])
			for x in range(self.rowlength[y]):
				col = self.board[index].color
				if col is None:
					col = "-"
				else:
					col = str(col)
				s += " "+col
				index += 1
			s += "\n"
		print(s, end="")
		print(self.out)
		print("Next color is: ", self.next_color)

	def is_valid_move(self, field, direction, color=None, debug=False):
		if color is None:
			color = self.next_color
		# Side move
		if isinstance(field, list):
			for subfield in field:
				if subfield.color != color:
					return False, "Invalid color for side move"
				target = subfield.to(direction)
				if target is None:
					return False, "Can't make side move outside of board"
				if target.color is not None:
					return False, "Can't make side move on enemy piece"

			return True, False

		"""!!! Use is_valid_move()[0] !!!"""
		#sideway moves :/

		if color != self.next_color:
			return False, "Not your (%s) turn, it's %i turn" % (str(color), self.next_color)

		if color is None:
			return False, "Can't move nothing"

		if field.color != color:
			return False, "Can't move enemy ball"

		fields = [field]

		lastisborder = False
		ownfields = 1#assume, or add color argument?
		enemyfields = 0
		while True:
			nextfield = fields[-1].to(direction)
			if nextfield == None:
				lastisborder = True
				break

			if nextfield.color is None:
				break
			elif nextfield.color == color:
				ownfields += 1
			else:
				enemyfields += 1

			fields.append(nextfield)

		enemyloss = False
		if lastisborder:
			if fields[-1].color == color:
				return False, "Can't push out own ball"
			else:
				enemyloss = True

		if ownfields < enemyfields + 1:
			return False, "Not enough balls to move enemy"

		if ownfields > 3:
			return False, "Can't move more than 3 balls"


		if debug:
			print(fields, lastisborder, fields[-1].color, color)

		return True, enemyloss

	def get_repeats(self, fields, key=None, repeat=None):
		if key is None:
			key = lambda f : f.color

		if repeat is None:
			repeat = [2,3]

		values = []
		for i,field in enumerate(fields):
			values.append(key(field))

		for i, field in enumerate(fields):
			for r in repeat:
				sublist = values[i:i+r]
				if len(sublist) == r and len(set(sublist)) == 1:
					yield fields[i:i+r]

	def move_gen(self, color=None):
		if color is None:
			color = self.next_color

		for field in self.board:
			#print(field.color, color)
			if field.color == color:
				for direction in deltas.keys():
					ivm = self.is_valid_move(field, direction, field.color)
					if ivm[0]:
						yield field, direction, ivm[1]

		# for every axis, every subset of 2-3 own balls on axis

		#x,y format
		axes = [
		[[RIGHT, LEFT], [[0,0],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[0,8]]],
		[[DOWNRIGHT, UPLEFT], [[0,4],[0,3],[0,2],[0,1],[0,0],[1,0],[2,0],[3,0],[4,0]]],
		[[DOWNLEFT, UPRIGHT], [[0,0],[1,0],[2,0],[3,0],[4,0],[5,1],[6,2],[7,3], [8,4]]]
		]
		for axis in axes:
			for i, start in enumerate(axis[1]):
				fields = [self.at(start[0], start[1])]
				for c in range(self.rowlength[i]-1):
					fields.append(fields[-1].to(axis[0][0]))

				sublists = self.get_repeats(fields)

				for direction in axis[0]:
					for sublist in sublists:
						if self.is_valid_move(sublist, direction)[0]:
							yield fields, direction, ivm[1]

	def move(self, field, direction):
		if isinstance(field, Field):
			color = field.color
		else:
			color = field[0].color
		ivm = self.is_valid_move(field, direction, color, debug=False)
		if not ivm[0]:
			return ivm

		fields = [field]
		while True:
			nextfield = fields[-1].to(direction)

			fields.append(nextfield)
			if nextfield is not None and nextfield.color is None:
				break

			if nextfield is None:
				break

		if fields[-1] is None:
			self.out[fields[-2].color] += 1
			fields = fields[:-1]

		for i in range(len(fields)-1, 0, -1):
			fields[i].color = fields[i-1].color

		fields[0].color = None

		self.next_color = 0 if self.next_color == 1 else 1

		return True, "Done"

	def is_over(self):
		return 6 in self.out.values()

	def translate(self, fields):
		"""Translates fields from other game into this game"""
		if isinstance(fields, Field):
			return self.at(*fields.xycoords)
		elif isinstance(fields, list):
			results = []
			for field in fields:
				results.append(self.at(*field.xycoords))
			return results
		else:
			raise Exception("Translation Error")

	def aimove(self):
		from random import random
		MAXNODES = 1000
		#print("AI", self.next_color)
		moves = sorted(list(self.move_gen()), key=lambda m:random())
		sortedmoves = sorted(moves, key=lambda m:m[2], reverse=True)#[:5]
		scorelist = []

		def recurse(game, depth=0):
			#print(depth	)
			score = 0
			moves = sorted(list(game.move_gen()), key=lambda m:random())
			for move in sorted(moves, key=lambda m:m[2], reverse=True)[:2]:
					if move[2]:
						score -= 1#increase loss value if it loses the game!

					subgame = deepcopy(game)
					subgame.move(subgame.translate(move[0]), move[1])

					submoves = sorted(list(subgame.move_gen()), key=lambda m:random())
					for submove in sorted(submoves, key=lambda m:m[2], reverse=True)[:2]:
							if submove[2]:
								score += 1

							subgame2 = deepcopy(game)
							subgame2.move(subgame2.translate(submove[0]), submove[1])

							if depth < 0:#1:
								score += recurse(game, depth+1)



			return score

		for submove in sortedmoves:
				score = 0
				if submove[2]:
					score += 1

				subgame = deepcopy(self)
				subgame.move(subgame.translate(submove[0]), submove[1])

				score += recurse(subgame)

				scorelist.append(score)

		print(scorelist)
		bestmove = sortedmoves[scorelist.index(max(scorelist))]#randomize a bit, in case of same scores?
		result = self.move(*bestmove[:2])
		return result

	def randommove(self):
		from random import choice
		move = choice(list(self.move_gen()))
		result = self.move(*move[:2])
		return result
