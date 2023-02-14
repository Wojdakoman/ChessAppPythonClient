from PyQt6.QtWidgets import QDialog, QPushButton, QLineEdit, QLabel, QHBoxLayout, QGridLayout, QMessageBox
from server_url_helper import ServerURLHelper
from websocket_handler import Websockethandler

class ServerEditDialog(QDialog):
    def __init__(self, ws: Websockethandler):
        super().__init__();
        
        self.ws = ws;
        self.setWindowTitle("Edit Chess Web App domain");
        
        layout = QGridLayout();
        
        layout.addWidget(QLabel("URL"), 0, 0);
        self.urlBox = QLineEdit();
        layout.addWidget(self.urlBox, 0, 1);
        
        self.urlBox.setText(ServerURLHelper.getServerURL());
        
        buttonLayout = QHBoxLayout();
        buttonSave = QPushButton("Save");
        buttonSave.clicked.connect(self.saveUrl);
        buttonLayout.addWidget(buttonSave);
        
        buttonCancel = QPushButton("Canel");
        buttonCancel.clicked.connect(self.close);
        buttonLayout.addWidget(buttonCancel);
        
        layout.addLayout(buttonLayout, 3, 0, 1, 2);
        
        self.setLayout(layout);
        
    def saveUrl(self) -> None:
        url = self.urlBox.text();
        
        if not url:
            QMessageBox(QMessageBox.Icon.Warning, "Missing data", "Please fill URL data", parent=self).show();
            return;
        
        ServerURLHelper.saveServerURL(url);
        self.ws.close();
        
        self.accept();