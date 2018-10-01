import threading
import time
import os
from pynput import *

s = 0

def wakeup():
    os.system("cvlc ~/programming/alarms/Chime.mp3 --play-and-exit")
def KeyboardMonitor():
    def on_move(x, y):
        global s
        s = 0
        #print('Pointer moved to {0}'.format((x, y)))
        

    def on_click(x, y, button, pressed):
        global s
        s = 0
        #print('{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y)))
    
    with mouse.Listener(
        on_move=on_move,
        on_click=on_click) as listener:
        listener.join()


threads = []
kb = threading.Thread(target=KeyboardMonitor)
threads.append(kb)
kb.start()
while 1:
    time.sleep(1)
    s = s + 1
    print(s)
    if s > 10:
        print('Wake up!!')
        wakeup()

