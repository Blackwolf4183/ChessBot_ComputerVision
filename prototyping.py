import cv2 as cv
import os
from ChessBoardDetection import ChessBoardAnalizer
import utils
import time
import pyautogui
from ChessIncrementalEval import ChessEngine
from autoMover import AutoMover
import chess

os.chdir(os.path.dirname(os.path.abspath(__file__)))


board = chess.Board("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")
engine = ChessEngine(board)

print(engine.selectmove(4))

#chessbot
#rnbqkbnr/pppp1ppp/4p3/8/3PP3/8/PPP2PPP/RNBQKBNR b KQkq d3 0 2

#mia
#RNBKQBNR/PPP2PPP/8/3PP3/8/3p4/ppp1pppp/rnbkqbnr b KQkq - 0 1

mover = AutoMover(586,167,99,'b')

mover.movePiece("g8","f6")