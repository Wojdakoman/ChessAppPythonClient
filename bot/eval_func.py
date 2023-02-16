import chess

from bot.figure_tables import FigureTables

class EvalFunction:
    @staticmethod
    def eval(board: chess.Board) -> int:
        if board.is_checkmate():
            if board.turn:
                return -9999; # black win
            else:
                return 9999; # white win
        if board.is_stalemate():
            return 0;
        if board.is_insufficient_material():
            return 0;
            
        wp = len(board.pieces(chess.PAWN, chess.WHITE));
        bp = len(board.pieces(chess.PAWN, chess.BLACK));
        wn = len(board.pieces(chess.KNIGHT, chess.WHITE));
        bn = len(board.pieces(chess.KNIGHT, chess.BLACK));
        wb = len(board.pieces(chess.BISHOP, chess.WHITE));
        bb = len(board.pieces(chess.BISHOP, chess.BLACK));
        wr = len(board.pieces(chess.ROOK, chess.WHITE));
        br = len(board.pieces(chess.ROOK, chess.BLACK));
        wq = len(board.pieces(chess.QUEEN, chess.WHITE));
        bq = len(board.pieces(chess.QUEEN, chess.BLACK));
        
        material = 100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq);
        
        pawnsq = sum([FigureTables.pawnTable[i] for i in board.pieces(chess.PAWN, chess.WHITE)]);
        pawnsq = pawnsq + sum([-FigureTables.pawnTable[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK)]);
        
        knightsq = sum([FigureTables.knightsTable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)]);
        knightsq = knightsq + sum([-FigureTables.knightsTable[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK)]);
        
        bishopsq = sum([FigureTables.bishopsTable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)]);
        bishopsq = bishopsq + sum([-FigureTables.bishopsTable[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.BLACK)]);
        
        rooksq = sum([FigureTables.rooksTable[i] for i in board.pieces(chess.ROOK, chess.WHITE)]);
        rooksq = rooksq + sum([-FigureTables.rooksTable[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK)]);
        
        queensq = sum([FigureTables.queensTable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)]);
        queensq = queensq + sum([-FigureTables.queensTable[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK)]);
        
        kingsq = sum([FigureTables.kingsTable[i] for i in board.pieces(chess.KING, chess.WHITE)]);
        kingsq = kingsq + sum([-FigureTables.kingsTable[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK)]);
        
        value = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq;
        
        if board.turn:
            return value
        else:
            return -value