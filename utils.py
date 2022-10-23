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

blank_square_threshold = 0.9

def isBlankSquare(image):

    global blank_square_threshold

    rgb_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    clt = KMeans(n_clusters=2)
    clt.fit(rgb_image.reshape(-1,3))
    percentages = palettePerc(clt)
    
    #print("Percentage", percentages)
    max_val = 0

    #Iteramos en un diccionario {0: 0.95, 1: 0.02, 2:0.05 ...}
    for perc in percentages:
        if percentages[perc] > max_val:
            max_val = percentages[perc]

    if max_val >= blank_square_threshold:
        return True
    else:
        return False

def getBestScaleMatch(original,template):
            
        (tH, tW) = template.shape[:2]

        found = None
        bestMatch = 0.0

        #FIXME: los parametros de linspace se puede alterar para buscar cuales son los mejores
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
    