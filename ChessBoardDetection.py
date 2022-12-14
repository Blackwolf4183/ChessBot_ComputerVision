import cv2 as cv
import numpy as np
import os
import math
from utils import showImage,isBlankSquare3,getBestScaleMatch,isPieceWhite,array2fen

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
    }

    def __init__(self, image):
        self.board = image

    

    def getContours(self):

        #Pasamos a gris la imagen
        gray = cv.cvtColor(self.board, cv.COLOR_BGR2GRAY)
        #Hacemos un threshold
        th = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,9,2)
        #showImage("Threshold Image", th)
        
        #Cogemos los contornos de la imagen
        contours, _ = cv.findContours(th, cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        return contours

    def findBoard(self, contours):
        #Suma máxima del tamaño de los contornos (width + height)
        maxSum = 0
        #Aquí almacenamos el contorno más grande en perímetro/2
        contornoMax = []
        #Variables para luego cropear la imagen
        xSquare, ySquare, wSquare, hSquare = 0, 0, 0, 0
        #Iteramos los contornos
        for cnt in contours:
            approx = cv.approxPolyDP(cnt, 0.05 * cv.arcLength(cnt, True), True)
            if len(approx) == 4:
                x, y, w, h = cv.boundingRect(cnt)
                ratio = float(w) / h
                
                if w + h > maxSum and 0.9 <= ratio <= 1.1:  # Buscamos el cuadrado mas grande con la suma de ancho y alto
                    maxSum = w + h
                    contornoMax = cnt
                    xSquare, ySquare, wSquare, hSquare = x, y, w, h  # Guardamos el cuadrado para recortar

        #Dibujar contornos
        #REVIEW: le hemos quitado 5 pixeles por cada lado ya que con esto se queda perfecta la imagen en cada intento
        cropped_chessboard = self.board[ySquare+5:ySquare + hSquare -5,
                                        xSquare+5:xSquare +
                                        wSquare - 5]  # Recorte de la imagen
        #Dibujamos cuadrado para ver el tablero
        self.board = cv.drawContours(self.board, [contornoMax], -1, (0, 255, 0), 3)
        
        #Devolvemos imagen recortada y posicion en la pantalla
        return cropped_chessboard, xSquare, ySquare

    def divideSquares(self, cropped_board):

        img_width = cropped_board.shape[0] #Anchura del tablero
        square_size = int(img_width / 8)  # Tamaño del lado del cuadrado

        squares_arr = [] #Array que contenga las posiciones de arriba izquierda de los cuadrados

        #Añadimos las posiciones en la pantalla de los cuadrados
        for f in range(8):
            for c in range(8):
                squares_arr.append(
                    (int(f * square_size), int(c * square_size)))

        return squares_arr, square_size



    def classifyPieces(self, squares_array, square_size, cropped_chessboard):

        #Iteramos por todos los cuadrados y vamos añadiendo piezas
        directory = './template_images'
        precision_values = []
        board = np.zeros((8,8), dtype=np.int)

        for (x, y) in squares_array:
            #Cropeamos las imagenes
            chess_square = cropped_chessboard[x:x + square_size,
                                              y:y + square_size]
            #showImage("square" + str(x) + str(y), chess_square)

            #Filtramos primero si es un cuadrado sin nada
            if isBlankSquare3(chess_square):
                #Si no tiene nada continuamos a la siguiente iteración 
                continue 


            #showImage("square" + str(x) + str(y), chess_square)
            for filename in os.listdir(directory):
                f = os.path.join(directory, filename)
                # checking if it is a file
                if os.path.isfile(f):
                    current_img = cv.imread(f, 0)
                    best_match = getBestScaleMatch(chess_square,current_img)
                    #print("Best match is: ", best_match)
                    precision_values.append((f, best_match))
               
            #print(precision_values)

            top_piece = "",
            top_value = -math.inf

            for (name, precision) in precision_values:
                if precision > top_value:
                    top_value = precision
                    top_piece = name

            #posicionamiento en tablero virtual
            x_piece = int(x / int(square_size))
            y_piece = int(y / int(square_size))
            

            piece_value = self.filename2piece[top_piece]

            #Evaluamos si la pieza es blanca para cambiarle el valor
            if(isPieceWhite(chess_square)):
                piece_value = -piece_value

            #Metemos la pieza en la matriz
            board[x_piece][y_piece] =  piece_value

            #Vaciamos array
            precision_values.clear()


        return board


    def processBoard(self):
        contours = self.getContours()
        cropped_chessboard, x, y = self.findBoard(contours)
        squares_array, square_size = self.divideSquares(cropped_chessboard)
        updatedChess = self.classifyPieces(squares_array, square_size, cropped_chessboard)

        #Devolvemos el nuevo objeto Chess con las posiciones de las piezas actualizadas
        return updatedChess, x, y, square_size



