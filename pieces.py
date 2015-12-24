class Piece:
	def __init__(self):
		self.location = (-1, -1) #(row, col)
		self.rank = -1
		self.name = None
		self.team = None
		self.id = None
		self.moved = False
		self.known = False
		self.guess = None	

		self.numberOfMoves = 0
		#self.probDistribution = ProbabilityDistribution()

	def getName(self):
		return self.name

	def getTeam(self):
		return self.team

	def getID(self):
		return self.id

	def getLocation(self):
		return self.location

	def getRank(self):
		return self.rank

	def getNumberOfMoves(self):
		return self.numberOfMoves

	def hasMoved(self):
		return self.moved

	def firstTimeMoving(self):
		self.moved = True

	def addMove(self):
		self.numberOfMoves += 1

	def makeKnown(self):
		self.known = True

	def isKnown(self):
		return self.known

	def getGuess(self):
		return self.guess

	def setGuess(self, guess):
		self.guess = guess

	def getProbabilityDistribution(self):
		return self.probDistribution

	def setLocation(self, row, col):
		self.location = (row, col)

class NullPiece(Piece):
	def __init__(self):
		Piece.__init__(self)
		self.id = 'null'
		self.name = '_Empty_'

class Flag(Piece):
	def __init__(self, team):
		Piece.__init__(self)
		self.rank = 0
		self.name = 'Flg(00)'
		self.team = team
		self.id = 'flg'

class Bomb(Piece):
	def __init__(self, team):
		Piece.__init__(self)
		self.rank = 11
		self.name = 'Bmb(11)'
		self.team = team
		self.id = 'bmb'

class Spy(Piece):
	def __init__(self, team):
		Piece.__init__(self)
		self.rank = 1
		self.name = 'Spy(01)'
		self.team = team
		self.id = 'spy'

class Scout(Piece):
	def __init__(self, team):
		Piece.__init__(self)
		self.rank = 2
		self.name = 'Sct(02)'
		self.team = team
		self.id = 'sct'

class Miner(Piece):
	def __init__(self, team):
		Piece.__init__(self)
		self.rank = 3
		self.name = 'Min(03)'
		self.team = team
		self.id = 'min'

class Sergeant(Piece):
	def __init__(self, team):
		Piece.__init__(self)
		self.rank = 4
		self.name = 'Sgt(04)'
		self.team = team
		self.id = 'sgt'

class Lieutenant(Piece):
	def __init__(self, team):
		Piece.__init__(self)
		self.rank = 5
		self.name = 'Ltn(05)'
		self.team = team
		self.id = 'ltn'

class Captain(Piece):
	def __init__(self, team):
		Piece.__init__(self)
		self.rank = 6
		self.name = 'Cap(06)'
		self.team = team
		self.id = 'cap'

class Major(Piece):
	def __init__(self, team):
		Piece.__init__(self)
		self.rank = 7
		self.name = 'Maj(07)'
		self.team = team
		self.id = 'maj'

class Colonel(Piece):
	def __init__(self, team):
		Piece.__init__(self)
		self.rank = 8
		self.name = 'Col(08)'
		self.team = team
		self.id = 'col'

class General(Piece):
	def __init__(self, team):
		Piece.__init__(self)
		self.rank = 9
		self.name = 'Gen(09)'
		self.team = team
		self.id = 'gen'

class Marshall(Piece):
	def __init__(self, team):
		Piece.__init__(self)
		self.rank = 10
		self.name = 'Mar(10)'
		self.team = team
		self.id = 'mar'


class ProbabilityDistribution:
	def __init__(self):
		self.ranks = {'sct':2, 'bmb':11, 'min':3, 'flg':0, 'spy':1, 'mar':9, 'gen':10}
		self.distribution = {'sct':2, 'bmb':2, 'min':2, 'flg':1, 'spy':1, 'mar':1, 'gen':1}
		self.activePieces = 10

	def pieceSeen(self, pieceName):
		distribution = self.distribution
		if not distribution[pieceName] == 0:
			distribution[pieceName] = distribution[pieceName] - 1
			self.activePieces -= 1

	def chanceOfBeating(self, pieceRank):#probabilty that a piece of the given rank beats the piece this method is called with
		beatablePieces = []
		ranks = self.ranks
		for piece in ranks:
			if pieceRank > ranks[piece]:
				beatablePieces.append(piece)

		totalBeatablePieces = 0
		distribution = self.distribution
		for piece in beatablePieces:
			totalBeatablePieces += distribution[piece]

		chanceOfWinning = (float(totalBeatablePieces) / self.activePieces) * 100
		return chanceOfWinning

	def chanceOfTying(self, pieceID): 
		#probabiltiy that a piece of the given ID ties the piece this method is called with
		totalTyingPieces = self.distribution[pieceID]

		chanceOfTying = (float(totalTyingPieces) / self.activePieces) * 100
		return chanceOfTying

	def pieceMoved(self):
		distribution = self.distribution
		for piece in distribution:
			if piece == 'bmb' or piece == 'flg':
				distribution[piece] = 0
		self.activePieces -= 3


#import unittest

#class MyTest(unittest.TestCase):
#	def test(self):
#		distribution = ProbabilityDistribution()
#		self.assertEqual(distribution.chanceOfBeating(3), float(40))
#		self.assertEqual(distribution.chanceOfTying('sct'), float(20))
#		distribution.pieceSeen('spy')
#		self.assertEqual(distribution.chanceOfBeating(3), float(3)/9*100)
#		self.assertEqual(distribution.chanceOfTying('spy'), 0)
#		distribution.pieceMoved()
#		self.assertEqual(distribution.chanceOfTying('bmb'), 0)
#		self.assertEqual(distribution.chanceOfTying('flg'), 0)

#if __name__ == '__main__':
#	unittest.main()






