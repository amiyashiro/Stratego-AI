from pieces import *
from player import *
import random
from AI import *

class Stratego:
	def __init__(self):
		self.board = []
		self.columns = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
		for i in range(8):
			self.board.append([])
			for j in range(8):
				self.board[i].append(None)

		self.redGraveyard = []
		self.blueGraveyard = []
		self.populateGraveyard(self.redGraveyard, 'red')
		self.populateGraveyard(self.blueGraveyard, 'blue')
		

		###Change these to have human player, random player, or AI
		#self.redPlayer = Player('red', self.getBoard())
		#self.redPlayer = Random('red', self.getBoard())
		self.redPlayer = AI('red', self.getBoard())
		redPlayer = self.getPlayer('red')
		
		#self.bluePlayer = Player('blue', self.getBoard())
		#self.bluePlayer = Random('blue', self.getBoard())
		self.bluePlayer = Random('blue', self.getBoard())
		bluePlayer = self.getPlayer('blue')
		

		redGrave = self.getGraveyard('red')
		for piece in redGrave:
			redPlayer.addMyPiece(piece)
			bluePlayer.addEnemyPiece(piece)
		
		blueGrave = self.getGraveyard('blue')
		for piece in blueGrave:
			bluePlayer.addMyPiece(piece)
			redPlayer.addEnemyPiece(piece)

		self.lastMove = ((-1, -1), (-1, -1))


	def getGraveyard(self, c):
		if c == 'red':
			return self.redGraveyard
		elif c == 'blue':
			return self.blueGraveyard

	def getBoard(self):
		return self.board

	def getLastMove(self):
		return self.lastMove

	def updateBoard(self, newBoard):
		self.board = newBoard

	def printBoard(self):
		for row in self.board:
			print row
			print ''

	def printGraveyard(self, graveyard):
		for row in graveyard:
			for piece in row:
				print piece.getName()

	def printBoardLine(self, line):
		for piece in line:
			if piece is None:
				print '_______ ',
			elif piece.getTeam() == 'blue':
				print ' HIDDEN ',
			else:
				print piece.getName() + ' ',	

	def printPiece(self, piece):
		print piece.getName(),

	def printGame(self):
		labels = ['A','B','C','D','E','F','G','H']
		print
		print "Red Team",
		for _ in range(14):
			print '\t',
		print "Blue Team"

		for _ in range(3):
			print '\t',
		for label in labels:
			print label.rjust(8),
		for _ in range(4):
			print '\t',
		print

		for line in range(10):
			self.printPiece(self.redGraveyard[line])
			
			for _ in range(2):
				print '\t',

			if line < 8:
				board = self.getBoard()
				print '{} '.format(line),
				self.printBoardLine(board[line])
			else:
				for _ in range(9):
					print '\t',

			for _ in range(3):
				print '\t',
			
			self.printPiece(self.blueGraveyard[line])
			print

	def populateGraveyard(self, graveyard, team):
		graveyard.append(Flag(team))		
		graveyard.append(Spy(team))
		graveyard.append(General(team))
		graveyard.append(Marshall(team))

		for i in range(2):
			graveyard.append(Bomb(team))

		for i in range(2):
			graveyard.append(Scout(team))

		for i in range(2):
			graveyard.append(Miner(team))

	def getGraveyard(self, team):
		if team == 'red':
			return self.redGraveyard
		else: 
			return self.blueGraveyard

	def getPlayer(self, team):
		if team == 'red':
			return self.redPlayer
		else: 
			return self.bluePlayer

	def isSpotTaken(self, board, row, col):
		if board[row][col] is None:
			return False
		else:
			return True

	def placePieces(self, team, randomize):
		graveyard = self.getGraveyard(team)
		player = self.getPlayer(team)
		board = self.getBoard()

		if team == 'red':
			upBound = 7
			lowBound = 5
		else:
			upBound = 2
			lowBound = 0

		if randomize == True:
			for i in range(10):
				piece = graveyard.pop(i)
				graveyard.insert(i, NullPiece())
				row = random.randint(lowBound, upBound)
				col = random.randint(0,7)
					
				while self.isSpotTaken(board, row, col):
					row = random.randint(lowBound, upBound)
					col = random.randint(0,7)

				self.placePiece(piece, board, row, col)
		else:
			while any(graveyard):  #While graveyard is not empty
				find = False

				while True:
					piece = raw_input('Name of piece (cap, gen, etc.): ')
					location = raw_input('Location (A1, G7, etc.): ')

					if team == 'red' and int(location[1]) < 5:
						print "Place your piece in a starting position (rows 5-7)."
					else:
						break

				for i in range(10):					
					item = graveyard[i]

					if piece == item.getID():
						item = graveyard.pop(i)
						graveyard.insert(i, NullPiece())

						col = self.columns[location[0].lower()]
						row = int(location[1])

						if self.isSpotTaken(board, row, col): 
							print "Spot is already taken."			
							find = True
							break
						else:
							self.placePiece(item, board, row, col)
							self.printGame()
							break


	def placePiece(self, piece, board, row, col):
		board[row].pop(col)
		board[row].insert(col, piece)
		piece.setLocation(row, col)

	def movePiece(self, move, board): #takes a move (location, destination) and performs the move in the given board
			location = move[0]
			ypos = location[0]
			xpos = location[1]

			destination = move[1]
			ydest = destination[0]
			xdest = destination[1]

			target = board[ydest][xdest]			   

			piece = board[ypos].pop(xpos)
			board[ypos].insert(xpos, None)

			#piece is going to move, must update prob. dist. for this piece and others if needed
			piece.addMove()
			if self.movedMultipleSpaces(move):
				#piece moved multiples spaces, so it is a scout
				if not piece.isKnown():
					self.makePieceKnown(piece)

			if self.isCollision(move, board):
				#there is a collision between two pieces, so both with will be known
				destination = move[1]
				row = destination[0]
				col = destination[1]
				enemyPiece = board[row][col]

				if not piece.isKnown():
					self.makePieceKnown(piece)
				if not enemyPiece.isKnown():
					self.makePieceKnown(enemyPiece)

			if not piece.hasMoved():
				#first time this piece is moving
				piece.firstTimeMoving()
				if piece.getGuess() == 0 or piece.getGuess() == 11:
					team = piece.getTeam()
					player = self.getPlayer(team)
					player.setMusicalChairs()

				#piece.getProbabilityDistribution().pieceMoved()

			if target is None:
				#spot is empty
				board[ydest].pop(xdest)
				board[ydest].insert(xdest, piece)
				piece.setLocation(ydest, xdest)
				self.updateBoard(board)
			else:
				#enemy piece is in spot
				redGrave = self.getGraveyard('red')
				blueGrave = self.getGraveyard('blue')
				self.attack(piece, destination, redGrave, blueGrave, board)

			self.setLastMove(move)

	def movedMultipleSpaces(self, move):
		location = move[0]
		row = location[0]
		col = location[1]

		destination = move[1]
		rowDest = destination[0]
		colDest = destination[1]

		if abs(row - rowDest) > 1:
			return True
		elif abs(col - colDest) > 1:
			return True
		else:
			return False

	def makePieceKnown(self, piece):
		piece.makeKnown()
		team = piece.getTeam()
		player = self.getPlayer(team)
		player.setMusicalChairs()
		#otherPieces = player.getMyPieces()
		#for myPiece in otherPieces:
		#	if not myPiece == piece:
		#		myPiece.getProbabilityDistribution().pieceSeen(piece.getID())


	def isCollision(self, move, board):
		location = move[0]
		row = location[0]
		col = location[1]

		destination = move[1]
		rowDest = destination[0]
		colDest = destination[1]

		if board[rowDest][colDest] is None:
			return False
		else:
			return True

	def gameOver(self):
		redGrave = self.getGraveyard('red')
		blueGrave = self.getGraveyard('blue')
		for i in range(10):
			redPiece = redGrave[i].getID()
			bluePiece = blueGrave[i].getID()
			if redPiece == 'flg':
				print "Blue team wins!"
				self.printGame()
				return True
			elif bluePiece == 'flg':
				self.printGame()
				print "Red Team wns!"
				return True

		board = self.getBoard()
		for i in range(8):
			for j in range(8):
				piece = board[i][j]
				if not piece is None:
					if not piece.getID() == 'flg' and not piece.getID() == 'bmb':
						return False
		print "No moveable pieces left. Tie!"
		return True

	def attack(self, piece, target, redGrave, blueGrave, board):
		ydest = target[0]
		xdest = target[1]
		enemy = board[ydest][xdest]

		enemyRank = enemy.getRank()
		myRank = piece.getRank()

		if myRank == 1 and enemyRank == 10:
			#spy wins
			self.placePiece(piece, board, ydest, xdest)
			self.addToGrave(enemy)
		elif enemyRank == 11:
			if myRank == 3:
				#miner wins
				self.placePiece(piece, board, ydest, xdest)
				self.addToGrave(enemy)
			else:
				#piece and enemy bomb removed
				board[ydest].pop(xdest)
				board[ydest].insert(xdest, None)
				self.addToGrave(enemy)
				self.addToGrave(piece)
		elif myRank > enemyRank:
			#piece wins
			self.placePiece(piece, board, ydest, xdest)
			self.addToGrave(enemy)
		elif myRank < enemyRank:
			#enemy wins
			self.addToGrave(piece)
		else:
			#tie, both removed
			self.addToGrave(piece)
			board[ydest].pop(xdest)
			board[ydest].insert(xdest, None)
			self.addToGrave(enemy)

		#print
		#print '{} piece: {}'.format(enemy.getTeam().capitalize(), enemy.getName())

	def addToGrave(self, piece): #add given piece to its graveyard
		team = piece.getTeam()
		grave = self.getGraveyard(team)

		for i in range(10):
			if grave[i].getID() == 'null':
				grave.pop(i)
				grave.insert(i, piece)
				piece.setLocation(-1, -1)
				break

	def setLastMove(self, move):
		self.lastMove = move

	def showLastMove(self):
		move = self.getLastMove()
		columns = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H'}

		location = move[0]
		ypos = location[0]
		xpos = columns[location[1]]

		destination = move[1]
		ydes = destination[0]
		xdes = columns[destination[1]]

		lastMove = (xpos + str(ypos), xdes + str(ydes))

		print "Last move: ", lastMove

	def simGameOver(self):
		redGrave = self.getGraveyard('red')
		blueGrave = self.getGraveyard('blue')
		for i in range(10):
			redPiece = redGrave[i].getID()
			bluePiece = blueGrave[i].getID()
			if redPiece == 'flg':
				print "Blue team wins!"
				return 2
			elif bluePiece == 'flg':
				print "Red team wins!"
				return 1

		board = self.getBoard()
		redPieces = 0
		bluePieces = 0
		for i in range(8):
			for j in range(8):
				piece = board[i][j]
				if not piece is None:
					if not piece.getID() == 'flg' and not piece.getID() == 'bmb':
						if piece.getTeam() == 'red':
							redPieces += 1
						else:
							bluePieces += 1

		if redPieces == 0 and bluePieces == 0:
			#tie
			print "No movable pieces left. Tie!"
			return 3
		elif bluePieces == 0:
			#red wins
			print "Red team wins!"
			return 1
		elif redPieces == 0:	
			#blue wins
			print "Blue team wins!"
			return 2		
			



