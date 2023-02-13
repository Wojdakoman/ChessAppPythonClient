from pawn_type import PawnType

class GameController:
    boardSize = 8;
    columnHeaders = ["A", "B", "C", "D", "E", "F", "G", "H"];
    rowHeaders = ["1", "2", "3", "4", "5", "6", "7", "8"];
    pawnTypes = [PawnType.UNKNOWN, PawnType.PAWN, PawnType.ROOK, PawnType.KNIGHT, PawnType.BISHOP, PawnType.QUEEN, PawnType.KING];