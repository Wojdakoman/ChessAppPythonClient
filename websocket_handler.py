from observable import Observable

class Websockethandler:
    def __init__(self, wsClient):
        self.ws = wsClient;
        self.obs = Observable();
        self.action = None;
        
        self.subscribe();
        
    def subscribe(self):
        self.ws.obs.on("msg", self.on_message);
        self.ws.obs.on("error", self.on_error);
        self.ws.obs.on("closed", self.on_close);
        
    def ping(self):
        self.ws.do_ping();
        
    def login(self, login, password):
        self.ws.connect();
        self.ws.send_message("L:{} P:{}".format(login, password));
        self.action = "login";
        
    def logout(self, reason):
        self.ws.send_message("LO:{}".format(reason));
        
    def close(self):
        self.ws.close();
        
    def findGame(self):
        self.ws.send_message("FG");
        self.action = "findGame";
        
    def getPossibleMoves(self, row: int, col: int):
        self.ws.send_message("GM R:{} C:{}".format(row, col));
        self.action = "possibleMoves";
        
    def performMove(self, current_row: int, current_col: int, destination_row: int, destination_column: int):
        self.ws.send_message("GM RO:{} CO:{} RN:{} CN:{}".format(current_row, current_col, destination_row, destination_column));
        
    def giveUp(self):
        self.ws.send_message("GM GO");
        
    def getOpponentsDetails(self):
        self.ws.send_message("GM ED");
        self.action = "opponentsDetails";
        
    def on_message(self, msg):
        print("on_message: {}".format(msg));
        
        if self.action == "login":
            self.action = None;
            self.obs.trigger("login", msg == "L OK");
        elif self.action == "findGame" and "GS: ST" in msg:
            self.action = None;
            self.obs.trigger("gameStart", msg);
        elif self.action == "possibleMoves" and "GMOV:" in msg:
            self.action = None;
            self.obs.trigger("possibleMoves", msg.replace("GMOV: ", ""));
        elif self.action == "opponentsDetails" and "GMES:" in msg:
            self.action = None;
            self.obs.trigger("opponentsDetails", msg.replace("GMES:", "").strip());
        elif "GBRD:" in msg:
            self.obs.trigger("boardData", msg.replace("GBRD: ", ""));
        elif "GPOSTOP:" in msg:
            self.obs.trigger("startPosition", msg.replace("GPOSTOP: ", ""));
        elif "GTRN:" in msg:
            self.obs.trigger("turnChange", msg.replace("GTRN: ", ""));
        elif "GS: GO" in msg:
            self.obs.trigger("gameOver", msg.replace("GS: GO ", ""));
            
    def on_error(self):
        print("on_error");
        
        if self.action == "login":
            self.obs.trigger("login", False);
        elif self.action == "findGame":
            self.obs.trigger("gameStart", False);
            
    def on_close(self):
        self.on_error();
        self.obs.trigger("WSclosed");