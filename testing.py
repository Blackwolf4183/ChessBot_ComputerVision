import cv2 as cv
import numpy as np
import os
import imutils
from chessBoardDetection import ChessBoardAnalizer
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


print(isBlankSquare(chess_square))




needle_img = cv.imread("./template_images/white_knight.png",0)
needle_img = cv.Canny(needle_img,100,200)
(tH, tW) = needle_img.shape[:2]

#showImage("board",cropped_chessboard)
#showImage("needle",needle_img)

found = None

for scale in np.linspace(0.2, 2, 20)[::-1]:
    resized = imutils.resize(chess_square, width = int(chess_square.shape[1] * scale))
    #showImage("result" ,result)
    r = chess_square.shape[1] / float(resized.shape[1])

    #Si el template es más grande que la imagen cambiada de tamaño
    if resized.shape[0] < tH or resized.shape[1] < tW:
        break

    chess_square_edged = cv.Canny(resized,100,200)
    result = cv.matchTemplate(chess_square_edged, needle_img, cv.TM_CCORR_NORMED)
    _, maxVal, _, maxLoc = cv.minMaxLoc(result)

    print("maxVal is: " ,maxVal)

    #DEBUG
    clone = np.dstack([chess_square_edged, chess_square_edged, chess_square_edged])
    cv.rectangle(clone, (maxLoc[0], maxLoc[1]),
        (maxLoc[0] + tW, maxLoc[1] + tH), (0, 0, 255), 2)
    cv.imshow("Visualize", clone)
    ####

    if found is None or maxVal > found[0]:
        found = (maxVal, maxLoc, r)

    _, maxLoc, r = found
    (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
    (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
    # draw a bounding box around the detected result and display the image
    cv.rectangle(chess_square, (startX, startY), (endX, endY), (0, 0, 255), 2)
    cv.imshow("Image", chess_square)
    cv.waitKey(0)

    


cv.destroyAllWindows()