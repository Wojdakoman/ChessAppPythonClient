import chess

from game_controller import GameController

class BoardTranslate:
    @staticmethod
    def translateBotBoard(board: chess.Board) -> str:
        board_data = "";
        
        s = "{}".format(board);
        idx = 0;
        for i in range(GameController.boardSize):
            for j in range(GameController.boardSize):
                if s[idx] != '.':
                    board_data += BoardTranslate.getFigure(s[idx], i, j);
                idx += 2;
            print();
            
        return board_data;
    
    @staticmethod
    def getFigure(data: str, i: int, j: int) -> str:
        isWhite = data.isupper();
        return "{}{},{},{} ".format("" if isWhite else "-", BoardTranslate.getFigureNumber(data), i, j);
        
    @staticmethod
    def getFigureNumber(data: str) -> str:
        data = data.lower();
        figures = list([None, 'p', 'r', 'n', 'b', 'q', 'k']);
        return figures.index(data);
    
    @staticmethod
    def getPossibleMoves(board: chess.Board, i: int, j: int) -> str:
        # print(board);
        name = BoardTranslate.getMoveName(i, j);
        result = "";
        # print(name);
        for i in list(board.legal_moves):
            st = "{}".format(i);
            if name in st:
                # print(st);
                result += "{},{} ".format(GameController.boardSize - 1 - GameController.rowHeaders.index(st[3].upper()), GameController.columnHeaders.index(st[2].upper()));
        return result;
    
    @staticmethod
    def getMoveName(i: int, j: int) -> str:
        return "{}{}".format(GameController.columnHeaders[j].lower(), GameController.rowHeaders[GameController.boardSize - 1 - i]);
        
        