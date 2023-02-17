import chess.polyglot

from bot.eval_func import EvalFunction

class BotEngine:
    depth = 2;
    maxIter = 5000;
    
    def __init__(self):
        self.board = chess.Board();
    
    def getMove(self) -> chess.Move:
        try:
            move = chess.polyglot.MemoryMappedReader("bot/books/human.bin").weighted_choice(self.board).move;
            return move;
        except:
            bestMove = chess.Move.null();
            bestValue = -99999;
            alpha = -100000;
            beta = 100000;
            self.iter = 0;
            for move in self.board.legal_moves:
                self.board.push(move);
                boardValue = -self.alphaBeta(-beta, -alpha, self.depth - 1);
                if boardValue > bestValue:
                    bestValue = boardValue;
                    bestMove = move;
                if (boardValue > alpha):
                    alpha = boardValue;
                self.board.pop();
            return bestMove;
        
    def alphaBeta(self, alpha: int, beta: int, depthLeft: int):
        bestscore = -9999;
        self.iter += 1;
        if (depthLeft == 0):
            return self.quiescenceSearch(alpha, beta);
        for move in self.board.legal_moves:
            self.board.push(move);
            score = -self.alphaBeta(-beta, -alpha, depthLeft - 1);
            self.board.pop();
            if (score >= beta):
                return score;
            if (score > bestscore):
                bestscore = score;
            if (score > alpha):
                alpha = score;
            if self.iter >= self.maxIter:
                break;
        return bestscore;
    
    def quiescenceSearch(self, alpha: int, beta: int) -> int:
        self.iter += 1;
        if (self.iter >= self.maxIter):
            return beta;
        stand_pat = EvalFunction.eval(self.board);
        if (stand_pat >= beta):
            return beta;
        if (alpha < stand_pat):
            alpha = stand_pat;
        
        for move in self.board.legal_moves:
            if self.board.is_capture(move):
                self.board.push(move);
                score = -self.quiescenceSearch(-beta, -alpha);
                self.board.pop();
                
                if (score >= beta):
                    return beta;
                if (score > alpha):
                    alpha = score;
        return alpha;