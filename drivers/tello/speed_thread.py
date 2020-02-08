import threading
from datetime import datetime
import time

time_cycle = 500 # ms 

class SpeedThread(threading.Thread):
    
    def __init__(self, parent):
    
        #Threading
        self.kill_event = threading.Event()
        self.stop_event = threading.Event()
        self.parent = parent
        self.init = False
        threading.Thread.__init__(self, args=self.stop_event)
        #print('Creating speed thread')
    
    def run(self):
        while (not self.kill_event.is_set()):

            start_time = datetime.now()
            if not self.stop_event.is_set():
                self.init = True
                self.parent.velocity_control()

            finish_Time = datetime.now()

            dt = finish_Time - start_time
            ms = (dt.days * 24 * 60 * 60 + dt.seconds) * \
                1000 + dt.microseconds / 1000.0
            #print (ms)
            if (ms < time_cycle):
                time.sleep((time_cycle - ms) / 1000.0)

    def stop(self):
        self.kill_event.set()

