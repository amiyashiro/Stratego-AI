# Stratego-AI

Group project for B351 AI course. Other group members: Nathan Krummen, Tian Jin.

This Stratego is the 10v10 version (8x8 board) and runs on the command line. All game mechanics are 
contained in main.py. AI.py contains logic for randomly selecting a move. pieces.py holds the classes for
each piece in the game. player.py is used to get a move from each player during play. AITwo.py contains the
logic for intelligently selecting a move. Our AI uses mini-max with alpha-beta pruning and random
configurations of the board (which we called 'musical chairs') to select the best move.
