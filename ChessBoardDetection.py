from turtle import update
import cv2 as cv
import numpy as np
import os
from chess import Chess
from utils import showImage,isBlankSquare
from matplotlib import pyplot as plt

#Poner el path relativo
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class ChessBoardAnalizer:

    filename2piece = {
        "./template_images\\black_pawn.png": -1,
        "./template_images\\black_knight.png": -2,
        "./template_images\\black_bishop.png": -3,
        "./template_images\\black_rook.png": -4,
        "./template_images\\black_queen.png": -5,
        "./template_images\\black_king.png": -6,
        "./template_images\\white_pawn.png": 1,
        "./template_images\\white_knight.png": 2,
        "./template_images\\white_bishop.png": 3,
        "./template_images\\white_rook.png": 4,
        "./template_images\\white_queen.png": 5,
        "./template_images\\white_king.png": 6,
        "NONE": 0
    }

    def __init__(self, image):
        self.board = image

    

    def getContours(self):
        #Sacamos Canny para los bordes porque si sacamos los contornos directamente no funciona por el ruido
        edges = cv.Canny(self.board, 100, 200)
        #showImage("Edges", edges)
        #Cogemos los contornos de la imagen
        contours, _ = cv.findContours(edges, cv.RETR_TREE,
                                      cv.CHAIN_APPROX_SIMPLE)
        return contours

    def findBoard(self, contours):
        #FIXME: Hay bug en el que con algunos tamaños más pequeños de tabla no la reconoce
        #Suma máxima del tamaño de los contornos (width + height)
        maxSum = 0
        #Aquí almacenamos el contorno más grande en perímetro/2
        contornoMax = []
        #Variables para luego cropear la imagen
        xSquare, ySquare, wSquare, hSquare = 0, 0, 0, 0
        #Iteramos los contornos
        for cnt in contours:
            x1, y1 = cnt[0][0]
            approx = cv.approxPolyDP(cnt, 0.05 * cv.arcLength(cnt, True), True)
            if len(approx) == 4:
                x, y, w, h = cv.boundingRect(cnt)
                ratio = float(w) / h
                
                if w + h > maxSum and 0.9 <= ratio <= 1.1:  # Buscamos el cuadrado mas grande con la suma de ancho y alto
                    maxSum = w + h
                    contornoMax = cnt
                    xSquare, ySquare, wSquare, hSquare = x, y, w, h  # Guardamos el cuadrado para recortar
        #Dibujar contornos
        self.board = cv.drawContours(self.board, [contornoMax], -1,
                                     (0, 255, 0), 3)
        cropped_chessboard = self.board[ySquare:ySquare + hSquare,
                                        xSquare:xSquare +
                                        wSquare]  # Recorte de la imagen
        
        return cropped_chessboard

    def divideSquares(self, cropped_board):
        #Aplicamos Canny para sacar las casillas del tablero
        square_edges = cv.Canny(cropped_board, 100, 200)
        img_width = square_edges.shape[0]
        square_size = int(img_width / 8)  # Tamaño del lado del cuadrado
        #Array que contenga las posiciones de arriba izquierda de los cuadrados
        squares_arr = []
        #Añadimos las posiciones en la pantalla de los cuadrados
        for f in range(8):
            for c in range(8):
                squares_arr.append(
                    (int(f * square_size), int(c * square_size)))

        #print(squares_arr)
        return squares_arr, square_size

    def classifyPieces(self, squares_array, square_size, cropped_chessboard):

        #Iteramos por todos los cuadrados y vamos añadiendo piezas
        directory = './template_images'
        precision_values = []
        chess = Chess()

        for (x, y) in squares_array:
            #Cropeamos las imagenes
            chess_square = cropped_chessboard[x:x + square_size,
                                              y:y + square_size]

            #Filtramos primero si es un cuadrado sin nada
            if isBlankSquare(chess_square):
                continue

            chess_square = cv.Canny(chess_square, 100, 200)

            for filename in os.listdir(directory):
                f = os.path.join(directory, filename)
                # checking if it is a file
                if os.path.isfile(f):
                    current_img = cv.imread(f, 0)
                    result = cv.matchTemplate(chess_square, current_img,
                                              cv.TM_CCORR_NORMED)
                    #showImage("result" + filename, result)
                    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
                    if max_val > 0.1:
                        precision_values.append((f, max_val))
                    else:
                        precision_values.append(("NONE", max_val))

                    #print("Max val is: ", precision_values)

            #print(precision_values)

            top_piece = "",
            top_value = -100

            for (name, precision) in precision_values:
                if precision > top_value:
                    top_value = precision
                    top_piece = name

            #posicionamiento en tablero virtual
            x_piece = int(x / int(square_size))
            y_piece = int(y / int(square_size))
            chess.setPiece(x_piece, y_piece, self.filename2piece[top_piece])

            #print("x: ", x_piece, " y: ", y_piece, " piece: " , filename2piece[top_piece])

            print("BEST MATCH: " , top_piece)

            top_value = -100
            top_piece = ""

            #Vaciamos array
            precision_values.clear()

        return chess


    def processBoard(self):
        contours = self.getContours()
        cropped_chessboard = self.findBoard(contours)
        squares_array, square_size = self.divideSquares(cropped_chessboard)
        updatedChess = self.classifyPieces(squares_array, square_size, cropped_chessboard)

        #Devolvemos el nuevo objeto Chess con las posiciones de las piezas actualizadas
        return updatedChess


""" 
#####################################################################

#TODO: temporal
pawn_img = cv.imread('./template_images/pawn.png',cv.IMREAD_UNCHANGED)
peon_w = pawn_img.shape[1]
peon_h = pawn_img.shape[0]


num_p = 0

threshold = 0.6

def detectarPeon(cell,count): #FIXME: temporal
    global num_p
    result = cv.matchTemplate(cell,pawn_img,cv.TM_CCOEFF_NORMED)
    #if count == 55: 
    #showImage("Celda" + str(count), result)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    print("PRECISION: " , max_val)
    if max_val >= threshold: 
        num_p = num_p + 1 
        print("PEON")
        
    

count = 0 #TODO: temporal
for (x,y) in squares_arr: #Recorremos los cuadrados pintando cada contorno
    top_left = (x,y)
    bottom_right = (x+square_size,y+square_size)
    cv.rectangle(cropped_chessboard, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

    #Cropeamos las imagenes
    chess_square = cropped_chessboard[x:x+square_size,y:y+square_size]
    detectarPeon(chess_square,count)
    #showImage("Celda" + str(count), chess_square)


showImage("Cuadrado", cropped_chessboard) # Enseñar cuadrados con los contornos dibujados


print(num_p)
##################################################################### """
