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



""" 
def slope(x1, y1, x2, y2): # Line slope given two points:
    return (y2-y1)/(x2-x1)

def angle(s1, s2): 
    return math.degrees(math.atan((s2-s1)/(1+(s2*s1))))



def getHoughLines(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    # Apply edge detection method on the image
    edges = cv.Canny(gray, 50, 150, apertureSize=3)
    
    # This returns an array of r and theta values
    lines = cv.HoughLines(edges, 1, np.pi/180, 200)
    

    lineArray = []
    # The below for loop runs till r and theta values
    # are in the range of the 2d array
    for r_theta in lines:
        arr = np.array(r_theta[0], dtype=np.float64)
        r, theta = arr
        # Stores the value of cos(theta) in a
        a = np.cos(theta)
    
        # Stores the value of sin(theta) in b
        b = np.sin(theta)
    
        # x0 stores the value rcos(theta)
        x0 = a*r
    
        # y0 stores the value rsin(theta)
        y0 = b*r
    
        # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
        x1 = int(x0 + 1000*(-b))
    
        # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
        y1 = int(y0 + 1000*(a))
    
        # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
        x2 = int(x0 - 1000*(-b))
    
        # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
        y2 = int(y0 - 1000*(a))
    
        # cv.line draws a line in img from the point(x1,y1) to (x2,y2).
        # (0,0,255) denotes the colour of the line to be
        # drawn. In this case, it is red.
        lineArray.append([(x1,y1),(x2,y2)])
        cv.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)



    showImage("hough", img)

st = time.time()
getHoughLines(img)
et = time.time()
print("time: " ,et - st) """

img = cv.imread('./test_images/test_board_9.png')

analizer = ChessBoardAnalizer(img)

contours = analizer.getContours()
st = time.time()
cropped_chessboard = analizer.findBoard(contours)
et = time.time()
print("time: " ,et - st)

showImage("Cropped", cropped_chessboard)

squares_array, square_size = analizer.divideSquares(cropped_chessboard)



#Primer cuadrado del tablero con sus bordes en canny
chess_square = cropped_chessboard[square_size*2:square_size*2+square_size,square_size*1:square_size*1+square_size]


showImage("cuadrado",chess_square)


#Cogemos la imagen template y la pasamos a canny
needle_img = cv.imread("./template_images/black_pawn.png",0)
#needle_img = cv.imread("./template_images/transparent_canny/black_king.png",0)

#print(getBestScaleMatch(chess_square,needle_img))

print("isblank: " , isBlankSquare(chess_square))

cv.waitKey(0)
cv.destroyAllWindows()