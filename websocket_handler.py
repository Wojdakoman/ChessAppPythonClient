from observable import Observable

class Websockethandler:
    def __init__(self, wsClient):
        self.ws = wsClient;
        self.obs = Observable();
        self.action = None;
        
        self.subscribe();
        
    def subscribe(self):
        self.ws.obs.on("msg", self.on_message);
        self.ws.obs.on("closed", self.on_error);
        
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
        
    def on_message(self, msg):
        print("on_message: {}".format(msg));
        
        if self.action == "login":
            self.action = None;
            self.obs.trigger("login", msg == "L OK");
        elif self.action == "findGame" and "GS: ST" in msg:
            self.action = None;
            self.obs.trigger("gameStart", msg);
        elif "GBRD:" in msg:
            self.obs.trigger("boardData", msg.replace("GBRD: ", ""));
        elif "GPOSTOP:" in msg:
            self.obs.trigger("startPosition", msg.replace("GPOSTOP: ", ""));
            
    def on_error(self):
        print("on_error");
        
        if self.action == "login":
            self.obs.trigger("login", False);
        elif self.action == "findGame":
            self.obs.trigger("gameStart", False);