from PyQt6.QtWidgets import QMainWindow, QPushButton, QGridLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self, ws):
        super().__init__();
        
        self.ws = ws;

        self.setWindowTitle("Chess App");
        self.setGeometry(100, 100, 280, 80);
        
        layout = QGridLayout();
        
        button = QPushButton("Ping!");
        button.clicked.connect(ws.ping);
        
        button2 = QPushButton("Login OK");
        button2.clicked.connect(self.loginOK);
        
        button3 = QPushButton("Login BAD");
        button3.clicked.connect(self.loginBAD);
        
        layout.addWidget(button, 0, 0);
        layout.addWidget(button2, 1, 0);
        layout.addWidget(button3, 1, 1);
        
        wid = QWidget(self);
        wid.setLayout(layout);
        
        self.setCentralWidget(wid);
        
    def closeEvent(self, event):
        print("ON APP CLOSE");
        
        self.ws.logout("Exit");
        self.ws.close();
    
    def on_msg(self, msg):
        print("ON MSG: {}".format(msg));
        
    def loginOK(self):
        self.ws.login("adam", "adam123");
        self.onLoginRepsonse();
        
    def loginBAD(self):
        self.ws.login("adam", "adam1234");
        self.onLoginRepsonse();
        
    def onLoginRepsonse(self):
        self.ws.obs.on("login", lambda v: print("login {}".format(v)));
        
