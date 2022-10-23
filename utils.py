import cv2 as cv
from collections import Counter
import numpy as np
from sklearn.cluster import KMeans

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


    