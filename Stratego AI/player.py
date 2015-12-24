import random
import copy
from pieces import *

class Player():
	def __init__(self, team, board):
		self.team = team
		self.board = board
		self.ownPieces = [] 
		self.enemyPieces = []

	def updateBoard(self, newBoard):
		self.board = newBoard

	def getCurrentBoard(self):
		return self.board

	def getTeam(self):
		return self.team

	def getMyPieces(self):
		return self.ownPieces

	def getEnemyPieces(self):
		return self.enemyPieces

	def addMyPiece(self, piece):
		pieces = self.getMyPieces()
		pieces.append(piece)

	def addEnemyPiece(self, piece):
		enemyPieces = self.getEnemyPieces()
		enemyPieces.append(piece)


	def getMove(self): #asks player for a move, if valid returns move ((x1, y1) (x2, y2)) 
		columns = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8, 'j':9}
		board = self.getCurrentBoard()
		move = raw_input('Enter move (e.g. A4 B4, C8 C7, etc.): ')
		xtarget = columns[move[0].lower()]
		ytarget = int(move[1])
		xdest = columns[move[3].lower()]
		ydest = int(move[4])

		piece = board[ytarget][xtarget]
		if piece is None:
			print "Please choose a valid piece."
			return False
		elif not piece.getTeam() == self.getTeam():
			print "This is not your piece."
			return False

		if self.isValidMove(ytarget, xtarget, ydest, xdest, board):
			return ((ytarget, xtarget), (ydest, xdest))
		else:
			#not a valid move
			return False

	def isValidMove(self, ytarget, xtarget, ydest, xdest, board): #can you move piece at (xtarget, ytarget) to (xdest, ydest) on given board
		if board[ytarget][xtarget] == None:
			print "You don't have a piece in that spot."
			return False

		possibleMoves = self.getAllMoves(ytarget, xtarget, board)

		if (ydest, xdest) in possibleMoves:
			return True
		else:
			return False

	def checkSpot(self, row, col, team, board): #returns True if the given spot is empty or occupied by enemy piece, returns False if occupied by friendly
		spot = board[row][col]
		if spot is None:
			#spot is empty
			return True
		elif spot.getTeam() != team:
			#spot occupied by enemy
			return True
		else:
			#spot occupied by friendly
			return False	

	def getAllMoves(self, row, col, board): #returns list (list of tuples) of possible moves for piece at position (row, col)
		moves = []
		piece = board[row][col]
		team = piece.getTeam()
		ID = piece.getID()

		if ID == 'bmb' or ID == 'flg':
			return moves

		if ID == 'sct':
			#generate moves for scout
			ypos = row
			xpos = col
			while row > 0:
				row = row - 1
				if self.checkSpot(row, col, team, board):
					moves.append((row, col))					
					if not board[row][col] is None:
						#spot is occupied by enemy, must stop loop
						break
				else:
					break
			col = xpos
			row = ypos				
			while col > 0:
				col = col - 1
				if self.checkSpot(row, col, team, board):
					moves.append((row, col))					
					if not board[row][col] is None:
						break
				else:
					break
			col = xpos
			row = ypos		
			while row < 7:
				row = row + 1
				if self.checkSpot(row, col, team, board):
					moves.append((row, col))					
					if not board[row][col] is None:
						break
				else:
					break
			col = xpos
			row = ypos		
			while col < 7:
				col = col + 1
				if self.checkSpot(row, col, team, board):
					moves.append((row, col))					
					if not board[row][col] is None:
						break
				else:
					break	

			return moves
		else:
			if row > 0:
				if self.checkSpot(row - 1, col, team, board):
					moves.append((row - 1, col))
			if col > 0:
				if self.checkSpot(row, col - 1, team, board):
					moves.append((row, col - 1))
			if row < 7:
				if self.checkSpot(row + 1, col, team, board):
					moves.append((row + 1, col))
			if col < 7:
				if self.checkSpot(row, col + 1, team, board):
					moves.append((row, col + 1))
						
		return moves


	def setMusicalChairs(self):
		#randomly assigns each of the player's pieces a guess unless the piece is known
		ranks = [0, 11, 11, 1, 2, 2, 3, 3, 10, 9]
		movableRanks = [1, 2, 2, 3, 3, 10, 9]
		pieces = self.getMyPieces()[:]

		for piece in pieces:
			if piece.isKnown():
				#piece is already known, remove its rank so no other piece can be assigned it
				ranks.remove(piece.getRank())
				pieces.remove(piece)
				if piece.getRank() in movableRanks:
					movableRanks.remove(piece.getRank())

		for piece in pieces:
			if piece.hasMoved():
				#piece has moved but it is not known
				guess = random.choice(movableRanks)
				piece.setGuess(guess)
				movableRanks.remove(guess)
				ranks.remove(guess)
				pieces.remove(piece)
		
		for piece in pieces:
				#piece has not moved and is not known
				guess = random.choice(ranks)
				piece.setGuess(guess)
				ranks.remove(guess)
				if guess in movableRanks:
					movableRanks.remove(guess)


class Random(Player):
	def __init__(self, team, board):
		Player.__init__(self, team, board)

	def getType(self):
		return self.opponentType


	def getRandomPiece(self):
		pieces = self.getMyPieces()

		i = random.randint(0, 9)
		return pieces[i]

	def getRandomMove(self):
		allMoves = self.generateAllMoves(self.getCurrentBoard(), self.getTeam())
		keys = allMoves.keys()
		keyList = list(keys)

		i = len(keyList)
		for j in range(i):
			key = keyList[j]
			if not allMoves[key]:
				keys.remove(key)

		if keys == []:
			print 'No Moves'
			return 0

		piece = random.choice(keys)
		moves = allMoves[piece]
		move = random.choice(moves)

		return (piece, move)

	def getMove(self):
		return self.getRandomMove()

	#generates all possible moves for this player
	#dictionary: {location : [possible moves for piece]}
	def generateAllMoves(self, board, team):
		moves = {}
		pieceLocations = self.getAllPieces(board, team)

		for location in pieceLocations:
			newMoves = self.getAllMoves(location[0], location[1], board)
			moves[location] = newMoves
		return moves

	def getAllPieces(self, board, team):
		#gets all piece locations on the board
		pieceLocations = []

		for i in range(8):
			for j in range(8):
				piece = board[i][j]
				if not piece is None:
					if piece.getTeam() == team:
						pieceLocations.append((i, j))

		return pieceLocations

		



		