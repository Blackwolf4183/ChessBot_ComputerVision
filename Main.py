import cv2 as cv
import numpy as np
from ChessBoardDetection import ChessBoardAnalizer
import time
import warnings
import utils
import pyautogui
import chess
from ChessIncrementalEval import ChessEngine
from autoMover import AutoMover

#para sklearn
warnings.filterwarnings("ignore")



def start(color):

    print("color is: " ,color)

    window_name = utils.findChessWindow()
    pyautogui.getWindowsWithTitle(window_name)[0].minimize()
    pyautogui.getWindowsWithTitle(window_name)[0].maximize()

    time.sleep(1)

    #Guardamos la ultima notacion fen del tablero 
    
    while True: 
        # INFO: variable para contar tiempo de inicio
        st = time.time()

        #TODO: extraer en funcione de utils todo esto
        # Tomamos captura y convertimos a formato opencv
        tablero = pyautogui.screenshot()
        tablero_opencv = np.array(tablero)  
        tablero_opencv = tablero_opencv[:, :, ::-1].copy()

        #cv.imshow('Computer Vision', tablero_opencv)

        # Inicializamos analizador por vision por computador
        chessBoardAnalizer = ChessBoardAnalizer(tablero_opencv)
        resulting_board ,x ,y ,square_size = chessBoardAnalizer.processBoard()


        # Mostramos el tablero virtualizado por consola
        utils.printArrayBoard(resulting_board)
        
        fen = utils.array2fen(resulting_board,color)
        fen = utils.completeFENString(fen,color)

        #TODO: hay que hacer sistema para que no mueva hasta que el oponente no hay movido


        # Creamos un tablero con la cadena FEN e inicializamos el motor
        board = chess.Board(fen)
        engine = ChessEngine(board)
        # Inicializamos AutoMover con los parámetros del tablero en la pantalla
        autoMover = AutoMover(x,y,square_size,color)

        # Encontramos el mejor movimiento con profundidad 4
        #FIXME: hay bug en el que añade una q a un movimiento que no sea el inicial con las piezas negras
        bestMove = engine.selectmove(4)
        print("Best move: ",  bestMove)
        
        # Movemos la pieza en la pantalla
        print("Moviendo pieza...")
        autoMover.movePiece(str(bestMove)[0:2],str(bestMove)[2:4])

        et = time.time()
        print("Time to execute: " , et-st)

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break

        time.sleep(2)






