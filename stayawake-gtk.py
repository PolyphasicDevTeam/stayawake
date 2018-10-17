#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, GLib, Gdk
import monitor
import threading
import time
import os
import configparser
from datetime import datetime
from configload import configload
from wakeup import wakeup
import argparse
import sleepnext
import shlex

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
schedule_name = settings[4]
schedule = settings[5]
schedule = schedule.split()
schedule_pretty = ''
for i in range(0,len(schedule)):
    schedule[i] = schedule[i].split('-')
print(schedule)
for i in range(0,len(schedule)):
    schedule_pretty += schedule[i][0]
    schedule_pretty += '-'
    schedule_pretty += schedule[i][1]
    schedule_pretty += ' '
#print(len(schedule))
sleep_names = settings[6]
sleep_names = shlex.split(sleep_names)
print(sleep_names)

# Settings will be printed out to stdout in verbose mode
if verbose:
    print('max-inactivity = ', max_inactivity)
    print('alarm-folder = ', alarm_dir)
    print('volume-max-command = ', volume_max_command)
    print('play-command = ', play_command)

class Dashboard(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="StayAwake")
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.add(vbox)
        vbox.set_margin_top(30)
        vbox.set_margin_start(60) 
        vbox.set_margin_end(60) 
        
        title = Gtk.Label()
        title.set_markup("<span font_size='30720'>StayAwake</span>")
        vbox.add(title)
                
        config_label = Gtk.Label(label="Configuration file path:")
        config_path_entry = Gtk.Entry()
        config_path_entry.set_text("~/.config/stayawake/stayawake.conf")
        config_button = Gtk.Button(label="Use")
        config_box = Gtk.Box()
        config_box.pack_start(config_path_entry, True, True, 0)
        config_box.pack_end(config_button, False, False, 10)
        vbox.add(config_label)
        vbox.add(config_box)

        global schedule_name
        global schedule
        global schedule_pretty
        schedule_box = Gtk.ListBox()
        schedule_label = Gtk.Label(label="Current Schedule")
        schedule_name = Gtk.Label(label=schedule_name)
        schedule_times = Gtk.Label(label=schedule_pretty)
        schedule_box.add(schedule_label)
        schedule_box.add(schedule_name)
        schedule_box.add(schedule_times) 
        schedule_box.get_row_at_index(0).do_activate(schedule_box.get_row_at_index(0))
        vbox.add(schedule_box)

        status_box = Gtk.ListBox()
        status_label = Gtk.Label(label="Current Time")
        self.status_time = Gtk.Label()
        self.status_sleep_next = Gtk.Label()
        self.status_time_remaining = Gtk.Label()
        status_box.add(status_label)
        status_box.add(self.status_time)
        status_box.add(self.status_sleep_next)
        status_box.add(self.status_time_remaining)
        status_box.get_row_at_index(0).do_activate(status_box.get_row_at_index(0))
        vbox.add(status_box)
        
        activity_box = Gtk.ListBox()
        activity_label = Gtk.Label(label="Activity Monitor")
        self.activity_timer_label = Gtk.Label()
        monitor_suspend_label = Gtk.Label(label="*Dangerous* Suspend Monitor")
        

        suspend_button_box = Gtk.Box()
        suspend_button_5 = Gtk.Button(label="5min")
        suspend_button_15 = Gtk.Button(label="15min")
        suspend_button_30 = Gtk.Button(label="30min")
        suspend_button_box.add(suspend_button_5)
        suspend_button_box.add(suspend_button_15)
        suspend_button_box.add(suspend_button_30)
        suspend_button_box.set_halign(Gtk.Align.CENTER)

        activity_box.add(activity_label)
        activity_box.add(self.activity_timer_label)
        activity_box.add(monitor_suspend_label)
        activity_box.add(suspend_button_box)
        activity_box.get_row_at_index(0).do_activate(activity_box.get_row_at_index(0))
        vbox.add(activity_box)

    def clock(self):
        self.status_time.set_text(str(datetime.now())[:19])
        self.activity_timer_label.set_text("{:.1f}".format(monitor.s) + 's')
        self.status_sleep_next.set_text('Next Sleep: ' + sleepnext.next(schedule, sleep_names))
        self.status_time_remaining.set_text(sleepnext.time_remaining(schedule) + ' remaining')
        return True

    def start_clock(self):
        GLib.timeout_add(100, self.clock)

def counter():
    while 1:
        monitor.s += 0.1 
        time.sleep(0.1)

window = Dashboard()
        
def main():
    while 1:
        if monitor.s >= max_inactivity:
            window.activity_timer_label.override_background_color(0, Gdk.RGBA(red=1.0, green=0.0, blue=0.0, alpha=1.0))
            window.activity_timer_label.override_color(0, Gdk.RGBA(red=1.0, green=1.0, blue=1.0, alpha=1.0))
            wakeup(alarm_dir, volume_max_command, play_command)
        if monitor.s < max_inactivity:
            #print('Activity Resumes')
            window.activity_timer_label.override_background_color(0, None)
            window.activity_timer_label.override_color(0, None) 
        time.sleep(1)
            
threads = []
mouseactivity = threading.Thread(target=monitor.MouseMonitor)
keyboardactivity = threading.Thread(target=monitor.KeyboardMonitor)
counter = threading.Thread(target=counter)
main = threading.Thread(target=main)
threads.append(mouseactivity)
threads.append(keyboardactivity)
threads.append(counter)
threads.append(main)

for thread in threads:
    thread.daemon = True
    thread.start()


window.connect("destroy", Gtk.main_quit)
window.show_all()
window.start_clock()
Gtk.main()

