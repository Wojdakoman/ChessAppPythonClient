from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QMessageBox, QLabel, QStatusBar
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QTimer
import random
from bot.board_translate import BoardTranslate
from bot.bot_engine import BotEngine
from game_controller import GameController
from widgets.field import Field
from widgets.header import Header
from widgets.login_dialog import LoginDialog
from widgets.pawn import Pawn
from widgets.server_edit_dialog import ServerEditDialog

class MainWindow(QMainWindow):
    def __init__(self, ws):
        super().__init__();
        
        self.ws = ws;
        self.lastusername = "";

        self.isBoardTurned = False;
        self.isClientTurn = False;
        self.playingVSBot = False;
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
        self.ws.obs.on("gameOver", self.onGameOver);
        self.ws.obs.on("WSclosed", self.onWSClosed);
        
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
                isMovePossible = self.board_moves_data[i][j] == 1;
                isPawnActive = self.board_moves_data[i][j] == 2;
                field = Field(isOdd, fieldSize, self.getFieldFigure(i, j, fieldSize), isPawnActive, isMovePossible);
                field.mousePressEvent = lambda e, row=i, col=j, isMovePossible=isMovePossible: self.onFieldClick(e, row, col, isMovePossible);
                rowLayout.addWidget(field);
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
        self.actionGiveUp.triggered.connect(self.giveUp);
        self.gameMenu.addAction(self.actionGiveUp);
        
        self.actionOpDetails = QAction('Opponent\'s details', self);
        self.actionOpDetails.triggered.connect(self.getOpponentsDetails);
        self.gameMenu.addAction(self.actionOpDetails);
        
        self.actionBotPlay = QAction('Play vs BOT', self);
        self.actionBotPlay.triggered.connect(self.playVSBot);
        self.gameMenu.addAction(self.actionBotPlay);
        
    def createSettingMenu(self) -> None:
        self.settingMenu = self.menu.addMenu("Settings");

        self.actionChangeURL = QAction('Edit Chess Web App domain', self);
        self.actionChangeURL.triggered.connect(self.editUrl);
        self.settingMenu.addAction(self.actionChangeURL);
        
    def setOnlineStatus(self, isOnline: bool) -> None:
        if isOnline:
            self.status.setText("Login status: ONLINE as {}".format(self.lastusername));
            
            self.actionLogin.setDisabled(True);
            self.actionLogout.setEnabled(True);
            
            self.actionFindGame.setEnabled(True);
            self.actionGiveUp.setDisabled(True);
            self.actionOpDetails.setDisabled(True);
            self.actionBotPlay.setEnabled(True);
            
            self.actionChangeURL.setEnabled(True);
        else:
            self.status.setText("Login status: OFFLINE");
            
            self.actionLogin.setEnabled(True);
            self.actionLogout.setDisabled(True);
            
            self.actionFindGame.setDisabled(True);
            self.actionGiveUp.setDisabled(True);
            self.actionOpDetails.setDisabled(True);
            self.actionBotPlay.setEnabled(True);
            
            self.actionChangeURL.setEnabled(True);
            
    def showLoginDialog(self) -> None:
        dialog = LoginDialog(self.ws);
        if dialog.exec():
            self.lastusername = dialog.loginBox.text();
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
        self.generateEmptyBoard();
        self.generateBoard();
        self.status.setText("Finding game...");
        self.ws.findGame();
        self.ws.obs.once("gameStart", self.onGameFoundRepsonse);
    
    def onGameFoundRepsonse(self, msg) -> None:
        if not msg:
            self.status.setText("Error while finding game!");
            QMessageBox(QMessageBox.Icon.Critical, "Error", "An error occurred while searching for games!", parent=self).show();
        else:
            self.actionFindGame.setDisabled(True);
            self.actionGiveUp.setEnabled(True);
            self.actionOpDetails.setEnabled(True);
            self.actionChangeURL.setDisabled(True);
            self.actionBotPlay.setDisabled(True);
            
            self.bd_sub = self.ws.obs.on("boardData", self.onGameData);
            self.turn_sub = self.ws.obs.on("turnChange", self.onChangeTurn);
            
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
        self.clearMovesData();
            
    def clearMovesData(self) -> None:
        self.board_moves_data = [None for i in range(GameController.boardSize)];
        for i in range(GameController.boardSize):
            self.board_moves_data[i] = [None for j in range(GameController.boardSize)];
            
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
            fig = Pawn(figure_data[1], fieldSize, figure_data[0]);
            fig.mousePressEvent = lambda e, row=row, col=col, isWhite=figure_data[1]: self.onFigClick(e, row, col, isWhite);
            return fig;
            
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
        
    def onChangeTurn(self, data: str) -> None:
        self.isClientTurn = "T" in data;
        
        if self.isClientTurn:
            statusMsg = "YOUR TURN";
        else:
            statusMsg = "waiting for {} move".format("bot's" if self.playingVSBot else "opponent's");
        self.status.setText("{}: {}".format("Login status: OFFLINE - INGAME vs BOT" if self.playingVSBot else "Login status: ONLINE as {} - INGAME".format(self.lastusername), statusMsg));
        
    def onFigClick(self, e, row: int, col: int, isWhite: bool) -> None:
        if (isWhite and self.isBoardTurned) or (not isWhite and not self.isBoardTurned):
            # check capture move
            self.onFieldClick(None, row, col, self.board_moves_data[row][col] == 1);
        elif not self.isClientTurn:
            return;
        else:
            self.clearMovesData();
            self.board_moves_data[row][col] = 2; # flag active figure
            if self.isBoardTurned:
                row = GameController.boardSize - 1 - row;
                col = GameController.boardSize - 1 - col;
            if self.playingVSBot:
                self.onPossibleMoves(BoardTranslate.getPossibleMoves(self.botEngine.board, row, col));
            else:
                self.ws.getPossibleMoves(row, col);
                self.ws.obs.once("possibleMoves", self.onPossibleMoves);
            
    def onPossibleMoves(self, data: str) -> None:
        list_data = data.split();
        for i in range(len(list_data)):
            figure_data = list_data[i].split(",");
            row = int(figure_data[0]);
            col = int(figure_data[1]);
            #if (self.isBoardTurned and not self.playingVSBot) or (self.playingVSBot and not self.isBoardTurned):
            if self.isBoardTurned:
                row = GameController.boardSize - 1 - row;
                col = GameController.boardSize - 1 - col;
            self.board_moves_data[row][col] = 1; # flag possible move
        self.generateBoard();
        
    def onFieldClick(self, e, row: int, col: int, isMovePossible: bool) -> None:
        if not isMovePossible or not self.isClientTurn:
            return;
        
        activePawn = self.getActivePawn();
        if activePawn is None:
            return;
        
        currentRow = activePawn[0];
        currentCol = activePawn[1];
        
        if self.isBoardTurned:
            row = GameController.boardSize - 1 - row;
            col = GameController.boardSize - 1 - col;
            currentRow = GameController.boardSize - 1 - currentRow;
            currentCol = GameController.boardSize - 1 - currentCol;
            
        if self.playingVSBot:
            self.performVSBotMove(currentRow, currentCol, row, col);
        else:
            self.ws.performMove(currentRow, currentCol, row, col);
        
    def getActivePawn(self):
        for i in range(GameController.boardSize):
            for j in range(GameController.boardSize):
                if self.board_moves_data[i][j] == 2:
                    return (i,j);
        return None;
    
    def onGameOver(self, msg: str) -> None:
        self.ws.obs.off("boardData");
        self.ws.obs.off("turnChange");
        QMessageBox(QMessageBox.Icon.Information, "Game over!", msg, parent=self).show();
        self.setOnlineStatus(True);
        
    def giveUp(self) -> None:
        self.ws.giveUp();
        
    def getOpponentsDetails(self) -> None:
        self.ws.getOpponentsDetails();
        self.ws.obs.once("opponentsDetails", lambda msg: QMessageBox(QMessageBox.Icon.Information, "Opponent's details", msg, parent=self).show());
        
    def editUrl(self) -> None:
        dialog = ServerEditDialog(self.ws);
        if dialog.exec():
            self.setOnlineStatus(False);
            
    def onWSClosed(self) -> None:
        if self.playingVSBot:
            return;
        QMessageBox(QMessageBox.Icon.Critical, "Connection lost", "Connection to server has been lost", parent=self).show()
        if "INGAME" in self.status.text():
            self.onGameOver("Connection lost");
        self.setOnlineStatus(False);
        
    def playVSBot(self) -> None:
        print('Playing VS BOT');
        self.ws.close();
        self.playingVSBot = True;
        self.botEngine = BotEngine();
                
        if random.random() < 0.5:
            # bot is black
            self.setStartPosition("F");
            self.onChangeTurn("T");
            self.onGameData(BoardTranslate.translateBotBoard(self.botEngine.board));
        else:
            # bot is white
            self.setStartPosition("T");
            self.onChangeTurn("F");
            self.onGameData(BoardTranslate.translateBotBoard(self.botEngine.board));
            QTimer.singleShot(random.uniform(0.5, 2.9) * 1000, self.performBotMove);
            #self.performBotMove();
        
    def performBotMove(self) -> None:
        mov = self.botEngine.getMove();
        print("BOT: {}".format(mov));
        self.botEngine.board.push(mov);
        
        self.onGameData(BoardTranslate.translateBotBoard(self.botEngine.board));
        self.checkBotGameEnded();
        self.onChangeTurn("T");
        
    def performVSBotMove(self, current_row: int, current_col: int, destination_row: int, destination_column: int) -> None:
        from_square = BoardTranslate.getMoveName(current_row, current_col);
        to_square = BoardTranslate.getMoveName(destination_row, destination_column);
        print(from_square);
        print(to_square);
        
        self.botEngine.board.push_san("{}{}".format(from_square, to_square));
        self.onGameData(BoardTranslate.translateBotBoard(self.botEngine.board));
        self.checkBotGameEnded();
        self.onChangeTurn("F");
        
        QTimer.singleShot(random.uniform(0.5, 2.9) * 1000, self.performBotMove);
        #self.performBotMove();
        
    def checkBotGameEnded(self) -> None:
        if self.botEngine.board.is_game_over(claim_draw=True):
            self.onGameOver("You have won!" if self.isClientTurn else "BOT has won!");
            self.playingVSBot = False;
            self.setOnlineStatus(False);
