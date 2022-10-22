import cv2 as cv
import numpy as np
from chess import Chess
from chessBoardDetection import ChessBoardAnalizer
import time

#TODO: Captura de imagenes a tiempo real
# ADD: Capturar hasta que haya un tablero
# ADD: tomar captura una vez se haya hecho un movimiento y luego esperar a que cambie el tablero para volver a mirar ()

#INFO: screenCapturer.py

#TODO: Actualizar si se está jugando una partida
# ADD: Función que devuelva True/False isChessBoard()
# ADD: Calcular turno (Quizás con los cuadrados amarillos)

#TODO: Si esta jugando partida analizar tablero
# ADD: Crear clases para piezas y hacer todas las piezas objetos
#INFO: #https://en.wikipedia.org/wiki/Board_representation_(computer_chess)
#INFO: https://github.com/jhlywa/chess.js LIBRERIA DE JS

st = time.time()

#Importamos imagen
tablero = cv.imread('./test_images/test_image.png',cv.IMREAD_UNCHANGED)

chessBoardAnalizer = ChessBoardAnalizer(tablero)
resulting_board = chessBoardAnalizer.processBoard()

resulting_board.printChessBoard()

et = time.time()

print("Time to execute: " , et-st)

cv.waitKey(0)
cv.destroyAllWindows()


#TODO: Si es mi turno, calculo mejor movimiento
# ADD: Lo ejecuto con ratón y teclado
# INFO: https://www.freecodecamp.org/news/simple-chess-ai-step-by-step-1d55a9266977/  chess ai




"""

#el mejor match
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)


if max_val >= threshold:
    print("Se ha encontrado un peon con confidence: %f",max_val)

    # dimensiones del peon
    peon_w = pawn_img.shape[1]
    peon_h = pawn_img.shape[0]

    top_left = max_loc
    bottom_right = (top_left[0] + peon_w,top_left[1] + peon_h)

    cv.rectangle(chessboard,top_left,bottom_right,color=(0,255,0),thickness=2,lineType=cv.LINE_4)
    cv.imshow("Result", chessboard)
    cv.waitKey(0)

"""
