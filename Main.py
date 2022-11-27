import cv2 as cv
import numpy as np
from ChessBoardDetection import ChessBoardAnalizer
from screenCapturer import ScreenCapture
import time
import warnings

#para sklearn
warnings.filterwarnings("ignore")

#TODO: Captura de imagenes a tiempo real
# ADD: Capturar hasta que haya un tablero
# ADD: tomar captura una vez se haya hecho un movimiento y luego esperar a que cambie el tablero para volver a mirar ()

#INFO: screenCapturer.py
#screenCapturer = ScreenCapturer


#TODO: Actualizar si se está jugando una partida
# ADD: Función que devuelva True/False isChessBoard()
# ADD: Calcular turno (Quizás con los cuadrados amarillos)

#TODO: Si esta jugando partida analizar tablero
#INFO: #https://en.wikipedia.org/wiki/Board_representation_(computer_chess)
#INFO: https://github.com/jhlywa/chess.js LIBRERIA DE JS

#INFO: variable para contar tiempo de inicio

#Importamos imagen
st = time.time()
tablero = cv.imread('./test_images/mover.png',cv.IMREAD_UNCHANGED)

chessBoardAnalizer = ChessBoardAnalizer(tablero)
resulting_board,_ ,x,y,square_size = chessBoardAnalizer.processBoard()
print("x,y: ", x, y)
print("Square size: ", square_size)

et = time.time()

print("Time to execute: " , et-st)

cv.waitKey(0)
cv.destroyAllWindows()


#TODO: Si es mi turno, calculo mejor movimiento
# ADD: Lo ejecuto con ratón y teclado
# INFO: https://www.freecodecamp.org/news/simple-chess-ai-step-by-step-1d55a9266977/  chess ai



