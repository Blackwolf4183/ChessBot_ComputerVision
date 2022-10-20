import cv2 as cv
import numpy as np
import os
import random
import math

#################################

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Nombro la ventana
cv.namedWindow("Cuadrado", cv.WINDOW_NORMAL)
  
# Reajustamos el tamaño de la ventana
cv.resizeWindow("Cuadrado", 1000, 1000)

def showImage(name,img): # Funcion para mostrar la imagen
    cv.imshow(name,img)

#################################


#Importamos imagen
img = cv.imread('./test_images/test_image.png',cv.IMREAD_UNCHANGED)
#Sacamos Canny para los bordes porque si sacamos los contornos directamente no funciona por el ruido
edges = cv.Canny(img,100,200)


#Cogemos los contornos de la imagen
contours, _ = cv.findContours(edges,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)

#Suma máxima del tamaño de los contornos (width + height)
maxSum = 0
#Aquí almacenamos el contorno más grande en perímetro/2
contornoMax = []
#Variables para luego cropear la imagen
xSquare = ySquare = wSquare = hSquare = 0


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
cv.putText(img,'Square',(x1,y1),cv.FONT_HERSHEY_SIMPLEX,0.6,(255,255,0),2)

#TODO: cambiar nombre
img = img[ySquare:ySquare+hSquare,xSquare:xSquare+wSquare] # Recorte de la imagen



#showImage("Cuadrado", img)


square_edges = cv.Canny(img,100,200)

img_width = square_edges.shape[0]
square_size = int(img_width/8) # Tamaño del lado del cuadrado

#Array que contenga las posiciones de arriba izquierda de los cuadrados
squares_arr = []

for f in range(8):
    for c in range(8):
        squares_arr.append((int(f * square_size),int(c * square_size)))

        

print(squares_arr)

#TODO: Estructura de datos con el numero maximo de cada pieza
#Empezamos solo detectando peones
num_p = 0

pawn_img = cv.imread('pawn.png',cv.IMREAD_UNCHANGED)
peon_w = pawn_img.shape[1]
peon_h = pawn_img.shape[0]

#TODO: temporal
threshold = 0.6

def detectarPeon(cell,count): #FIXME: temporal
    result = cv.matchTemplate(cell,pawn_img,cv.TM_CCOEFF_NORMED)
    #if count == 55: 
    #showImage("Celda" + str(count), result)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    print("PRECISION: " , max_val)
    if max_val >= threshold: 
        print("PEON")
    

#TODO: PONER NOMBRES DE VARIABLES REALES
count = 0 #FIXME: temporal
for (x,y) in squares_arr: #Recorremos los cuadrados pintando cada contorno
    count = count+1
    top_left = (x,y)
    bottom_right = (x+square_size,y+square_size)
    cv.rectangle(img, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

    #Cropeamos las imagenes
    chess_square = img[x:x+square_size,y:y+square_size]
    detectarPeon(chess_square,count)
    #showImage("Celda" + str(count), chess_square)


showImage("Cuadrado", img) # Enseñar cuadrados con los contornos dibujados


#Iteración de los cuadrados y detección de piezas



cv.waitKey(0)
cv.destroyAllWindows()

