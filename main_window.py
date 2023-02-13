from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QMessageBox, QLabel, QStatusBar
from PyQt6.QtGui import QAction
from game_controller import GameController
from pawn_type import PawnType
from widgets.field import Field
from widgets.header import Header
from widgets.login_dialog import LoginDialog
from widgets.pawn import Pawn

class MainWindow(QMainWindow):
    def __init__(self, ws):
        super().__init__();
        
        self.ws = ws;
        
        self.isBoardTurned = False;
        self.generateEmptyBoard();

        self.setWindowTitle("Chess App");
        self.setGeometry(100, 100, 600, 600);
        
        self.createMenu();
        self.generateBoard();
        
        self.status = QLabel();
        self.statusBar = QStatusBar();
        self.statusBar.addPermanentWidget(self.status, 1);
        self.setStatusBar(self.statusBar);
        
        self.setOnlineStatus(False);
        
        self.ws.obs.on("startPosition", self.setStartPosition);
        
    def generateBoard(self) -> None:
        borderSize = 25;
        fieldSize = self.getFieldSize(borderSize);
        
        layout = QVBoxLayout();
        self.drawHeaderRow(layout, borderSize, fieldSize);
        
        # board
        isOdd = True;
        for i in range(GameController.boardSize):
            rowLayout = QHBoxLayout();
            headerIdx = i;
            if self.isBoardTurned:
                headerIdx = GameController.boardSize - 1 - i;
            rowLayout.addWidget(Header(fieldSize, borderSize, GameController.rowHeaders[headerIdx]));
            for j in range(GameController.boardSize):
                rowLayout.addWidget(Field(isOdd, fieldSize, self.getFieldFigure(i, j, fieldSize)));
                isOdd = not isOdd;
            rowLayout.addWidget(Header(fieldSize, borderSize, GameController.rowHeaders[headerIdx]));
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
        for i in range(GameController.boardSize):
            columnIdx = i;
            if self.isBoardTurned:
                columnIdx = GameController.boardSize - 1 - i;
            rowLayout.addWidget(Header(borderSize, fieldSize, GameController.columnHeaders[columnIdx]));
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
        self.actionLogin.triggered.connect(self.showLoginDialog);
        self.accountMenu.addAction(self.actionLogin);
        
        self.actionLogout = QAction('Logout', self);
        self.actionLogout.triggered.connect(self.logout);
        self.accountMenu.addAction(self.actionLogout);
        
    def createGameMenu(self) -> None:
        self.gameMenu = self.menu.addMenu("Game");

        self.actionFindGame = QAction('Find game', self);
        self.actionFindGame.triggered.connect(self.findGame);
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
            self.status.setText("Login status: ONLINE");
            
            self.actionLogin.setDisabled(True);
            self.actionLogout.setEnabled(True);
            
            self.gameMenu.setEnabled(True);
            
            self.actionChangeURL.setEnabled(True);
        else:
            self.status.setText("Login status: OFFLINE");
            
            self.actionLogin.setEnabled(True);
            self.actionLogout.setDisabled(True);
            
            self.gameMenu.setDisabled(True);
            
            self.actionChangeURL.setDisabled(True);
            
    def showLoginDialog(self) -> None:
        dialog = LoginDialog(self.ws);
        if dialog.exec():
            self.status.setText("Logging in...");
            self.ws.obs.once("login", self.onLoginRepsonse);
        
    def onLoginRepsonse(self, response: bool) -> None:
        if response:
            self.setOnlineStatus(True);
            QMessageBox(QMessageBox.Icon.Information, "Login successful", "Logged in!", parent=self).show();
        else:
            self.setOnlineStatus(False);
            QMessageBox(QMessageBox.Icon.Critical, "Login failed", "Couldn't log in!", parent=self).show();
            
    def logout(self) -> None:
        self.ws.logout("Logout");
        self.setOnlineStatus(False);

    def findGame(self) -> None:
        self.status.setText("Finding game...");
        self.ws.findGame();
        self.ws.obs.once("gameStart", self.onGameFoundRepsonse);
    
    def onGameFoundRepsonse(self, msg) -> None:
        if not msg:
            self.status.setText("Error while finding game!");
            QMessageBox(QMessageBox.Icon.Critical, "Error", "An error occurred while searching for games!", parent=self).show();
        else:
            self.bd_sub = self.ws.obs.on("boardData", self.onGameData);
            
            self.status.setText("Login status: ONLINE - INGAME");
            alertBoxMsg = msg.replace("GS: ST ", "");
            QMessageBox(QMessageBox.Icon.Information, "Found game!", alertBoxMsg, parent=self).show();
            
            
    def onGameData(self, data: str) -> None:
        self.generateEmptyBoard();
        self.readBoardData(data);
        self.generateBoard();
            
    def generateEmptyBoard(self) -> None:
        self.board_data = [None for i in range(GameController.boardSize)];
        for i in range(GameController.boardSize):
            self.board_data[i] = [None for j in range(GameController.boardSize)];
            
    def readBoardData(self, data: str) -> None:
        list_data = data.split();
        for i in range(len(list_data)):
            figure_data = list_data[i].split(",");
            type_int = int(figure_data[0]);
            f_type = GameController.pawnTypes[abs(type_int)];
            isWhite = type_int > 0;
            row = int(figure_data[1]);
            col = int(figure_data[2]);
            if self.isBoardTurned:
                row = GameController.boardSize - 1 - row;
                col = GameController.boardSize - 1 - col;
            self.board_data[row][col] = (f_type, isWhite);
            
    def getFieldFigure(self, row: int, col: int, fieldSize: int) -> Pawn:
        figure_data = self.board_data[row][col];
        if figure_data is None:
            return None;
        else:
            return Pawn(figure_data[1], fieldSize, figure_data[0]);
            
    def debug_print_board(self) -> None:
        print(self.board_data);
        print();
        print();
        for i in range(GameController.boardSize):
            for j in range(GameController.boardSize):
                print(self.board_data[i][j], end=" ");
            print();
            
    def setStartPosition(self, data: str) -> None:
        self.isBoardTurned = "T" in data;
            