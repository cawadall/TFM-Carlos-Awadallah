from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import subprocess
import os

class TelloWS(WebSocket):

    def handleMessage(self):
        print (type(self.data))
        runCommand(self.data)

def handleConnected(self):

    print (self.address, 'connected')

def handleClose(self):

    print (self.address, 'disconnected')

def runCommand(data):
    print(data)

    with open("tello_code.py", "w") as text_file:
        text_file.write(data)
    p = subprocess.Popen('python2 tello_code.py', stdout=subprocess.PIPE, shell=True)
    
    out, err = p.communicate()
    result = out.decode("utf-8").split('\n')
    
    for lin in result:
        if not lin.startswith('#'):
            print(lin)

    os.remove("tello_code.py")

    

server = SimpleWebSocketServer('', 9001, TelloWS)
server.serveforever()
