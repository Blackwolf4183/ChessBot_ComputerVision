import cv2 as cv
import numpy as np

chessboard = cv.imread('test_image.png',cv.IMREAD_UNCHANGED)
pawn_img = cv.imread('pawn.png',cv.IMREAD_UNCHANGED)

peon_w = pawn_img.shape[1]
peon_h = pawn_img.shape[0]

result = cv.matchTemplate(chessboard,pawn_img,cv.TM_CCOEFF_NORMED)

threshold = 0.6

#localizaciones donde hay puntos con mas que el threshold
locations = np.where(result >= threshold) # me devuelve dos arrays, el primero con las posiciones en y, y el segundo con las posiciones en x

#revierte el orden de los arrays y combina cada uno de los elementos de cada array en una tupla
locations = list(zip(*locations[::-1]))
#print(locations)

# primero creamos una lista de rectangulos del tipo [x,y,w,h]
rectangles = []

for loc in locations:
    rect = [int(loc[0]),int(loc[1]),peon_w,peon_h]
    rectangles.append(rect)
    #Lo hacemos dos veces para que al menos cada rectangulo tenga un overlap, y así cuando hagamos groupRectangles no desaparezcan los matches debiles
    rectangles.append(rect)
print("RECTANGULOS:")


#agrupamos los matches en la misma region
rectangles, weights = cv.groupRectangles(rectangles,1,0.5)
print(rectangles)


if len(rectangles):

    for (x,y,w,h) in rectangles:

        top_left = (x,y)
        bottom_right = (x+w,y+h)
        cv.rectangle(chessboard, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)


    cv.imshow("Matches", chessboard)
    cv.waitKey()


"""


#el mejor match
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)


if max_val >= threshold:
    print("Se ha encontrado un peon con confidence: %f",max_val)

    # dimensiones del peon
    peon_w = pawn_img.shape[1]
    peon_h = pawn_img.shape[0]

    top_left = max_loc
    bottom_right = (top_left[0] + peon_w,top_left[1] + peon_h)

    cv.rectangle(chessboard,top_left,bottom_right,color=(0,255,0),thickness=2,lineType=cv.LINE_4)
    cv.imshow("Result", chessboard)
    cv.waitKey(0)

"""
