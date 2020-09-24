from pynput import *
import datetime
la = datetime.datetime.now()

def on_event(*args):
    global la
    if la < datetime.datetime.now():
        la = datetime.datetime.now()
def MouseMonitor():
    with mouse.Listener(
        on_move=on_event,
        on_click=on_event,
        on_scroll=on_event) as listener:
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
        on_press=on_event,
        on_release=on_event) as listener:
        listener.join()
