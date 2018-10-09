#!/usr/bin/python
import threading, time, argparse, os, configparser, sys, signal, random, progressbar
from pynput import *
from datetime import datetime
from playsound import playsound
config = configparser.ConfigParser()
# CLI options
options = argparse.ArgumentParser(description='The program that helps you stay awake.')
options.add_argument('-c','--config', metavar='CONF', help='specify config file')
options.add_argument('-v','--verbose', action='store_true',  help='output more details')
options.parse_args()

# Load config file
max_inactivity = 60 
alarm_dir = '~/Music/alarms/'
verbose = False
if os.uname().sysname == 'Linux':
    volume_max_command = "pactl set-sink-volume `pacmd list-sources | grep -m 1 -e device.string | cut -d'\"' -f2` 100%"
else:
    volume_max_command = ''
play_command = ''

def configload():
    if options.parse_args().config:
        config.read(os.path.expanduser(options.parse_args().config))
        print('Using configuration file: ' , os.path.expanduser(options.parse_args().config))
    else:
        config.read(os.path.expanduser('~/.config/stayawake/stayawake.conf'))
        print('Using default configuration file: ', '~/.config/stayawake/stayawake.conf')
    global max_inactivity
    global alarm_dir
    global verbose
    global volume_max_command
    global play_command
    max_inactivity = int(config['Settings']['max-inactivity'])
    alarm_dir = os.path.expanduser(config['Settings']['alarm-folder'])
    verbose = options.parse_args().verbose
    volume_max_command = config['Settings']['volume-max-command'] 
    play_command = config ['Settings']['play-command']
    if volume_max_command == '':
        print("Remember to turn the volume up to an unbearably high level!")
if verbose:
    print('max-inactivity = ', max_inactivity)
    print('alarm-folder = ', alarm_dir)
    print('volume-max-command = ', volume_max_command)
    print('play-command = ', play_command)

# Second counter
s = 0


def wakeup():
    timenow = datetime.now().time()
    soundfile = os.path.join(alarm_dir, random.choice(os.listdir(alarm_dir)))
    print("\n", str(timenow)[:8], "Wake Up!", "Now Playing ", soundfile)
    if volume_max_command != '':
        os.system(volume_max_command)
    if play_command != '':
        os.system(play_command + ' ' + soundfile)
    else:
        playsound(soundfile)
def MouseMonitor():
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

def KeyboardMonitor():
    def on_press(key):
        global s
        s = 0
        #print('Key pressed.')

    def on_release(key):
        global s
        s = 0
        #print('Key released.')
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
        listener.join()

configload()
threads = []
mouseactivity = threading.Thread(target=MouseMonitor)
keyboardactivity = threading.Thread(target=KeyboardMonitor)
threads.append(mouseactivity)
threads.append(keyboardactivity)
for thread in threads:
    thread.daemon = True
    thread.start()
    
if not verbose:
    bar = progressbar.ProgressBar(maxval=max_inactivity, widgets=[progressbar.Bar('=','[',']'), ' ', progressbar.Percentage()])
    bar.start()
while 1:
    time.sleep(1)
    s = s + 1
    if verbose:
        print(str(s)+'s ', end='', flush=True)
    elif s <= max_inactivity:
        bar.update(s)
    if s > max_inactivity:
        if verbose:
            print('Wake up!!')
        wakeup()
