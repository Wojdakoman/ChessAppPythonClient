from PyQt6 import QtWidgets
from PyQt6.QtGui import QPainter, QBrush, QPen
from PyQt6.QtCore import Qt, QRectF

class Header(QtWidgets.QWidget):    
    def __init__(self, height: int, width: int, text: str):
        super().__init__();
        self.setMinimumSize(width, height);
        self.setMaximumSize(width, height);
        self.rheight = height;
        self.rwidth = width;
        self.text = text;

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.GlobalColor.transparent, 1, Qt.PenStyle.SolidLine));
        painter.setBrush(QBrush(Qt.GlobalColor.black, Qt.BrushStyle.SolidPattern));
 
        painter.drawRect(0, 0, self.rwidth, self.rheight);
        
        painter.setPen(QPen(Qt.GlobalColor.white));
        painter.drawText(QRectF(0, 0, self.rwidth, self.rheight), Qt.AlignmentFlag.AlignCenter, self.text);
