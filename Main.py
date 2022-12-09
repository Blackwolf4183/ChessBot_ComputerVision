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

    while True: 
        #INFO: variable para contar tiempo de inicio
        st = time.time()

        tablero = pyautogui.screenshot()
        tablero_opencv = np.array(tablero) 
        # Convert RGB to BGR 
        tablero_opencv = tablero_opencv[:, :, ::-1].copy()

        #cv.imshow('Computer Vision', tablero_opencv)

        chessBoardAnalizer = ChessBoardAnalizer(tablero_opencv)
        resulting_board ,fen ,x ,y ,square_size = chessBoardAnalizer.processBoard()

        utils.printArrayBoard(resulting_board)

        fen = fen[0:len(fen)-1]
        fen = fen + " " + color 
        print("FEN: ",fen)

        board = chess.Board(fen)
        engine = ChessEngine(board)
        #Automover
        autoMover = AutoMover(x,y,square_size)

        bestMove = engine.selectmove(4)

        print("Best move: ",  bestMove)
        
        #Movemos
        print("Moviendo pieza...")
        autoMover.movePiece(str(bestMove)[0:2],str(bestMove)[2:4])

        et = time.time()
        print("Time to execute: " , et-st)

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break

        print("Esperando al siguiente movimiento...")
        time.sleep(2)





