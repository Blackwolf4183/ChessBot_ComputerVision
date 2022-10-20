import cv2 as cv
import numpy as np
import os
import random

os.chdir(os.path.dirname(os.path.abspath(__file__)))

#Importamos imagen
img = cv.imread('./test_images/test_image.png')
#Sacamos Canny para los bordes
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

img = img[ySquare:ySquare+hSquare,xSquare:xSquare+wSquare] # Recorte de la imagen

# Nombro la ventana
cv.namedWindow("Cuadrados", cv.WINDOW_NORMAL)
  
# Reajustamos el tamaño de la ventana
cv.resizeWindow("Cuadrados", 1000, 1000)

cv.imshow('Cuadrados',img)
cv.waitKey(0)
cv.destroyAllWindows()
















# HOUGH
""" lines = cv.HoughLinesP(edges, 1, np.pi/180, 60, np.array([]), 120, 5)
print(lines)

for line in lines:
    for x1, y1, x2, y2 in line:
        cv.line(img, (x1, y1), (x2, y2), (20, 220, 20), 3)

# Naming a window
cv.namedWindow("Lineas", cv.WINDOW_NORMAL)
  
# Using resizeWindow()
cv.resizeWindow("Lineas", 1200, 700)

cv.imshow('Lineas',img)
cv.waitKey(0)
cv.destroyAllWindows() """


""" 
gray_img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

#cv.imshow("Gray image",gray_img)

#Binarización de la imagen
ret,thresh = cv.threshold(gray_img,150,255,0)
cv.imshow("Threshold",thresh)

#Contornos
contours, _ = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)

print("Numero de contornos: %i",len(contours))

for cnt in contours:
    x1,y1 = cnt[0][0]
    approx = cv2.approxPolyDP(cnt,0.01*cv.arcLength(cnt,True),True)
    if len(approx) == 4:
        x, y, w, h = cv2.boundingRect(cnt)
        ratio = float(w)/h
        if 0.9 <= ratio <= 1.1:
            img = cv.drawContours(img,[cnt],-1,(0,255,255),3)
            cv.putText(img,'Square',(x1,y1),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,0),2)

cv.imshow('Cuadrados',img)
cv.waitKey(0)
cv.destroyAllWindows()
 """
