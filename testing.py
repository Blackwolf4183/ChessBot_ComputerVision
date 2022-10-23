import cv2 as cv
import numpy as np
import os
import imutils
from ChessBoardDetection import ChessBoardAnalizer
from utils import isBlankSquare, showImage
from matplotlib import pyplot as plt



os.chdir(os.path.dirname(os.path.abspath(__file__)))

img = cv.imread('./test_images/test_image.png',cv.IMREAD_UNCHANGED)
analizer = ChessBoardAnalizer(img)

contours = analizer.getContours()
cropped_chessboard = analizer.findBoard(contours)
squares_array, square_size = analizer.divideSquares(cropped_chessboard)

#Primer cuadrado del tablero con sus bordes en canny
chess_square = cropped_chessboard[square_size*6:square_size*6+square_size,square_size*1:square_size*1+square_size]


showImage("cuadrado",chess_square)


#Cogemos la imagen template y la pasamos a canny
needle_img = cv.imread("./template_images/black_pawn.png",0)


#Scamos sus dimensiones








def getBestScaleMatch(original,template):

    template = cv.Canny(template,100,200)
    (tH, tW) = template.shape[:2]

    found = None
    bestMatch = 0.0

    for scale in np.linspace(0.2, 1, 20)[::-1]:
        #reescalamos la imagen original
        resized = imutils.resize(original, width = int(original.shape[1] * scale))

        #cogemos el ratio
        r = original.shape[1] / float(resized.shape[1])

        #Si el template es más grande que la imagen cambiada de tamaño
        if resized.shape[0] < tH or resized.shape[1] < tW:
            break

        #Aplicamos Canny a la imagen original
        original_edged = cv.Canny(resized,100,200)
        result = cv.matchTemplate(original_edged, template, cv.TM_CCORR_NORMED)
        #Calculamos la precisión del match
        _, maxVal, _, maxLoc = cv.minMaxLoc(result)

        #print("maxVal is: " ,maxVal)

        if found is None or maxVal > found[0]:
            found = (maxVal, maxLoc, r)

        if maxVal > bestMatch:
            bestMatch = maxVal

    return bestMatch


print(getBestScaleMatch(chess_square,needle_img))

cv.waitKey(0)
cv.destroyAllWindows()