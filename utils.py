import cv2 as cv
from collections import Counter
import numpy as np
from sklearn.cluster import KMeans
import imutils

# Funcion para mostrar la imagen
def showImage(name, img, w=800, h=800):
    cv.namedWindow(name, cv.WINDOW_NORMAL) # Nombro la ventana
    cv.resizeWindow(name, w, h) # Reajustamos el tamaño de la ventana
    cv.imshow(name, img)


def palettePerc(k_cluster):
    
    n_pixels = len(k_cluster.labels_)
    #Numero de pixeles por cluster
    counter = Counter(k_cluster.labels_) 
    perc = {}
    for i in counter:
        perc[i] = np.round(counter[i]/n_pixels, 2)
    perc = dict(sorted(perc.items()))
    
    return perc

#FIXME: hay que ajustarlo para mejores resultados
blank_square_threshold = 0.91

#FIXME: hay cuadrados que no pilla bien
def isBlankSquare(image):
    
    global blank_square_threshold

    rgb_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    #FIXME: con 2 clusters se raya hay que poner mas?
    clt = KMeans(n_clusters=3)
    clt.fit(rgb_image.reshape(-1,3))
    percentages = palettePerc(clt)
    
    #print("Percentage", percentages)
    max_val = 0

    #Iteramos en un diccionario {0: 0.95, 1: 0.02, 2:0.05 ...}
    for perc in percentages:
        if percentages[perc] > max_val:
            max_val = percentages[perc]

    #print("MAX VAL IS:" , max_val)
    #print("percentages: " , percentages)

    if max_val >= blank_square_threshold:
        return True
    else:
        return False

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

def getBestScaleMatch(original,template):
            
        (tH, tW) = template.shape[:2]

        found = None
        bestMatch = 0.0

        #FIXME: los parametros de linspace se puede alterar para buscar cuales son los mejores
        #FIXME: valores normales son 0.2,1 -- dependiendo de si nuestra imagen es más pequeña o más grande necesitaremos ajustar (quizas un script para sacar longitud de la captura y ver)
        for scale in np.linspace(0.2, 1.6, 20)[::-1]:
            #reescalamos la imagen original
            resized = imutils.resize(original, width = int(original.shape[1] * scale))

            #cogemos el ratio
            r = original.shape[1] / float(resized.shape[1])

            #Si el template es más grande que la imagen cambiada de tamaño
            if resized.shape[0] < tH or resized.shape[1] < tW:
                break

            #Aplicamos Canny a la imagen original
            original_edged = cv.Canny(resized,100,200)
            #TODO:REMOVE
            #showImage("Original_edged" + str(scale), original_edged)
            result = cv.matchTemplate(original_edged, template, cv.TM_CCORR_NORMED)
            #Calculamos la precisión del match
            _, maxVal, _, maxLoc = cv.minMaxLoc(result)

            #print("maxVal is: " ,maxVal)

            if found is None or maxVal > found[0]:
                found = (maxVal, maxLoc, r)

            if maxVal > bestMatch:
                bestMatch = maxVal

        return bestMatch
    