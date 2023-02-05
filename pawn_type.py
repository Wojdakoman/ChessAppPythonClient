from enum import Enum

class PawnType(str, Enum):
    BISHOP = "bishop";
    KING = "king";
    KNIGHT = "knight";
    PAWN = "pawn";
    QUEEN = "queen";
    ROOK = "rook";
    UNKNOWN = "unknown";