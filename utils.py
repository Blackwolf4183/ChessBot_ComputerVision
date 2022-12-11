import cv2 as cv
from collections import Counter
import numpy as np
from sklearn.cluster import KMeans
import imutils
import win32gui
import io
import chess

# Funcion para mostrar la imagen con tamaño variable
def showImage(name, img, w=800, h=800):
    cv.namedWindow(name, cv.WINDOW_NORMAL) # Nombro la ventana
    cv.resizeWindow(name, w, h) # Reajustamos el tamaño de la ventana
    cv.imshow(name, img)

# Lista los nombres de las ventanas abiertas
def listWindowNames():
        active_windows = []
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                active_windows.append(win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)
        
        return active_windows

def printArrayBoard(chess_array):
    for f in range(8):
        print("")
        for c in range(8):
            if(chess_array[f,c] < 0):
                print(chess_array[f,c], "|",end = '')
            else: 
                print(chess_array[f,c], " |",end = '')
    print("")

#Para transformar los valores numericos del array en valores ASCII para FEN
index2piece = {
    1: "p",
    2: "n",
    3: "b",
    4: "r",
    5: "q",
    6: "k",
}

def array2fen(chess_array,color):
    
    # StringIO es mas eficiente para concatenar
    with io.StringIO() as s:
        for row in range(8):
            empty = 0
            for cell in range(8):
                c = chess_array[row][cell]
                if c != 0:
                    if empty > 0:
                        s.write(str(empty))
                        empty = 0
                    #escribir en notación FEN la pieza
                    s.write(index2piece[abs(c)].upper() if c > 0 else index2piece[abs(c)].lower())
                else:
                    empty += 1
            if empty > 0:
                s.write(str(empty))
            s.write('/')
        # Move one position back to overwrite last '/'
        s.seek(s.tell() - 1)
        # Get the string from the StringIO object
        fen = s.getvalue()        
        # If the color parameter is "b", reverse the string
        if color == 'b':
            fen = fen[::-1]
            fen = fen[1:]
            fen += '/'
        
        return fen

def change_case(s):
    return "".join([c.lower() if c.isupper() else c.upper() for c in s])

def completeFENString(fen,color):

    # Normalizamos la string FEN y la printeamos
    fen = fen[0:len(fen)-1] 

    #FIXME: hay que ver como ponemos el final de la cadena para los openings
    fen = fen + " " + color + " KQkq - 0 1"

    print("FEN: " , fen)
    return fen


# Busca los nombres de ventana que contengan Chess.com
def findChessWindow():
    chessWindows = []

    for windowName in listWindowNames():
        if "Chess.com" in windowName:
            chessWindows.append(windowName)

    arr_len = len(chessWindows)

    if( arr_len == 1): 
        return chessWindows[0]
    elif(arr_len == 0):
        raise Exception("No se ha registrado ninguna partida en Chess.com")
    elif(arr_len > 1):
        raise Exception("Hay mas de una partida jugandose a la vez")


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
        #100 es el threshold de intensidad para considerar pixel blanco
        if pixel > 100: whitePixels = whitePixels +1

    #Si hay una proporcion grande de pixeles blancos (la ventana quizas se ha desplazado hacia un borde un poco)
    return whitePixels > int(flattened_img.shape[0]/1.5)


def getBestScaleMatch(original,template):
            
        (tH, tW) = template.shape[:2]

        found = None
        bestMatch = 0.0

        #FIXME: los parametros de linspace se puede alterar para buscar cuales son los mejores
        #FIXME: valores normales son 0.2,1 -- dependiendo de si nuestra imagen es más pequeña o más grande necesitaremos ajustar (quizas un script para sacar longitud de la captura y ver)
        for scale in np.linspace(0.2, 1.6, 25)[::-1]:
            #reescalamos la imagen original
            resized = imutils.resize(original, width = int(original.shape[1] * scale))
            #cogemos el ratio
            r = original.shape[1] / float(resized.shape[1])

            #Si el template es más grande que la imagen cambiada de tamaño
            if resized.shape[0] < tH or resized.shape[1] < tW:
                break

            #Aplicamos Canny a la imagen original
            original_edged = cv.Canny(resized,100,200)
            result = cv.matchTemplate(original_edged, template, cv.TM_CCORR_NORMED) 
            _, maxVal, _, maxLoc = cv.minMaxLoc(result) #Precision

            #print("maxVal is: " ,maxVal)

            if found is None or maxVal > found[0]:
                found = (maxVal, maxLoc, r)

            if maxVal > bestMatch:
                bestMatch = maxVal

        return bestMatch
    



def isBlankSquare3(image):

    global blank_square_threshold

    image = cv.cvtColor(image,cv.COLOR_BGR2RGB)
    #print(image)

    flattened_img = image.reshape((-1,3))
    result = np.unique(flattened_img, axis=0, return_counts = True)
    image_size = len(flattened_img)
    ocurrences = result[1]
    max_ocurrence = np.amax(ocurrences)

    #FIXME: hay que cambiar el umbral, porque los cuadrados señalados con circulos en los movimientos
    # de las piezas no los tiene en cuenta
    return max_ocurrence/image_size > 0.8
