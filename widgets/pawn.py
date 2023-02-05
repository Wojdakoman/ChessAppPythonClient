import os
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from pawn_type import PawnType

class Pawn(QLabel):
    def __init__(self, white: bool, size: int, type: PawnType = PawnType.UNKNOWN):
        super().__init__();

        path = os.getcwd() + "\\resources\\";
        if type is PawnType.UNKNOWN:
            path += "unknown.png";
        else:
            path += "{}_{}.png".format("white" if white else "black", type);
        
        pixmap = QPixmap(path).scaledToWidth(0.9 * size, Qt.TransformationMode.SmoothTransformation);
        
        self.setPixmap(pixmap);
        
        self.setMinimumSize(pixmap.width(), pixmap.height());
        self.setMaximumSize(pixmap.width(), pixmap.height());
        
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)