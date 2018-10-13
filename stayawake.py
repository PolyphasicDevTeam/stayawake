#!/usr/bin/env python3
import threading, time, argparse, os, configparser, sys, progressbar
from configload import configload
from wakeup import wakeup
import monitor
config = configparser.ConfigParser()
# CLI options
options = argparse.ArgumentParser(description='The program that helps you stay awake.')
options.add_argument('-c','--config', metavar='CONF', help='specify config file')
options.add_argument('-v','--verbose', action='store_true',  help='output more details')
options.parse_args()
verbose = options.parse_args().verbose
path = ''
if options.parse_args().config:
    path = os.path.expanduser(options.parse_args().config)
    print('Using configuration file: ' , path)
else:
    print('Using default configuration file: ', os.path.expanduser('~/.config/stayawake/stayawake.conf'))

settings = configload(path, config)
max_inactivity = settings[0]
alarm_dir = settings[1]
volume_max_command = settings[2]
play_command = settings[3]
# Settings will be printed out to stdout in verbose mode
if verbose:
    print('max-inactivity = ', max_inactivity)
    print('alarm-folder = ', alarm_dir)
    print('volume-max-command = ', volume_max_command)
    print('play-command = ', play_command)

threads = []
mouseactivity = threading.Thread(target=monitor.MouseMonitor)
keyboardactivity = threading.Thread(target=monitor.KeyboardMonitor)
threads.append(mouseactivity)
threads.append(keyboardactivity)
for thread in threads:
    thread.daemon = True
    thread.start()
    
# In verbose mode, instead of a progress bar, the number of seconds will be continuously printed to stdout.
if not verbose:
    bar = progressbar.ProgressBar(maxval=max_inactivity, widgets=[progressbar.Bar('=','[',']'), ' ', progressbar.Percentage()])
    bar.start()
while 1:
    time.sleep(1)
    if verbose:
        print(str(monitor.s)+'s ', end='', flush=True)
    elif monitor.s <= max_inactivity:
        bar.update(monitor.s)
    monitor.s = monitor.s + 1
    if monitor.s > max_inactivity:
        if verbose:
            print('Wake up!!')
        wakeup(alarm_dir, volume_max_command, play_command)
