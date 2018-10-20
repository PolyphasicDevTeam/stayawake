from multiprocessing import Value
from ctypes import c_double
from pynput import *
s = Value(c_double, 0.0)
def MouseMonitor():
#    def on_move(x, y):
#        global s
#        s = 0
#        #print('Pointer moved to {0}'.format((x, y)))
        

    def on_scroll(x, y, dx, dy):
        global s
        s.value = 0
    def on_click(x, y, button, pressed):
        global s
        s.value = 0
        #print('{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y)))

    with mouse.Listener(
        #on_move=on_move,
        on_click=on_click) as listener:
        listener.join()

def KeyboardMonitor():
    def on_press(key):
        global s
        s.value = 0
        #print('Key pressed.')

    def on_release(key):
        global s
        s.value = 0
        #print('Key released.')
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
        listener.join()

