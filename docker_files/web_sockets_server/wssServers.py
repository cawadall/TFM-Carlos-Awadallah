# SimpleWebSocketServer imports
import ssl
from SimpleWebSocketServer import WebSocket, SimpleSSLWebSocketServer
import threading


class SimpleWSSServer (SimpleSSLWebSocketServer):
    def __init__(self, host, port, websocketclass, cert, key, version = ssl.PROTOCOL_TLSv1, selectInterval = 0.1):

        SimpleSSLWebSocketServer.__init__(self, host, port,
                                        websocketclass, cert, key, version, selectInterval)

        self._lock_clients = threading.Lock()
        self._clients = []


    def close(self):
        super(SimpleWSSServer, self).close()


    def serveforever(self):
        super(SimpleWSSServer, self).serveforever()

    def appendClient(self, client):
        self._lock_clients.acquire()
        self._clients.append(client)
        self._lock_clients.release()

    def removeClient(self, client):
        self._lock_clients.acquire()
        self._clients.remove(client)
        self._lock_clients.release()

    def sendMessage(self, message):
        
        self._lock_clients.acquire()
        my_clients = list(self._clients)
        self._lock_clients.release()
        for client in my_clients:
            client.sendMessage(unicode(message, "utf-8"))


class ThreadingWSSServer(threading.Thread):
    def __init__(self, host, port, websocketclass, cert, key, version = ssl.PROTOCOL_TLSv1, selectInterval = 0.1):
        super(ThreadingWSSServer, self).__init__()
        self._stop_event = threading.Event()
        self._server = SimpleWSSServer(host, port, websocketclass, cert, key, version, selectInterval)


    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def sendMessage(self, message):
        self._server.sendMessage(message)

    def run(self):
        self._server.serveforever()
