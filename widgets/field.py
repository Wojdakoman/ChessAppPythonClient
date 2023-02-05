from PyQt6 import QtWidgets
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout

from widgets.pawn import Pawn

class Field(QtWidgets.QWidget):
    def __init__(self, isOdd: bool, size: int, pawn: Pawn = None):
        super().__init__();
        self.setMinimumSize(size, size);
        self.setMaximumSize(size, size);
        if isOdd:
            self.color = QColor(100, 30, 22);
        else:
            self.color = QColor(249, 231, 159);
            
        if pawn is not None:
            self.setLayout(QGridLayout());
            self.layout().addWidget(pawn);
            self.layout().setContentsMargins(0, 0, 0, 0);
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.GlobalColor.transparent, 1, Qt.PenStyle.SolidLine));
        painter.setBrush(QBrush(self.color, Qt.BrushStyle.SolidPattern));
 
        size = self.width();
        painter.drawRect(0, 0, size, size);
