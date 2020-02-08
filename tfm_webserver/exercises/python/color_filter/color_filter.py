#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('/usr/lib/python2.7/')
import types
import yaml

from os import path
import traceback
import threading
import time
from datetime import datetime

import cv2
import base64
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import clear_output, display
import ipywidgets as w
from SimpleWebSocketServer import WebSocket, SimpleSSLWebSocketServer, SimpleWebSocketServer

class SimpleWS(WebSocket):

    def handleMessage(self):
        pass

    def handleConnected(self):
        
        self.server.appendClient(self)

        print (self.address, 'connected')

    def handleClose(self):

        self.server.removeClient(self)

        print (self.address, 'disconnected')

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

def getWebSocketServer(host, port):
    return ThreadingWSServer(host, port, SimpleWS)

# Websockets Image Streaming
from tornado import websocket
import tornado.ioloop
import base64
from PIL import Image
import io

class WebSocketImagesClient(websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        print "Websocket Opened"

    def on_message(self, message):
        message = message.replace('data:image/png;base64,', '')
        png_recovered = base64.decodestring(message)
        im = Image.open(io.BytesIO(png_recovered))
        #print im
        self.application.image = im #png_recovered
        self.application.width, self.application.height = im.size
        self.application.streaming = True
        #f = open("temp.png", "w")
        #f.write(png_recovered)
        #f.close()
        #self.write_message(u"You said: %s" % message)

    def on_close(self):
        print "Websocket closed"
        tornado.ioloop.IOLoop.instance().stop()


class WebRTCCameraClient():
    
    def __init__(self):
        self.application = tornado.web.Application([(r"/", WebSocketImagesClient),])
        self.image = None
        self.width = 640
        self.height = 480 
        self.listen()

    def listen(self):
        self.application.listen(8889)
        self.application.opened = True
        self.application.streaming = False
        #tornado.ioloop.IOLoop.instance().start()

    def isOpened(self):
        return self.application.opened

    def get(self, dim):
        size = [0,0,0,self.width,self.height]
        return size[dim]

    def read(self):
        frame = self.getImage()
        return 1, np.asarray(frame)

    def getImage(self):
        if self.application.streaming:
            self.image = self.application.image
            self.width = self.application.width
            self.height = self.application.height
            #print self.image
            return self.image
        else:
            return Image.new('RGB', (self.width, self.height))

class Camera:

    def getImage(self):
        ''' Gets the image from the webcam and returns it. '''
        return self.image

    def update(self):
        ''' Updates the camera with a frame from the device every time the thread changes. '''
        if self.cam:
            self.lock.acquire()
            _, frame = self.cam.read()
            if self.transcoding:
                self.image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                self.image = frame
            self.lock.release()

    
class ThreadCamera(threading.Thread):

    def __init__(self, cam):
        ''' Threading class for Camera. '''

        self.t_cycle = 50      # ms

        self.cam = cam
        threading.Thread.__init__(self)

    def run(self):
        ''' Updates the thread. '''
        while(True):
            start_time = datetime.now()
            self.cam.update()
            end_time = datetime.now()

            dt = end_time - start_time
            dtms = ((dt.days * 24 * 60 * 60 + dt.seconds) * 1000
                + dt.microseconds / 1000.0)

            delta = max(self.t_cycle, dtms)
            self.framerate = int(1000.0 / delta)

            if(dtms < self.t_cycle):
                time.sleep((self.t_cycle - dtms) / 1000.0)

class LocalCamera(Camera):

    def __init__ (self, device_idx, im_server):
        ''' Camera class gets images from a video device and transform them
        in order to detect objects in the image.
        '''
        self.lock = threading.Lock()

        if im_server == 0:
            # via WebRTC:
            self.cam = WebRTCCameraClient()
            self.transcoding = False
        elif im_server == 1:
            # via OpenCV:
            self.cam = cv2.VideoCapture(device_idx)
            self.transcoding = True
        else:
            print("%d is not a valid Image Server in this machine." % (im_server))
        
        if not self.cam.isOpened():
            print("%d is not a valid device index in this machine." % (device_idx))
            raise SystemExit("Please check your camera id (hint: ls /dev)")

        self.width = int(self.cam.get(3))
        self.height = int(self.cam.get(4))
        self.image = np.zeros((self.height, self.width,3), np.uint8)
        
        self.trackImage = np.zeros((self.height, self.width,3), np.uint8)
        self.trackImage.shape = self.height, self.width, 3

        self.thresholdImage = np.zeros((self.height,self. width,1), np.uint8)
        self.thresholdImage.shape = self.height, self.width,


class LocalVideo(Camera):

    def __init__ (self, video_path):
        ''' Camera class gets images from a video device and transform them
        in order to detect objects in the image.
        '''
        self.lock = threading.Lock()
        video_path = path.expanduser(video_path)

        if not path.isfile(video_path):
            raise SystemExit('%s does not exists. Please check the path.' % (video_path))

        self.cam = cv2.VideoCapture(video_path)
        if not self.cam.isOpened():
            print("%d is not a valid device index in this machine." % (device_idx))
            raise SystemExit("Please check your camera id (hint: ls /dev)")

        self.width = self.cam.get(3)
        self.height = self.cam.get(4)
        self.image = np.zeros((self.height, self.width,3), np.uint8)

        self.trackImage = np.zeros((self.height, self.width,3), np.uint8)
        self.trackImage.shape = self.height, self.width, 3

        self.thresholdImage = np.zeros((self.height,self. width,1), np.uint8)
        self.thresholdImage.shape = self.height, self.width,


def selectVideoSource(cfg):
    """
    @param cfg: configuration
    @return cam: selected camera
    @raise SystemExit in case of unsupported video source
    """
    source = cfg['Introrob']['Source']
    if source.lower() == 'local':
        #from local_camera import Camera
        cam_idx = cfg['Introrob']['Local']['DeviceNo']
        cam_server = cfg['Introrob']['Local']['Server']
        print('  Chosen source: local camera (index %d)' % (cam_idx))
        cam = LocalCamera(cam_idx, cam_server)
    elif source.lower() == 'video':
        #from local_video import Camera
        video_path = cfg['Introrob']['Video']['Path']
        print('  Chosen source: local video (%s)' % (video_path))
        cam = LocalVideo(video_path)
    #elif source.lower() == 'stream':
        # comm already prints the source technology (ICE/ROS)
        #import comm
        #import config
        #cfg = loadConfig('color_filter_conf.yml')
        #jdrc = comm.init(cfg, 'Introrob')
        #proxy = jdrc.getCameraClient('Introrob.Stream')
        #from stream_camera import Camera
        #cam = Camera(proxy)
    else:
        raise SystemExit(('%s not supported! Supported source: Local, Video, Stream') % (source))

    return cam


def readConfig():
    try:
        with open('color_filter_conf.yml', 'r') as stream:
            return yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        raise SystemExit('Error: Cannot read/parse YML file. Check YAML syntax.')
    except:
        raise SystemExit('\n\tFILE "color_filter_conf.yml" DOES NOT EXIST\n')

class ColorFilter ():

    def __init__(self):

        cfg = readConfig()
        self.camera = selectVideoSource(cfg)
        self.playpausebutton = None
        self.toggle = None
        # Threading the camera...
        t_cam = ThreadCamera(self.camera)
        t_cam.start()

        self.wsserver = getWebSocketServer('0.0.0.0', '9001')
        self.wsserver.start()
        self.wsserverstream = getWebSocketServer('0.0.0.0', '9002')
        self.wsserverstream.start()
        self.algorithm = MyAlgorithm(self.camera, self.wsserver, self.wsserverstream)
        
        print "Color filter initialized OK"
        
    def play(self):
        # self.unpause_physics_client()
        self.algorithm.play()
        print "Color filter is running"
        
    def pause (self):
        self.algorithm.pause()
        #self.pause_physics_client()
        print "Color filter has been paused"
         
    def stop(self):
        self.algorithm.stop()
        print "Color filter stopped"
                   
    def setExecute(self, execute):
        self.algorithm.algorithm = types.MethodType(execute, self.algorithm )
        print "Code updated"  

    def get_filtered_image (self):
        return self.algorithm.get_filtered_image()
    
    def get_color_image (self):
        return self.algorithm.get_color_image()

# Auxiliary Images functions
# -------------------------------------------------------------
'''def printImage(image):
    plt.axis('off')
    a = plt.imshow(image)
    plt.show()

def printVideo(image):
    #plt.close()
    plt.axis('off')
    v = plt.imshow(image)
    plt.show()
    time.sleep(2)
    plt.close()'''

def img2String(img):
    if len(img.shape) > 2:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    retval, buffer = cv2.imencode('.jpg', img)
    jpg_as_text = base64.b64encode(buffer)
    return "data:image/jpeg;base64, "+jpg_as_text
# ---------------------------------------------------------------

time_cycle = 80
class MyAlgorithm(threading.Thread):

    def __init__(self, camera, wsserver, wsserverstream):
        self.camera = camera
        self.started = False
        self.wsserver = wsserver
        self.wsserverstream = wsserverstream
        #self.func = None
        
        self.filtered_image = np.zeros((480,640,3), np.uint8)
        self.color_image = np.zeros((480,640,3), np.uint8)
        #self.visualizationIterator = 0
        #self.visualizationEnabled = False

        self.stop_event = threading.Event()
        self.stop_event.set()
        self.kill_event = threading.Event()
        self.lock = threading.Lock()
        self.filtered_image_lock = threading.Lock()
        self.color_image_lock = threading.Lock()
        threading.Thread.__init__(self, args=self.stop_event)

    def run (self):

        while (not self.kill_event.is_set()):

            self.stop_event.wait()
            
            start_time = datetime.now()

            self.algorithm()
            self.cameraStreaming()
            #self.visualizationIterator += 1    

            finish_Time = datetime.now()

            dt = finish_Time - start_time
            ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
            
            if (ms < time_cycle):
                time.sleep((time_cycle - ms) / 1000.0)

    def pause (self):
        # Academic Pause
        self.stop_event.clear()
        
    def play (self):
        self.stop_event.set()
        if not self.started:
          self.start()
          self.started = True

    def stop (self):
        self.kill_event.set()

    def cameraStreaming(self):
        img  = self.camera.getImage()
        imgStr = img2String(img)
        self.wsserverstream.sendMessage(imgStr)
        
        
    def set_color_image (self, image):
        img  = np.copy(image)
        #if len(img.shape) == 2:
        #  img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        self.color_image_lock.acquire()
        self.color_image = img
        self.color_image_lock.release()
        imgStr = img2String(img)
        #print(imgStr)
        self.wsserver.sendMessage(imgStr)
        
    def get_color_image (self):
        self.color_image_lock.acquire()
        img = np.copy(self.color_image)
        self.color_image_lock.release()
        return img
    
        
    def set_filtered_image (self, image):
        img = np.copy(image)
        #if len(img.shape) == 2:
        #  img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        self.filtered_image_lock.acquire()
        self.filtered_image = img
        self.filtered_image_lock.release()
        #plt.axis('off') # printImage
        #a = plt.imshow(img)
        #time.sleep(0.1)
        imgStr = img2String(img)
        self.wsserver.sendMessage(imgStr)
        
    def get_filtered_image (self):
        self.filtered_image_lock.acquire()
        img  = np.copy(self.filtered_image)
        self.filtered_image_lock.release()
        return img

    '''def printFilteredImage(self):
        printImage(self.filtered_image)'''

    def algorithm(self):
        image = self.camera.getImage()
        # Add your code here

        #SHOW THE FILTERED IMAGE ON THE GUI
        self.set_color_image(image)


