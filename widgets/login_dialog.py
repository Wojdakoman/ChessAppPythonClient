from PyQt6.QtWidgets import QDialog, QPushButton, QLineEdit, QLabel, QHBoxLayout, QGridLayout, QMessageBox
from websocket_handler import Websockethandler

class LoginDialog(QDialog):
    def __init__(self, ws: Websockethandler):
        super().__init__();
        
        self.ws = ws;
        self.setWindowTitle("Login to Chess Web App");
        
        layout = QGridLayout();
        
        layout.addWidget(QLabel("Login"), 0, 0);
        self.loginBox = QLineEdit();
        layout.addWidget(self.loginBox, 0, 1);
        
        layout.addWidget(QLabel("Password"), 1, 0);
        self.passwordBox = QLineEdit();
        self.passwordBox.setEchoMode(QLineEdit.EchoMode.Password);
        layout.addWidget(self.passwordBox, 1, 1);
        
        
        buttonLayout = QHBoxLayout();
        buttonLogin = QPushButton("Login");
        buttonLogin.clicked.connect(self.performLogin);
        buttonLayout.addWidget(buttonLogin);
        
        buttonCancel = QPushButton("Canel");
        buttonCancel.clicked.connect(self.close);
        buttonLayout.addWidget(buttonCancel);
        
        layout.addLayout(buttonLayout, 3, 0, 1, 2);
        
        self.setLayout(layout);
        
    def performLogin(self) -> None:
        login = self.loginBox.text();
        password = self.passwordBox.text();
        
        if not login or not password:
            QMessageBox(QMessageBox.Icon.Warning, "Missing data", "Please fill login and password", parent=self).show();
            return;
        
        self.ws.login(login, password);
        self.accept();