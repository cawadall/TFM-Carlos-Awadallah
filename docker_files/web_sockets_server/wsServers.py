from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
import threading

class SimpleWSServer (SimpleWebSocketServer):
    def __init__(self, host, port, websocketclass, selectInterval = 0.1):

        SimpleWebSocketServer.__init__(self, host, port,
                                        websocketclass, selectInterval)

        self._lock_clients = threading.Lock()
        self._clients = []


    def close(self):
        super(SimpleWSServer, self).close()


    def serveforever(self):
        super(SimpleWSServer, self).serveforever()

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


class ThreadingWSServer(threading.Thread):
    def __init__(self, host, port, websocketclass, selectInterval = 0.1):
        super(ThreadingWSServer, self).__init__()
        self._stop_event = threading.Event()
        self._server = SimpleWSServer(host, port, websocketclass, selectInterval)


    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def sendMessage(self, message):
        self._server.sendMessage(message)

    def run(self):
        self._server.serveforever()