def simulate(n):
	#simulates n games between a random player and our AI
	#red player is our AI, blue player is random
	redWins = 0
	blueWins = 0
	ties = 0

	for i in range(n):
		stratego = Stratego()
		stratego.placePieces('red', True)
		stratego.placePieces('blue', True)
		stratego.redPlayer.setMusicalChairs()
		stratego.bluePlayer.setMusicalChairs()
		stratego.printGame()

		while True:
			move = stratego.redPlayer.getMove()
			stratego.movePiece(move, stratego.getBoard())

			flag = stratego.simGameOver()
			if flag == 1:
				#red wins
				redWins += 1
				break
			if flag == 2:
				#blue wins
				blueWins += 1
				break
			if flag == 3:
				#tie
				ties += 1
				break
				
			move = stratego.bluePlayer.getMove()
			stratego.movePiece(move, stratego.getBoard())

			flag = stratego.simGameOver()
			if flag == 1:
				#red wins
				redWins += 1
				break
			if flag == 2:
				#blue wins
				blueWins += 1
				break
			if flag == 3:
				#tie
				ties += 1
				break

	print "Simulation Over."
	print "Red Wins (AI): {}".format(redWins)
	print "Blue Wins (Random): {}".format(blueWins)
	print "Ties: {}".format(ties)
	return 0


def simOneGame():
	stratego = Stratego()
	piece = stratego.blueGraveyard[0]
	stratego.placePieces('red', True) #True randomizes starting places
	stratego.placePieces('blue', True)
	stratego.redPlayer.setMusicalChairs()
	stratego.bluePlayer.setMusicalChairs()
	stratego.printGame()

	loss = False

	while not stratego.gameOver():
		
		while True:
			move = stratego.redPlayer.getMove()
			if move == 0:
				print "No moves. Red loses!"
				loss = True
				break
			if move:
				stratego.movePiece(move, stratego.getBoard())
				#stratego.printGame()
				#stratego.showLastMove()
				break

		if loss:
			stratego.printGame()
			break

		if stratego.gameOver():
			break

		while True:
			move = stratego.bluePlayer.getMove()
			if move == 0:
				print "No moves. Blue loses!"
				loss = True
				break
			#print move
			if move:
				stratego.movePiece(move, stratego.getBoard())
				stratego.printGame()
				stratego.showLastMove()
				break

		if loss:
			stratego.printGame()
			break


#simulates given number of games between the AI and random player
simulate(20)

#simulates one game between the AI and random player showing every move
#simOneGame()



