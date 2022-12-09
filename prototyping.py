import cv2 as cv
import os
from ChessBoardDetection import ChessBoardAnalizer
import utils
import time
from screenCapturer import ScreenCapture
import pyautogui
from ChessIncrementalEval import ChessEngine
from autoMover import AutoMover
import chess

os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    #Inicializacion de parametros
    window_name = utils.findChessWindow()
    screenCap = ScreenCapture(window_name)

    #Abrimos ventana
    pyautogui.getWindowsWithTitle(window_name)[0].minimize()
    pyautogui.getWindowsWithTitle(window_name)[0].maximize()

    # Game Loop
    print("Comienza la captura de imagen, no toque el teclado...")
    time.sleep(1)


    while(True):

        # get an updated image of the game
        screenshot = screenCap.get_screenshot()
        cv.imshow('Computer Vision', screenshot)


        chessBoardAnalizer = ChessBoardAnalizer(screenshot)
        resulting_board,fen, x, y, square_size = chessBoardAnalizer.processBoard()

        utils.printArrayBoard(resulting_board)
        print("FEN: ",fen)

        board = chess.Board(fen)
        engine = ChessEngine(board)
        print("Best move: ",  engine.selectmove(4))


        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break

            #Tiempo de 1 segundo entre capturas
      

except Exception as e:
    print(e)







""" img = cv.imread('./test_images/test_board_5.png',cv.IMREAD_UNCHANGED)

analizer = ChessBoardAnalizer(img)
contours = analizer.getContours()
cropped_chessboard = analizer.findBoard(contours)
squares_array, square_size = analizer.divideSquares(cropped_chessboard)
chess_square = cropped_chessboard[square_size*0:square_size*0+square_size,square_size*0:square_size*0+square_size]
utils.isPieceWhite(chess_square)

st = time.time()
for i in range(64):
    utils.isBlankSquare3(chess_square)

et = time.time()
print("time: " ,et - st)



#showImage("Cropped", cropped_chessboard)


#Primer cuadrado del tablero con sus bordes en canny
utils.showImage("Cuadrado",chess_square)

cv.waitKey(0)
cv.destroyAllWindows() """