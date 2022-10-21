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
        if self.tablero[x,y] != 99: # Que no se salga del tablero
            self.tablero[x+2,y+2] = piece_keycode
        
    def removePiece(self, x, y):
        chess.setPiece(x, y, 0)


""" chess = Chess()
print(chess.tablero)
chess.setPiece(7,7,6)
print(chess.tablero) """