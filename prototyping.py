import cv2 as cv
import numpy as np
import os
import imutils
from ChessBoardDetection import ChessBoardAnalizer
import utils
from matplotlib import pyplot as plt
import time
import math

os.chdir(os.path.dirname(os.path.abspath(__file__)))




img = cv.imread('./test_images/test_board_5.png',cv.IMREAD_UNCHANGED)

analizer = ChessBoardAnalizer(img)
contours = analizer.getContours()
cropped_chessboard = analizer.findBoard(contours)
squares_array, square_size = analizer.divideSquares(cropped_chessboard)
chess_square = cropped_chessboard[square_size*5:square_size*5+square_size,square_size*0:square_size*0+square_size]
utils.isPieceWhite(chess_square)

st = time.time()

print(utils.isBlankSquare3(chess_square)) 

et = time.time()
print("time: " ,et - st)



#showImage("Cropped", cropped_chessboard)


#Primer cuadrado del tablero con sus bordes en canny
utils.showImage("Cuadrado",chess_square)

cv.waitKey(0)
cv.destroyAllWindows()