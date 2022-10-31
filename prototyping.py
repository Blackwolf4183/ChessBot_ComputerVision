import cv2 as cv
import numpy as np
import os
import imutils
from ChessBoardDetection import ChessBoardAnalizer
from utils import isBlankSquare, showImage,getBestScaleMatch
from matplotlib import pyplot as plt
import time
import math

os.chdir(os.path.dirname(os.path.abspath(__file__)))



def isPieceWhite(cropped_square):

    s_window = 5

    #Pasamos a gris
    cropped_square = cv.cvtColor(cropped_square,cv.COLOR_BGR2GRAY)
    
    w = cropped_square.shape[0]
    h = cropped_square.shape[1]
    center = (int(w/2),int(h/2))
    #print("w, h, center", w, h, center)
    #Cogemos una unica ventana en el centro de la imagen que es donde va a estar la pieza
    _, binarized_square = cv.threshold(cropped_square,127,255,cv.THRESH_BINARY)
    #marked_window = cv.rectangle(binarized_square, (center[0]-s_window,center[1]+int(w/4)), (center[0]+s_window,center[1]+int(w/3)), (255,0,0), 1)
    #showImage("Region", marked_window)
    cropped_square = binarized_square[center[1]+int(h/3.5):center[1]+int(h/3),center[0]-s_window:center[0]+s_window]
    #showImage("Cropped_region",cropped_square)

    whitePixels = 0
    flattened_img = np.array(cropped_square).flatten()
    for pixel in flattened_img:
        if pixel > 100: whitePixels = whitePixels +1

    #Si hay una proporcion grande de pixeles blancos (la ventana quizas se ha desplazado hacia un borde un poco)
    if whitePixels > int(flattened_img.shape[0]/1.5):
        return True
    else: 
        return False



img = cv.imread('./test_images/test_board_5.png')

analizer = ChessBoardAnalizer(img)

st = time.time()
contours = analizer.getContours()
cropped_chessboard = analizer.findBoard(contours)
et = time.time()
print("time: " ,et - st)

#showImage("Cropped", cropped_chessboard)

squares_array, square_size = analizer.divideSquares(cropped_chessboard)

#Primer cuadrado del tablero con sus bordes en canny
chess_square = cropped_chessboard[square_size*7:square_size*7+square_size,square_size*0:square_size*0+square_size]
showImage("Cuadrado",chess_square)




print(isPieceWhite(chess_square))




cv.waitKey(0)
cv.destroyAllWindows()