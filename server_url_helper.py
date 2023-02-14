from os import path, remove

class ServerURLHelper:
    optFile = "serverurl.txt";
    defaultURL = "wss://localhost:7263/ws";
    
    @staticmethod
    def getServerURL() -> str:
        if path.isfile(ServerURLHelper.optFile):
            with open(ServerURLHelper.optFile) as f:
                return f.read();
        else:
            return ServerURLHelper.defaultURL;
        
    @staticmethod
    def saveServerURL(url: str) -> None:
        if url == ServerURLHelper.defaultURL:
            if path.isfile(ServerURLHelper.optFile):
                remove(ServerURLHelper.optFile);
        else:
            with open(ServerURLHelper.optFile, 'w') as f:
                f.writelines(url);