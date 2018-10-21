from pynput import *
import datetime
la = datetime.datetime.now() 
def MouseMonitor():
#    def on_move(x, y):
#        global s
#        s = 0
#        #print('Pointer moved to {0}'.format((x, y)))
        

    def on_scroll(x, y, dx, dy):
        global la 
        if la < datetime.datetime.now():
            la = datetime.datetime.now() 
    def on_click(x, y, button, pressed):
        global la 
        if la < datetime.datetime.now():
            la = datetime.datetime.now() 

    with mouse.Listener(
        #on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll) as listener:
            listener.join()

def KeyboardMonitor():
    def on_press(key):
        global la 
        if la < datetime.datetime.now():
            la = datetime.datetime.now() 

    def on_release(key):
        global la 
        if la < datetime.datetime.now():
            la = datetime.datetime.now() 
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
        listener.join()

