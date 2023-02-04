
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow
from websocket_client import WebsocketClient
from websocket_handler import Websockethandler

if __name__ == '__main__':
    app = QApplication([]);

    client = WebsocketClient(app);
    wsHandler = Websockethandler(client);
 
    window = MainWindow(wsHandler);
    window.show();
    
    app.exec();