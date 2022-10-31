import numpy as np

class Chess:
    
    #12 x 12

    """
        PIECES:
        -PAWN:      1
        -KNIGHT:    2
        -BISHOP:    3
        -ROOK:      4
        -QUEEN:     5
        -KING:      6
         
        (NEGATIVE VALUES FOR BLACK PIECES)

    """


    def __init__(self): #Rellenar con 99 las filas extra que no pertenecen al tablero
        self.tablero = np.zeros((12,12), dtype=np.int)
        self.tablero[:,0:2] = 99
        self.tablero[:,10:12] = 99
        self.tablero[0:2,:] = 99
        self.tablero[10:12, :] = 99

    def setPiece(self, x, y, piece_keycode):
        if self.tablero[x+2,y+2] != 99: # Que no se salga del tablero
            self.tablero[x+2,y+2] = piece_keycode
    
    #Crear un tablero dado un array de una dimensión con las casillas ordenadas de arriba izquierda a abajo derecha
    def setLinearConfiguration(self, chessArray):
        self.tablero[2:10,2:10] = np.reshape(chessArray,(8,8))
    
    #Devuelve la matriz que contiene el tablero de ajedrez como tal
    def getInnerMatrix(self):
        return self.tablero[2:10,2:10]

    def removePiece(self, x, y):
        self.setPiece(x, y, 0)

    def printChessBoard(self):
        for f in range(8):
            print("")
            for c in range(8):
                if(self.tablero[f+2,c+2] < 0):
                    print(self.tablero[f+2,c+2], "|",end = '')
                else: 
                    print(self.tablero[f+2,c+2], " |",end = '')
        print("")


""" chess = Chess()
print(chess.tablero)
chess.setPiece(7,7,6)
chess.printChessBoard() """