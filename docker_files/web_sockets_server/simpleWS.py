from SimpleWebSocketServer import WebSocket

class SimpleWS(WebSocket):

    def handleMessage(self):
        pass

    def handleConnected(self):
        
        self.server.appendClient(self)

        print (self.address, 'connected')

    def handleClose(self):

        self.server.removeClient(self)

        print (self.address, 'disconnected')