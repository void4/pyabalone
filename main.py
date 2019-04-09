from solver import Game
from random import choice

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
		game.print(stats=False)
		print("")

	print(nummoves)

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
	#print(game.move([game.at(2,2), game.at(3,2), game.at(4,2)], DOWNRIGHT))
	#game.print()
	#game.print(mode=3)

def pvsnpcgame(premoves=None):
	game = Game()
	#game.print()
	#game.print(mode=3)

	if isinstance(premoves, str):
		for line in premoves.split("\n"):
			line = line.strip()
			if len(line) == 0:
				continue
			print(line)
			game.move(*game.move_from_str(line))
			game.aimove()

	game.printsbs()
	round = 0
	colors = [0,1]

	while not game.is_over():
		if game.next_color == 0:
			while True:
				try:
					inp = input(">")
					move = game.move_from_str(inp)
					result = game.move(*move)
					if result[0]:
						break
					else:
						print(result)
				except Exception as e:
					print(e)
		else:
			result = game.aimove(debug=False)

		#if round % 100 == 0:
			#print(result)
		#game.print()
		#game.print(mode=0)
		#game.print(mode=3)
		game.printsbs()
		if result[0]:
			round += 1
		else:
			notice = "ball out" if result[2] else "e"
			print(result)

	print(game.out)
	print(round)

premoves = """
0 dl
5 dl
B dl
Q dr
Z dr
"""

if __name__ == "__main__":
	pvsnpcgame()
	#pvsnpcgame(premoves)
#npcgame()
#allinitmoves()
#test()
