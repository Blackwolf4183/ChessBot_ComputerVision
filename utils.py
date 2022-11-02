import cv2 as cv
from collections import Counter
import numpy as np
from sklearn.cluster import KMeans
import imutils

# Funcion para mostrar la imagen con tamaño variable
def showImage(name, img, w=800, h=800):
    cv.namedWindow(name, cv.WINDOW_NORMAL) # Nombro la ventana
    cv.resizeWindow(name, w, h) # Reajustamos el tamaño de la ventana
    cv.imshow(name, img)


def palettePerc(k_cluster):
    
    n_pixels = len(k_cluster.labels_)
    counter = Counter(k_cluster.labels_) 
    perc = {}
    for i in counter:
        perc[i] = np.round(counter[i]/n_pixels, 2)
    perc = dict(sorted(perc.items()))
    
    return perc


blank_square_threshold = 0.91


def isBlankSquare(image):
    
    global blank_square_threshold

    rgb_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    clt = KMeans(n_clusters=3)
    clt.fit(rgb_image.reshape(-1,3))
    percentages = palettePerc(clt)
    
    #print("Percentage", percentages)
    max_val = 0

    #Iteramos en un diccionario {0: 0.95, 1: 0.02, 2:0.05 ...}
    for perc in percentages:
        if percentages[perc] > max_val:
            max_val = percentages[perc]

    return max_val >= blank_square_threshold




def isPieceWhite(cropped_square):
    s_window = 5

    #Pasamos a gris
    cropped_square = cv.cvtColor(cropped_square,cv.COLOR_BGR2GRAY)
    
    w = cropped_square.shape[0]
    h = cropped_square.shape[1]
    center = (int(w/2),int(h/2))
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
    return whitePixels > int(flattened_img.shape[0]/1.5)


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
    




#FIXME: intentos de mejora de kmeans
def countPixels(clustered_image,center,img_size):

    ocurrences = {}

    counter = 0
    for color in center:
        amount = np.count_nonzero(np.all(np.array(clustered_image)==np.array(color),axis=2))
        ocurrences[counter] = round(amount/img_size,2)
        counter += 1
        
    return ocurrences


def isBlankSquare2(image):
    global blank_square_threshold

    rgb_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    flattened_img = rgb_image.reshape((-1,3))
    flattened_img = np.float32(flattened_img)

    K = 3
    #FIXME: 30 en pc grande - 35 en portatil para que funcione
    it = 30

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, it, 1.0)
    _,label,center=cv.kmeans(flattened_img,K,None,criteria,it,cv.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)

    res = center[label.flatten()]
    res2 = res.reshape((rgb_image.shape))
    #showImage("res",res2)

    #Obtenemos el array con las apariciones de cada pixel
    percentages = countPixels(res2,center,len(flattened_img))
    #print(percentages)


    max_val = 0
    #Iteramos en un diccionario {0: 0.95, 1: 0.02, 2:0.05 ...}
    for perc in percentages:
        if percentages[perc] > max_val:
            max_val = percentages[perc]

    return max_val >= blank_square_threshold

