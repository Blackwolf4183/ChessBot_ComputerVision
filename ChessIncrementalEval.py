import chess
import chess.svg
import chess.polyglot
import time

# Tablas usadas para la evaluación de posiciones
# Si la casilla es positiva, la pieza intentara moverse a esa casilla
# Si es negativa el motor tratara de evitar poner la pieza en esa casilla

pawntable = [  # La tabla esta hecha de tal manera que el motor se vea animado a avanzar los peones
    0, 0, 0, 0, 0, 0, 0, 0, 5, 10, 10, -20, -20, 10, 10, 5, 5, -5, -10, 0, 0,
    -10, -5, 5, 0, 0, 0, 20, 20, 0, 0, 0, 5, 5, 10, 25, 25, 10, 5, 5, 10, 10,
    20, 30, 30, 20, 10, 10, 50, 50, 50, 50, 50, 50, 50, 50, 0, 0, 0, 0, 0, 0,
    0, 0
]

knightstable = [  # Los caballos se ven animados a ocupar el centro y evitar los bordes a toda costa
    -50, -40, -30, -30, -30, -30, -40, -50, -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30, -30, 0, 15, 20, 20, 15, 0, -30, -30, 5, 15,
    20, 20, 15, 5, -30, -30, 0, 10, 15, 15, 10, 0, -30, -40, -20, 0, 0, 0, 0,
    -20, -40, -50, -40, -30, -30, -30, -30, -40, -50
]

bishopstable = [  # Los alfiles deben evitar las esquinas y los bordes del tablero
    -20, -10, -10, -10, -10, -10, -10, -20, -10, 5, 0, 0, 0, 0, 5, -10, -10,
    10, 10, 10, 10, 10, 10, -10, -10, 0, 10, 10, 10, 10, 0, -10, -10, 5, 5, 10,
    10, 5, 5, -10, -10, 0, 5, 10, 10, 5, 0, -10, -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]

rookstable = [  # Las torres deben evitar las columnas a y h a la vez que ocupar la fila 7
    0, 0, 0, 5, 5, 0, 0, 0, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0,
    -5, 5, 10, 10, 10, 10, 10, 10, 5, 0, 0, 0, 0, 0, 0, 0, 0
]

queenstable = [  # La dama debe evitar bordes y esquinas, y ocupar el centro
    -20, -10, -10, -5, -5, -10, -10, -20, -10, 0, 0, 0, 0, 0, 0, -10, -10, 5,
    5, 5, 5, 5, 0, -10, 0, 0, 5, 5, 5, 5, 0, -5, -5, 0, 5, 5, 5, 5, 0, -5, -10,
    0, 5, 5, 5, 5, 0, -10, -10, 0, 0, 0, 0, 0, 0, -10, -20, -10, -10, -5, -5,
    -10, -10, -20
]

kingstable = [  # El rey debe mantenerse refugiado tras los peones
    20, 30, 10, 0, 0, 10, 30, 20, 20, 20, 0, 0, 0, 0, 20, 20, -10, -20, -20,
    -20, -20, -20, -20, -10, -20, -30, -30, -40, -40, -30, -30, -20, -30, -40,
    -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -30,
    -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30
]

pieces = [
    chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING
]
tables = [
    pawntable, knightstable, bishopstable, rookstable, queenstable, kingstable
]
values = [100, 320, 330, 500, 900]



