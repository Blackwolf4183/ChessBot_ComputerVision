import cv2 as cv
import numpy as np
import os
import imutils
from ChessBoardDetection import ChessBoardAnalizer
from utils import isBlankSquare, showImage,getBestScaleMatch
from matplotlib import pyplot as plt



os.chdir(os.path.dirname(os.path.abspath(__file__)))

img = cv.imread('./test_images/test_image.png',cv.IMREAD_UNCHANGED)
analizer = ChessBoardAnalizer(img)

contours = analizer.getContours()
cropped_chessboard = analizer.findBoard(contours)
squares_array, square_size = analizer.divideSquares(cropped_chessboard)

#Primer cuadrado del tablero con sus bordes en canny
chess_square = cropped_chessboard[square_size*0:square_size*0+square_size,square_size*4:square_size*4+square_size]


showImage("cuadrado",chess_square)


#Cogemos la imagen template y la pasamos a canny
needle_img = cv.imread("./template_images/black_king.png",0)
#needle_img = cv.imread("./template_images/transparent_canny/black_king.png",0)



print(getBestScaleMatch(chess_square,needle_img))

cv.waitKey(0)
cv.destroyAllWindows()