#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading
import time
import numpy as np
import libh264decoder
import cv2
from math import pi as PI
from speed_thread import SpeedThread

MAX_VEL = 1.5 # m/s
MIN_VEL = 0.1 # m/s
MAX_ROT_VEL = 1 # deg/s
MAX_ROT_VEL = 360 # deg/s

#ORANGE_MIN = np.array([0, 123, 165],np.uint8)#numpy.array([48, 138, 138],numpy.uint8)
#ORANGE_MAX = np.array([179, 255, 255],np.uint8)#numpy.array([67, 177, 192],numpy.uint8)
ORANGE_MIN = np.array([117, 239, 76],np.uint8)#numpy.array([48, 138, 138],numpy.uint8)
ORANGE_MAX = np.array([179, 255, 255],np.uint8)#numpy.array([67, 177, 192],numpy.uint8)

class Tello:
    """Wrapper class to interact with the Tello drone."""

    def __init__(self, local_ip, local_port, command_timeout=.2, tello_ip='192.168.10.1',
                 tello_port=8889):
        """
        Binds to the local IP/port and puts the Tello into command mode.

        :param local_ip (str): Local IP address to bind.
        :param local_port (int): Local port to bind.
        :param command_timeout (int|float): Number of seconds to wait for a response to a command.
        :param tello_ip (str): Tello IP.
        :param tello_port (int): Tello port.
        """

        # vels vector
        #   [
        #       Right(+)/Left(-),
        #       Forward(+)/Backward(-),
        #       Up(+)/Down(-),
        #       Yaw_right(+)/Yaw_left(-)
        #   ]
        self._vels = [0, 0, 0, 0]
        self.abort_flag = False
        self.decoder = libh264decoder.H264Decoder()
        self.command_timeout = command_timeout

        self.last_height = -1

        self._pitch = -1
        self._roll = -1
        self._yaw = -1
        self._vgx = -1
        self._vgy = -1
        self._vgz = -1
        self._templ = -1
        self._temph = -1
        self._tof = -1
        self._h = -1
        self._bat = -1
        self._baro = -1
        
        self.response = None  
        self.frame = None  # numpy array BGR -- current camera output frame
        #self.is_freeze = False  # freeze current camera output
        #self.last_frame = None

        # socket for sending cmd
        # ---------------------------------------------------------------------
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
        self.tello_address = (tello_ip, tello_port)
        self.socket.bind((local_ip, local_port))
        # ---------------------------------------------------------------------

        # thread for speed control
        # ---------------------------------------------------------------------
        self.kill_event = threading.Event()
        self.speed_thread = SpeedThread(self)
        # ---------------------------------------------------------------------

        # Thread and socket for receiving state updates 
        # ---------------------------------------------------------------------
        self.state_lock = threading.Lock()
        self.local_state_port = 8890  # port for receiving state updates
        self.socket_state = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_state.bind((local_ip, self.local_state_port))
        self.receive_state_thread = threading.Thread(target=self._receive_state_thread)
        self.receive_state_thread.daemon = True
        self.receive_state_thread.start()
        # ---------------------------------------------------------------------

        # Thread and socket for receiving video
        # ---------------------------------------------------------------------
        self.video_lock = threading.Lock()
        self.local_video_port = 11111  # port for receiving video stream
        self.socket_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for receiving video stream
        #self.last_height = 0
        self.socket_video.bind((local_ip, self.local_video_port))
        self.receive_video_thread = threading.Thread(target=self._receive_video_thread)
        self.receive_video_thread.daemon = True
        self.receive_video_thread.start()
        # ---------------------------------------------------------------------    

        # thread for receiving cmd ack
        self.receive_thread = threading.Thread(target=self._receive_thread)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        print("Conectando con Tello .....")
        # to receive video -- send cmd: command, streamon
        self.socket.sendto(b'command', self.tello_address)
        print ('[Tello] Preparando controlador')
        self.socket.sendto(b'streamon', self.tello_address)
        print ('[Tello] Preparando flujo de vídeo')

        time.sleep(2) # sleep to give time to the drone to get started
        print("Preparado.")
        

    def __del__(self):
        """Closes the local socket."""
        print("Desconectando...")
        self.close()

    def close(self):

        self.socket.close()
        self.socket_video.close()

        if self.speed_thread.is_alive():
            self.speed_thread.stop()
        self.stop_thread = True
        self.kill_event.set()

        #self.speed_thread.join()
        #self.receive_thread.join()
        self.receive_video_thread.join()
    
    #def read(self):
    #    """Return the last frame from camera."""
    #    if self.is_freeze:
    #        return self.last_frame
    #    else:
    #        return self.frame

    #def video_freeze(self, is_freeze=True):
    #    """Pause video output -- set is_freeze to True"""
    #    self.is_freeze = is_freeze
    #    if is_freeze:
    #        self.last_frame = self.frame

    def _receive_thread(self):
        """Listen to responses from the Tello.

        Runs as a thread, sets self.response to whatever the Tello last returned.

        """
        while True:
            try:
                self.response, ip = self.socket.recvfrom(3000)
                #print(self.response)
            except socket.error as exc:
                print ("Caught exception socket.error : %s" % exc)

    def _receive_state_thread(self):
        """
        Listens for state updates from the Tello.

        Runs as a thread.

        """
        while (not self.kill_event.is_set()):
            try:
                response, ip = self.socket_state.recvfrom(3000)
                #print(response)
                #if stop_t():
                #    print("Stopping response_thread")
                #    break
                data = response.decode("utf-8") .split(';')
                del data[-1]
                data2 = []
                for i in data:
                    data2.append(float(i.split(":")[1]))

                self.state_lock.acquire()
                self._pitch = data2[0]
                self._roll = data2[1]
                self._yaw = data2[2]
                self._vgx = data2[3]
                self._vgy = data2[4]
                self._vgz = data2[5]
                self._templ = data2[6]
                self._temph = data2[7]
                self._tof = data2[8]
                self._h = data2[9]
                self._bat = data2[10]
                self._baro = data2[11]
                self.state_lock.release()
            except socket.error as exc:
                print ("Caught exception socket.error : %s" % exc)
            time.sleep(0.1)
        print("state out")

    def get_image(self):
        """
        Return the last frame from camera.
        """
        #self.video_lock.acquire()
        img = np.copy(self.frame)
        #self.video_lock.release()
        return img

    def _receive_video_thread(self):
        """
        Listens for video streaming (raw h264) from the Tello.
        Runs as a thread, sets self.frame to the most recent frame Tello captured.
        """
        packet_data = ""
        while (not self.kill_event.is_set()):
            try:
                res_string, ip = self.socket_video.recvfrom(2048)
                packet_data += res_string
                # end of frame
                if len(res_string) != 1460:
                    for frame in self._h264_decode(packet_data):
                        self.frame = frame
                    packet_data = ""

            except socket.error as exc:
                print ("Caught exception socket.error : %s" % exc)
    
    def _h264_decode(self, packet_data):
        """
        decode raw h264 format data from Tello
        
        :param packet_data: raw h264 data array
       
        :return: a list of decoded frame
        """
        res_frame_list = []
        frames = self.decoder.decode(packet_data)
        for framedata in frames:
            (frame, w, h, ls) = framedata
            if frame is not None:
                # print 'frame size %i bytes, w %i, h %i, linesize %i' % (len(frame), w, h, ls)

                frame = np.fromstring(frame, dtype=np.ubyte, count=len(frame), sep='')
                frame = (frame.reshape((h, ls / 3, 3)))
                frame = frame[:, :w, :]
                res_frame_list.append(frame)

        return res_frame_list


    def _send_command_with_retry(self, command, retries):
        i = 0
        response = ""

        retries = 10
        while (response != "ok" and i < retries):
            if i > 0:
                print("Command: {}, retry: {}".format(command, i))
            self.send_command(command)
            i+=1
            #time.sleep(4)
            response = self.get_response()
            print(response)
            
        #time.sleep(4)
        self.response = None
        return response

    def send_command(self, command):
        """
        Send a command to the Tello and wait for a response.

        :param command: Command to send.
        :return (str): Response from Tello.

        """

        print (">> enviando comando: {}".format(command))
        self.abort_flag = False
        timer = threading.Timer(self.command_timeout, self.set_abort_flag)

        self.response = None
        self.socket.sendto(command.encode('utf-8'), self.tello_address)

        timer.start()
        while self.response is None:
            if self.abort_flag is True:
                break
        timer.cancel()
        
        if self.response is None:
            response = 'none_response'
        else:
            response = self.response.decode('utf-8')

        #self.response = None
        time.sleep(3) # Waiting for the order to get completed, when Tello sends its response
        return response
        #response = self.socket.sendto(command.encode('utf-8'), self.tello_address)
    
    def set_abort_flag(self):
        """
        Sets self.abort_flag to True.

        Used by the timer in Tello.send_command() to indicate to that a response
        
        timeout has occurred.

        """

        self.abort_flag = True

    def takeoff(self):
        """
        Initiates take-off.

        Returns:
            str: Response from Tello, 'OK' or 'FALSE'.

        """
        self._vels = [0, 0, 0, 0]
        response = self._send_command_with_retry('takeoff', 5)
        #response = self.send_command('takeoff')
        #self.speed_thread.start()
        return response

    # ------ VELOCITY CONTROL METHODS --------

    def velocity_control(self):
        # Bloque para comandos de velocidad no bloqueantes (modo Radio Control - RC -)
        # [0]      Right(+)/Left(-),
        # [1]       Forward(+)/Backward(-),
        # [2]       Up(+)/Down(-),
        # [3]       Yaw_right(+)/Yaw_left(-)
        print("Enviando comandos de velocidad: {} cm/s [vx], {} cm/s [vy], {} cm/s [vz], {} grad/s [az]".format(self._vels[0], self._vels[1], self._vels[2], self._vels[3]))

        self.send_command('rc %s %s %s %s' % (self._vels[0], self._vels[1], self._vels[2], self._vels[3]))
        #print("Sending RC command with speeds", self._vels)

    def set_velocities(self, vy, vx, vz, rot):
        if not self.speed_thread.is_alive():
            if not self.speed_thread.init:
                self.speed_thread.start()
                print("starting vel thread")
        else:
            if self.speed_thread.stop_event.is_set():
                self.speed_thread.stop_event.clear()
                
            
        self._vels = [vy, vx, vz, rot]

    def set_speed(self, speed):
        """
        Sets speed.

        This method expects Meters Per Second. The Tello API expects speeds from
        1 to 100 centimeters/second.

        Metric: .1 to 3.6 KPH

        Args:
            speed (int|float): Speed.

        Returns:
            str: Response from Tello, 'OK' or 'FALSE'.

        """

        speed = float(speed)

        #if self.imperial is True:
        #    speed = int(round(speed * 44.704))
        #else:
        speed = int(round(speed * 100))

        return self.send_command('speed %s' % speed)

    def check_vel(self, vel, sign):
        if vel > MAX_VEL: 
            vel = MAX_VEL
        elif vel < MIN_VEL:
            vel = MIN_VEL
        
        return vel*sign

    ## COMANDOS DE VELOCIDAD BLOQUEANTES (hasta que no termina una instruccion y
    ## se para, no comienza la siguiente - movimiento no fluido - )
    def set_vx(self, vel):
        self.speeds[0] = self.check_vel(vel, 1)
    
    def set_vy(self, vel):
        self.speeds[0] = self.check_vel(vel, -1)

    def set_vz(self, vel):
        self.speeds[1] = self.check_vel(vel, -1)
    
    def set_rot(self, vel):
        self.speeds[1] = self.check_vel(vel, 1)

    def stop(self):
        print("parando Tello...")
        self._vels = [0,0,0,0]

    # ------ POSITION CONTROL METHODS ------

    def rotate_cw(self, degrees):
        """
        Rotates clockwise.

        Args:
            degrees (int): Degrees to rotate, 1 to 360.

        Returns:
            str: Response from Tello, 'OK' or 'FALSE'.

        """
        if self.speed_thread.is_alive() and not self.speed_thread.stop_event.is_set():
            self.speed_thread.stop_event.set()
            #self.speed_thread.stop()
        return self._send_command_with_retry('cw %s' % degrees, 5)
        #return self.send_command('cw %s' % degrees)

    def rotate_ccw(self, degrees):
        """
        Rotates counter-clockwise.

        Args:
            degrees (int): Degrees to rotate, 1 to 360.

        Returns:
            str: Response from Tello, 'OK' or 'FALSE'.

        """
        if self.speed_thread.is_alive() and not self.speed_thread.stop_event.is_set():
            self.speed_thread.stop_event.set()
        return self._send_command_with_retry('ccw %s' % degrees, 5)
        #return self.send_command('ccw %s' % degrees)

    def flip(self, direction):
        """
        Flips.

        Args:
            direction (str): Direction to flip, 'l', 'r', 'f', 'b'.

        Returns:
            str: Response from Tello, 'OK' or 'FALSE'.

        """
        if self.speed_thread.is_alive() and not self.speed_thread.stop_event.is_set():
            self.speed_thread.stop_event.set()
        return self._send_command_with_retry('flip %s' % direction, 5)
        #return self.send_command('flip %s' % direction)


    def land(self):
        """Initiates landing.

        Returns:
            str: Response from Tello, 'OK' or 'FALSE'.

        """
        self._vels = [0, 0, 0, 0]
        #return self.send_command('land')
        return self._send_command_with_retry('land', 5)

    def move(self, direction, distance):
        """Moves in a direction for a distance.

        This method expects meters or feet. The Tello API expects distances
        from 20 to 500 centimeters.

        Metric: .02 to 5 meters

        Args:
            direction (str): Direction to move, 'forward', 'back', 'right' or 'left'.
            distance (int|float): Distance to move.

        Returns:
            str: Response from Tello, 'OK' or 'FALSE'.

        """
        if self.speed_thread.is_alive() and not self.speed_thread.stop_event.is_set():
            self.speed_thread.stop_event.set()
        distance = float(distance)

        #if self.imperial is True:
        #    distance = int(round(distance * 30.48))
        #else:
        distance = int(round(distance * 100))

        return self._send_command_with_retry('%s %s' % (direction, distance), 5)
        #return self.send_command('%s %s' % (direction, distance))

    def move_backward(self, distance):
        """Moves backward for a distance.

        See comments for Tello.move().

        Args:
            distance (int): Distance to move.

        Returns:
            str: Response from Tello, 'OK' or 'FALSE'.

        """
        return self.move('back', distance)

    def move_down(self, distance):
        """Moves down for a distance.

        See comments for Tello.move().

        Args:
            distance (int): Distance to move.

        Returns:
            str: Response from Tello, 'OK' or 'FALSE'.

        """
        return self.move('down', distance)

    def move_forward(self, distance):
        """Moves forward for a distance.

        See comments for Tello.move().

        Args:
            distance (int): Distance to move.

        Returns:
            str: Response from Tello, 'OK' or 'FALSE'.

        """
        return self.move('forward', distance)

    def move_left(self, distance):
        """Moves left for a distance.

        See comments for Tello.move().

        Args:
            distance (int): Distance to move.

        Returns:
            str: Response from Tello, 'OK' or 'FALSE'.

        """
        return self.move('left', distance)

    def move_right(self, distance):
        """Moves right for a distance.

        See comments for Tello.move().

        Args:
            distance (int): Distance to move.

        """
        return self.move('right', distance)

    def move_up(self, distance):
        """Moves up for a distance.

        See comments for Tello.move().

        Args:
            distance (int): Distance to move.

        Returns:
            str: Response from Tello, 'OK' or 'FALSE'.

        """

        return self.move('up', distance)


    # ------ VISION METHODS ------

    def get_object(self, lower=ORANGE_MIN, upper=ORANGE_MAX, showImageFiltered=False):
        
        """Color filter for object detection. Default object color is Orange.
		
        """
		# resize the image
        image = self.get_image()
        print(image.dtype)

		# convert to the HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

		# construct a mask for the color specified
		# then perform a series of dilations and erosions
		# to remove any small blobs left in the mask
        mask = cv2.inRange(hsv, ORANGE_MIN, ORANGE_MAX)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

		# find contours in the mask and
		# initialize the current center
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        area = 0

		# only proceed if at least one contour was found
        if len(cnts) > 0:
			# find the largest contour in the mask, then use
			# it to compute the minimum enclosing circle and
			# centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            area = M["m00"]

			# only proceed if the radius meets a minimum size
            if radius > 10:
				# draw the circle border
                cv2.circle(image, (int(x), int(y)), int(radius), (0, 255, 0), 2)

				# and the centroid
                cv2.circle(image, center, 5, (0, 255, 255), -1)
        if showImageFiltered:
            # Control waitKey from outside, only for local executions, not jupyter.
            return center, area, image, mask
        return center, area



    # ------ GETTER METHODS ------



    def get_response(self):
        """
        Returns response of tello.

        Returns:
            int: response of tello.

        """
        response = self.response
        return response

    def get_height(self):
        """Returns height(dm) of tello.

        Returns:
            int: Height(dm) of tello.

        """
        height = self._send_command_with_retry('height?',2)
        #height = self.send_command('height?')
        height = str(height)
        height = filter(str.isdigit, height)
        try:
            height = int(height)
            self.last_height = height
        except:
            height = self.last_height
            pass
        return height

    def get_battery(self):
        """Returns percent battery life remaining.

        Returns:
            int: Percent battery life remaining.

        """
        
        battery = self._send_command_with_retry('battery?',2)
        #battery = self.send_command('battery?')

        try:
            battery = int(battery)
        except:
            pass

        return battery

    def get_flight_time(self):
        """Returns the number of seconds elapsed during flight.

        Returns:
            int: Seconds elapsed during flight.

        """

        flight_time = self._send_command_with_retry('time?',2)
        #flight_time = self.send_command('time?')

        try:
            flight_time = int(flight_time)
        except:
            pass

        return flight_time

    def get_speed(self):
        """Returns the current speed.

        Returns:
            int: Current speed in KPH or MPH.

        """

        speed = self._send_command_with_retry('speed?',2)
        #speed = self.send_command('speed?')

        try:
            speed = float(speed)

            #if self.imperial is True:
            #    speed = round((speed / 44.704), 1)
            #else:
            speed = round((speed / 27.7778), 1)
        except:
            pass

        return speed