class ChessEngine:


    def __init__(self, custom_board):

        global pawntable, knightstable, bishopstable, rookstable, queenstable, kingstable, tables, pieces, values

        self.board_value = -9999
        self.board = custom_board

        # Obtenemos el numero de piezas que tienen ambos jugadores
        white_pawns = len(self.board.pieces(chess.PAWN, chess.WHITE))
        white_knights = len(self.board.pieces(chess.KNIGHT, chess.WHITE))
        white_bishops = len(self.board.pieces(chess.BISHOP, chess.WHITE))
        white_rooks = len(self.board.pieces(chess.ROOK, chess.WHITE))
        white_queen = len(self.board.pieces(chess.QUEEN, chess.WHITE))
        black_pawns = len(self.board.pieces(chess.PAWN, chess.BLACK))
        black_knights = len(self.board.pieces(chess.KNIGHT, chess.BLACK))
        black_bishops = len(self.board.pieces(chess.BISHOP, chess.BLACK))
        black_rooks = len(self.board.pieces(chess.ROOK, chess.BLACK))
        black_queen = len(self.board.pieces(chess.QUEEN, chess.BLACK))

        # Calculamos la diferencia de material
        materialDiff = 100 * (white_pawns - black_pawns) + 320 * (white_knights - black_knights) + 330 * (
                white_bishops - black_bishops) \
                    + 500 * (white_rooks - black_rooks) + 900 * (white_queen - black_queen)

        # Calculamos la evaluacion segun las matrices definidas arriba
        # La primera linea ira sumando las piezas que tenemos en el tablero segun el valor dado en la tabla
        # La segunda linea flipea el tablero y evalua
        eval_pawns = sum(
            [pawntable[i] for i in self.board.pieces(chess.PAWN, chess.WHITE)])
        eval_pawns = eval_pawns + sum([
            -pawntable[chess.square_mirror(i)]
            for i in self.board.pieces(chess.PAWN, chess.BLACK)
        ])

        eval_knights = sum([
            knightstable[i]
            for i in self.board.pieces(chess.KNIGHT, chess.WHITE)
        ])
        eval_knights = eval_knights + sum([
            -knightstable[chess.square_mirror(i)]
            for i in self.board.pieces(chess.KNIGHT, chess.BLACK)
        ])

        eval_bishops = sum([
            bishopstable[i]
            for i in self.board.pieces(chess.BISHOP, chess.WHITE)
        ])
        eval_bishops = eval_bishops + sum([
            -bishopstable[chess.square_mirror(i)]
            for i in self.board.pieces(chess.BISHOP, chess.BLACK)
        ])

        eval_rooks = sum([
            rookstable[i] for i in self.board.pieces(chess.ROOK, chess.WHITE)
        ])
        eval_rooks = eval_rooks + sum([
            -rookstable[chess.square_mirror(i)]
            for i in self.board.pieces(chess.ROOK, chess.BLACK)
        ])

        eval_queen = sum([
            queenstable[i] for i in self.board.pieces(chess.QUEEN, chess.WHITE)
        ])
        eval_queen = eval_queen + sum([
            -queenstable[chess.square_mirror(i)]
            for i in self.board.pieces(chess.QUEEN, chess.BLACK)
        ])

        eval_king = sum([
            kingstable[i] for i in self.board.pieces(chess.KING, chess.WHITE)
        ])
        eval_king = eval_king + sum([
            -kingstable[chess.square_mirror(i)]
            for i in self.board.pieces(chess.KING, chess.BLACK)
        ])

        self.board_value = materialDiff + eval_pawns + eval_knights + eval_bishops + eval_rooks + eval_queen + eval_king

        print("Board value is: ", self.board_value)
        #return board_value

    def evaluate_board(self):


        if self.board.is_checkmate():
            if self.board.turn:
                return -9999
            else:
                return 9999
        if self.board.is_stalemate() or self.board.is_insufficient_material():
            return 0
        evaluation = self.board_value
        if self.board.turn:
            return evaluation
        else:
            return -evaluation

    def update_evaluation(self, move, side):
        global tables, values

        moving_piece = self.board.piece_type_at(move.from_square)

        if side:  #blancas juegan
            self.board_value = self.board_value - tables[moving_piece -
                                                         1][move.from_square]
            #Actualizamos el enroque
            if (move.from_square == chess.E1) and (move.to_square == chess.G1):
                self.board_value = self.board_value - rookstable[chess.H1]
                self.board_value = self.board_value + rookstable[chess.F1]
            elif (move.from_square == chess.E1) and (move.to_square
                                                     == chess.C1):
                self.board_value = self.board_value - rookstable[chess.A1]
                self.board_value = self.board_value + rookstable[chess.D1]
        else:
            self.board_value = self.board_value + tables[moving_piece -
                                                         1][move.from_square]
            # Actualizamos el enroque
            if (move.from_square == chess.E8) and (move.to_square == chess.G8):
                self.board_value = self.board_value - rookstable[chess.H8]
                self.board_value = self.board_value + rookstable[chess.F8]
            elif (move.from_square == chess.E8) and (move.to_square
                                                     == chess.C8):
                self.board_value = self.board_value - rookstable[chess.A8]
                self.board_value = self.board_value + rookstable[chess.D8]

        if side:
            self.board_value = self.board_value + tables[moving_piece -
                                                         1][move.to_square]
        else:
            self.board_value = self.board_value - tables[moving_piece -
                                                         1][move.to_square]

        #Actualizamos diferencia de material
        if move.drop is not None:
            if side:
                self.board_value = self.board_value + values[move.drop - 1]
            else:
                self.board_value = self.board_value - values[move.drop - 1]

        #Actualizamos posibles promociones de piezas
        if move.promotion is not None:
            if side:
                self.board_value = self.board_value + values[
                    move.promotion - 1] - values[moving_piece - 1]
                self.board_value = self.board_value - tables[moving_piece - 1][move.to_square] \
                            + tables[move.promotion-1][move.to_square]
            else:
                self.board_value = self.board_value - values[
                    move.promotion - 1] + values[moving_piece - 1]
                self.board_value = self.board_value + tables[moving_piece - 1][move.to_square] \
                            - tables[move.promotion - 1][move.to_square]
            return move

    def make_move(self, move):

        self.update_evaluation(move, self.board.turn)
        self.board.push(move)
        return move

    def unmake_move(self):  

        movement = self.board.pop()
        self.update_evaluation(movement, not self.board.turn)
        return movement

    def alphabeta(self, alpha, beta, depth):

        best_score = -9999
        if depth == 0:
            return self.quiesce(alpha, beta)

        for move in self.board.legal_moves:
            self.make_move(move)
            score = -self.alphabeta(-beta, -alpha, depth - 1)
            self.unmake_move()
            if score >= beta:
                return score
            if score > best_score:
                best_score = score
            if score > alpha:
                alpha = score

        return best_score

    def quiesce(self, alpha, beta):

        stand_pat = self.evaluate_board()
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat

        for move in self.board.legal_moves:
            if self.board.is_capture(move):
                self.make_move(move)
                score = -self.quiesce(-beta, -alpha)
                self.unmake_move()

                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score

        return alpha

    def selectmove(self, depth):

        try:
            move = chess.polyglot.MemoryMappedReader(
                "Perfect2017.bin").weighted_choice(self.board).move
            print("OPENING ES: ", move)
            # movehistory.append(move)
            return move
        except:
            bestMove = chess.Move.null()
            bestValue = -99999
            alpha = -100000
            beta = 100000
            for move in self.board.legal_moves:
                self.make_move(move)
                self.boardValue = -self.alphabeta(-beta, -alpha, depth - 1)
                if self.boardValue > bestValue:
                    bestValue = self.boardValue
                    bestMove = move
                if self.boardValue > alpha:
                    alpha = self.boardValue
                self.unmake_move()

            # movehistory.append(bestMove)
            return bestMove


