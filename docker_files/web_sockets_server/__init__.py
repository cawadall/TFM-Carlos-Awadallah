from .simpleWS import *
from .wsServers import *
from .wssServers import *
from .utils import *


def getWebSocketServer(host, port, ssl = False, cert=None, key=None, version = ssl.PROTOCOL_TLSv1):
    if ssl:
        return ThreadingWSSServer(host, port, SimpleWS, cert, key, version)
    else:
        return ThreadingWSServer(host, port, SimpleWS)