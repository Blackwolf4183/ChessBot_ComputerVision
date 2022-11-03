import cv2 as cv
import numpy as np
import os
import imutils
from ChessBoardDetection import ChessBoardAnalizer
from utils import isBlankSquare,isBlankSquare2,isPieceWhite, showImage,getBestScaleMatch
from matplotlib import pyplot as plt
import time
import math

os.chdir(os.path.dirname(os.path.abspath(__file__)))




img = cv.imread('./test_images/test_board_5.png')

analizer = ChessBoardAnalizer(img)
contours = analizer.getContours()
cropped_chessboard = analizer.findBoard(contours)
squares_array, square_size = analizer.divideSquares(cropped_chessboard)
chess_square = cropped_chessboard[square_size*4:square_size*4+square_size,square_size*2:square_size*2+square_size]

st = time.time()

isPieceWhite(chess_square)

et = time.time()
print("time: " ,et - st)


#showImage("Cropped", cropped_chessboard)


#Primer cuadrado del tablero con sus bordes en canny
showImage("Cuadrado",chess_square)

cv.waitKey(0)
cv.destroyAllWindows()