import cv2
import cv2 as cv
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

img = cv.imread('./test_images/test_image.png')
gray_img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

#cv.imshow("Gray image",gray_img)

#Binarización de la imagen
ret,thresh = cv.threshold(gray_img,150,255,0)
#cv.imshow("Threshold",thresh)

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

