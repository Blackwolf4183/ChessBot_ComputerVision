from tkinter.messagebox import showinfo
import cv2 as cv
import numpy as np
import os
from chess import Chess
import imutils


os.chdir(os.path.dirname(os.path.abspath(__file__)))

def showImage(name,img,w=800,h=800): # Funcion para mostrar la imagen
    # Nombro la ventana
    cv.namedWindow(name, cv.WINDOW_NORMAL)
    # Reajustamos el tamaño de la ventana
    cv.resizeWindow(name, w, h)
    cv.imshow(name,img)

img = cv.imread('./test_images/test_image.png',0)

edges = cv.Canny(img,100,200)
#Cogemos los contornos de la imagen
contours, _ = cv.findContours(edges,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)

#Suma máxima del tamaño de los contornos (width + height)
maxSum = 0
#Aquí almacenamos el contorno más grande en perímetro/2
contornoMax = []
#Variables para luego cropear la imagen
xSquare, ySquare, wSquare, hSquare = 0,0,0,0


#Iteramos los contornos
for cnt in contours:
    x1,y1 = cnt[0][0]
    approx = cv.approxPolyDP(cnt,0.01*cv.arcLength(cnt,True),True)
    if len(approx) == 4:
        x, y, w, h = cv.boundingRect(cnt)
        ratio = float(w)/h

        if w + h > maxSum and 0.9 <= ratio <= 1.1: # Buscamos el cuadrado mas grande con la suma de ancho y alto
                maxSum = w + h
                contornoMax = cnt
                xSquare,ySquare,wSquare,hSquare = x,y,w,h # Guardamos el cuadrado para recortar


#Texto y dibujar contornos
img = cv.drawContours(img,[contornoMax],-1,(0,255,0),3)
cropped_chessboard = img[ySquare:ySquare+hSquare, xSquare:xSquare+wSquare] # Recorte de la imagen


square_edges = cv.Canny(cropped_chessboard,100,200)

img_width = square_edges.shape[0]
square_size = int(img_width/8) # Tamaño del lado del cuadrado

#Array que contenga las posiciones de arriba izquierda de los cuadrados
squares_arr = []

#Añadimos las posiciones en la pantalla de los cuadrados
for f in range(8):
    for c in range(8):
        squares_arr.append((int(f * square_size),int(c * square_size)))


first_Square = square_edges[0] #(x,y)

chess_square = cropped_chessboard[first_Square[0]:first_Square[0]+square_size,first_Square[1]:first_Square[1]+square_size]
chess_square = cv.Canny(chess_square,100,200)

showImage("cuadrado",chess_square)
needle_img = cv.imread("./template_images/black_king.png",0)
(tH, tW) = needle_img.shape[:2]

showImage("board",cropped_chessboard)
showImage("needle",needle_img)

found = None

for scale in np.linspace(0.2, 1.0, 20)[::-1]:
    resized = imutils.resize(needle_img, width = int(needle_img.shape[1] * scale))
    #result = cv.matchTemplate(cropped_chessboard,needle_img,cv.TM_CCORR_NORMED)
    #showImage("result" ,result)
    r = needle_img.shape[1] / float(resized.shape[1])

    if resized.shape[0] < tH or resized.shape[1] < tW:
        break

cv.waitKey(0)
cv.destroyAllWindows()