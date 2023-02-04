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
        self.ws.send_message("L:{} P:{}".format(login, password));
        self.action = "login";
        
    def logout(self, reason):
        self.ws.send_message("LO:{}".format(reason));
        
    def close(self):
        self.ws.close();
        
    def on_message(self, msg):
        print("on_message: {}".format(msg));
        
        if self.action == "login":
            self.obs.trigger("login", msg == "L OK");
            
    def on_error(self):
        print("on_error");
        
        if self.action == "login":
            self.obs.trigger("login", False);