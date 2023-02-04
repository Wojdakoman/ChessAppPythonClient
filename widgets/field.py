from PyQt6 import QtWidgets
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor
from PyQt6.QtCore import Qt

class Field(QtWidgets.QWidget):
    def __init__(self, isOdd: bool, size: int):
        super().__init__();
        self.setMinimumSize(size, size);
        self.setMaximumSize(size, size);
        if isOdd:
            self.color = QColor(100, 30, 22);
        else:
            self.color = QColor(249, 231, 159);

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.GlobalColor.transparent, 1, Qt.PenStyle.SolidLine));
        painter.setBrush(QBrush(self.color, Qt.BrushStyle.SolidPattern));
 
        size = self.width();
        painter.drawRect(0, 0, size, size);
