from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QAction
from game_controller import GameController
from pawn_type import PawnType
from widgets.field import Field
from widgets.header import Header
from widgets.pawn import Pawn

class MainWindow(QMainWindow):
    def __init__(self, ws):
        super().__init__();
        
        self.ws = ws;

        self.setWindowTitle("Chess App");
        self.setGeometry(100, 100, 600, 600);
        
        self.createMenu();
        self.generateBoard();
        
        self.setOnlineStatus(False);
        
    def generateBoard(self) -> None:
        borderSize = 25;
        fieldSize = self.getFieldSize(borderSize);
        
        layout = QVBoxLayout();
        self.drawHeaderRow(layout, borderSize, fieldSize);
        
        # board
        isOdd = True;
        for i in range(8):
            rowLayout = QHBoxLayout();
            rowLayout.addWidget(Header(fieldSize, borderSize, GameController.rowHeaders[i]));
            for j in range(8):
                rowLayout.addWidget(Field(isOdd, fieldSize, Pawn(isOdd, fieldSize, PawnType.KING)));
                isOdd = not isOdd;
            rowLayout.addWidget(Header(fieldSize, borderSize, GameController.rowHeaders[i]));
            rowLayout.addStretch();
            layout.addLayout(rowLayout);
            isOdd = not isOdd;
            
        self.drawHeaderRow(layout, borderSize, fieldSize);
            
        layout.addStretch();
        layout.setContentsMargins(self.getSpacerSize(self.width(), fieldSize, borderSize), self.getSpacerSize(self.height(), fieldSize, borderSize), 0, 0);
        layout.setSpacing(0);
        
        wid = QWidget(self);
        wid.setLayout(layout);
        
        self.setCentralWidget(wid);
        
    def drawHeaderRow(self, layout: QVBoxLayout, borderSize: int, fieldSize: int) -> None:
        rowLayout = QHBoxLayout();
        rowLayout.addWidget(Header(borderSize, borderSize, ""));
        for i in range(8):
            rowLayout.addWidget(Header(borderSize, fieldSize, GameController.columnHeaders[i]));
        rowLayout.addWidget(Header(borderSize, borderSize, ""));
        rowLayout.addStretch();
        layout.addLayout(rowLayout);
        
    def resizeEvent(self, event):
        self.generateBoard();
        
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
        
    def getFieldSize(self, borderSize: int) -> int:
        height = self.height();
        width = self.width();
        
        if height <= width:
            return (height - 2 * borderSize) / (GameController.boardSize + 1);
        else:
            return (width - 2 * borderSize) / (GameController.boardSize + 1);
        
    def getSpacerSize(self, value: int, fieldSize: int, borderSize: int) -> int:
        return (value - GameController.boardSize * (fieldSize + 1) - 2 * borderSize) / 2;
    
    def createMenu(self) -> None:
        self.menu = self.menuBar()
        self.createAccountMenu();
        self.createGameMenu();
        self.createSettingMenu();
        
    def createAccountMenu(self) -> None:
        self.accountMenu = self.menu.addMenu("Account");

        self.actionLogin = QAction('Login', self);
        # actionLogin.triggered.connect(self.close)
        self.accountMenu.addAction(self.actionLogin);
        
        self.actionLogout = QAction('Logout', self);
        # actionLogin.triggered.connect(self.close)
        self.accountMenu.addAction(self.actionLogout);
        
    def createGameMenu(self) -> None:
        self.gameMenu = self.menu.addMenu("Game");

        self.actionFindGame = QAction('Find game', self);
        # actionLogin.triggered.connect(self.close)
        self.gameMenu.addAction(self.actionFindGame);
        
        self.actionGiveUp = QAction('Give up', self);
        # actionLogin.triggered.connect(self.close)
        self.gameMenu.addAction(self.actionGiveUp);
        
        self.actionOpDetails = QAction('Opponent\'s details', self);
        # actionLogin.triggered.connect(self.close)
        self.gameMenu.addAction(self.actionOpDetails);
        
    def createSettingMenu(self) -> None:
        self.settingMenu = self.menu.addMenu("Settings");

        self.actionChangeURL = QAction('Edit Chess Web App domain', self);
        # actionLogin.triggered.connect(self.close)
        self.settingMenu.addAction(self.actionChangeURL);
        
    def setOnlineStatus(self, isOnline: bool) -> None:
        if isOnline:
            self.statusBar().showMessage("Login status: ONLINE");
            
            self.actionLogin.setDisabled(True);
            self.actionLogout.setEnabled(True);
            
            self.gameMenu.setEnabled(True);
            
            self.actionChangeURL.setEnabled(True);
        else:
            self.statusBar().showMessage("Login status: OFFLINE");
            
            self.actionLogin.setEnabled(True);
            self.actionLogout.setDisabled(True);
            
            self.gameMenu.setDisabled(True);
            
            self.actionChangeURL.setDisabled(True);
