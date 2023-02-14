from PyQt6 import QtCore, QtWebSockets
from PyQt6.QtCore import QUrl
from observable import Observable
from server_url_helper import ServerURLHelper

class WebsocketClient(QtCore.QObject):
    def __init__(self, parent):
        super().__init__(parent);
        
        self.obs = Observable();
        self.isConnected = False;

        self.client = QtWebSockets.QWebSocket("", QtWebSockets.QWebSocketProtocol.Version.Version13, None);
        # self.client.ignoreSslErrors();
        self.client.connected.connect(self.on_connect);
        self.client.error.connect(self.error);
        self.client.disconnected.connect(self.on_close);

        self.connect();
        self.client.pong.connect(self.onPong);
        
        self.client.textMessageReceived.connect(self.onMessage);

    def connect(self) -> None:
        if not self.isConnected:
            self.client.open(QUrl(ServerURLHelper.getServerURL()));
        
    def on_connect(self) -> None:
        print("Connected to WS");
        self.isConnected = True;
        self.obs.trigger("connected");
        
    def do_ping(self):
        print("client: do_ping");
        self.client.ping(b"foo");

    def onPong(self, elapsedTime, payload):
        print("onPong - time: {} ; payload: {}".format(elapsedTime, payload));

    def error(self, error_code):
        print("error code: {}".format(error_code));
        print(self.client.errorString());
        self.isConnected = False;
        self.obs.trigger("error");

    def close(self):
        self.client.close();
        
    def on_close(self):
        print("WS remote close");
        self.isConnected = False;
        self.obs.trigger("closed");
        
    def send_message(self, msg):
        if not self.isConnected:
            self.obs.once("connected", lambda: self.send_message(msg));
            return;
        
        print("client: send_message: ", msg);
        self.client.sendTextMessage(msg);
        
    def onMessage(self, payload):
        print("onMessage; payload: {}".format(payload));
        self.obs.trigger("msg", payload);