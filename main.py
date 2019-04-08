from solver import Game, DIRECTIONS, UPLEFT,UPRIGHT,RIGHT,DOWNRIGHT,DOWNLEFT,LEFT
from random import choice


"""
84 total initial moves?

-> 42 per team, lets check (symmetry?)
"""

def smart_move():
	mycolor = 0

	movelist = list(game.move_gen(0))

	validmovelist = []
	for move in movelist:
		ivm = game.is_valid_move(*move, mycolor)
		if ivm[0]:
			validmovelist.append([move, ivm])

	# Choose random move that results in enemy loss
	enemylossmoves = [move for move in validmovelist if move[1][1]]
	if len(enemylossmoves) > 0:
		move = choice(enemylossmoves)[0]
	else:
		# Choose random move
		move = choice(validmovelist)[0]

	#print(move[0].coords, move[1])
	y = move[0].coords[1] + 4
	x = move[0].coords[0] - game.xcoord[y]
	print("Y:", y, "X:", x, "DIR", move[1])
	game.move(*move)

def allinitmoves():
	game = Game()
	#game.print()
	#game.printcoords()
	nummoves = len(list(game.move_gen(0)))
	#print(nummoves)
	for i in range(nummoves):
		game = Game()
		moves = list(game.move_gen(0))
		move = moves[i]
		#print(move)
		result = game.move(*move[:2])
		#print(result)
		game.print()
		print("")

	#print(nummoves)

def npcgame():
	game = Game()
	game.print()
	round = 0
	colors = [0,1]
	while not game.is_over():
		if round % 2 == 0:
			#result = game.randommove()
			result = game.aimove()
		else:
			result = game.aimove(debug=True)

		#if round % 100 == 0:
			#print(result)
		#game.print()
		game.print(mode=0)
		if result[0]:
			round += 1

	print(game.out)
	print(round)

def test():
	game = Game()
	game.printcoords()
	game.print()
	print(len(list(game.move_gen())))
	print(game.move([game.at(2,2), game.at(3,2), game.at(4,2)], DOWNRIGHT))
	game.print()
	game.print(mode=3)

def sidebyside(a,b,spacing=3):
	spacing = " " * spacing
	a = a.split("\n")
	b = b.split("\n")
	maxlinelen = max([len(line) for line in a])
	for i,line in enumerate(a):
		print(line + " " * (maxlinelen-len(line)) + b[i])

def pvsnpcgame():
	game = Game()
	game.print()
	game.print(mode=3)
	round = 0
	colors = [0,1]
	while not game.is_over():
		if round % 2 == 0:
			while True:
				try:
					inp = input(">")
					inp = inp.split()
					if "," in inp[0]:
						fields = [game.atname(n) for n in inp[0].split(",")]
					else:
						fields = game.atname(inp[0])
					
					for k, v in DIRECTIONS.items():
						if inp[1].lower() in k.split():
							direction = v
							break
						
					move = [fields, direction]
					result = game.move(*move)
					if result[0]:
						break
					else:
						print(result)
				except Exception as e:
					print(e)
		else:
			result = game.aimove(debug=True)

		#if round % 100 == 0:
			#print(result)
		#game.print()
		#game.print(mode=0)
		#game.print(mode=3)
		sidebyside(game.__repr__(mode=0), game.__repr__(mode=3))
		if result[0]:
			round += 1
		else:
			notice = "ball out" if result[2] else "e"
			print(result)

	print(game.out)
	print(round)

pvsnpcgame()
#npcgame()
#allinitmoves()
#test()
