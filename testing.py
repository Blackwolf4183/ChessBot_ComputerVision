import io
import chess
import chess.svg



board = [[0, -2, -3, 2, 0, 0, 0, -4], [0, 0, -1, -1, -3, 0, 0, -1],
         [-4, 0, 0, 0, 0, -6, -1, -2], [0, -1, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 1, 1, 0, 0, 1, 3],
         [1, 0, 0, 0, 1, 0, 0, 1], [4, 0, 3, 5, 0, 4, 6, 0]]

index2piece = {
    1: "p",
    2: "n",
    3: "b",
    4: "r",
    5: "q",
    6: "k",
}


def array2fen(chess_array):
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
                    s.write(index2piece[abs(c)].upper(
                    ) if c > 0 else index2piece[abs(c)].lower())
                else:
                    empty += 1
            if empty > 0:
                s.write(str(empty))
            s.write('/')
        # Move one position back to overwrite last '/'
        s.seek(s.tell() - 1)
        # If you do not have the additional information choose what to put
        #FIXME: hay que cambiarlo para que siempre nos de la posición de nuestras piezas como turno que toca
        s.write(' w KQkq - 0 1')
        return s.getvalue()


fen = array2fen(board)
print("fen is: ", fen)
board = chess.Board(fen)

