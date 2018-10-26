#!/usr/bin/env python3
import threading
import time
import os
import sys
import datetime
import argparse
import shlex
import warnings

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, GLib, Gdk

from configload import configload
from wakeup import Waker
import monitor
import sleepnext

warnings.simplefilter('ignore')
# CLI options
options = argparse.ArgumentParser(
        description='The program that helps you stay awake.')
options.add_argument('-c','--config',
                     metavar='CONF', help='specify config file')
options.add_argument('-v','--verbose', action='store_true',
                     help='output more details')
options.parse_args()
verbose = options.parse_args().verbose
path = ''
if options.parse_args().config:
    path = os.path.expanduser(options.parse_args().config)
    print('Using configuration file: ' , path)
elif os.path.isfile('stayawake.conf'):
    path = 'stayawake.conf'
    print('Using configuration file: ', path)
elif os.path.isfile(os.path.expandvars(
                            '$HOME/.config/stayawake/stayawake.conf')):
    path = os.path.expanduser('~/.config/stayawake/stayawake.conf')
    print('Using configuration file: ', path)
else:
    print('Configuration file not found.\n\
        It should be named "stayawake.conf" in the same directory as \
          the executable or in $HOME/.config/stayawake/ (Unix only)')
    sys.exit()

settings = configload(path)
max_inactivity = datetime.timedelta(seconds=settings[0])
alarm_dir = settings[1]
volume_max_command = settings[2]
play_command = settings[3]
schedule_name = settings[4]
schedule = settings[5]
# Format schedule into lists
schedule = schedule.split()
schedule_pretty = ''
for i in range(0,len(schedule)):
    schedule[i] = schedule[i].split('-')
for i in range(0,len(schedule)):
    schedule_pretty += schedule[i][0]
    schedule_pretty += '-'
    schedule_pretty += schedule[i][1]
    schedule_pretty += ' '
sleep_names = settings[6]
sleep_names = shlex.split(sleep_names)

# Settings will be printed out to stdout in verbose mode
if verbose:
    print('max-inactivity = ', max_inactivity)
    print('alarm-folder = ', alarm_dir)
    print('volume-max-command = ', volume_max_command)
    print('play-command = ', play_command)
    print('schedule = ', schedule)
    print('sleep-names = ', sleep_names)


class Dashboard(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="StayAwake")
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=18)
        self.add(vbox)
        vbox.set_margin_top(20)
        vbox.set_margin_start(40)
        vbox.set_margin_end(40)

        title = Gtk.Label()
        title.set_markup("<span font_size='30720'>StayAwake</span>")
        vbox.add(title)

        config_label = Gtk.Label(label="Using:  " + path)
        vbox.add(config_label)

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
        schedule_box.get_row_at_index(0)\
            .do_activate(schedule_box.get_row_at_index(0))
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
        status_box.get_row_at_index(0)\
            .do_activate(status_box.get_row_at_index(0))
        vbox.add(status_box)

        activity_box = Gtk.ListBox()
        activity_label = Gtk.Label(label="Activity Monitor")
        self.activity_timer_label = Gtk.Label()
        suspend_label = Gtk.Label(label="Suspend Monitor")

        suspend_spinbutton_box = Gtk.Box()
        self.suspend_spin_button = Gtk.SpinButton()
        suspend_adjustment = Gtk.Adjustment(
            value=0, lower=0, upper=720, step_increment=1)
        self.suspend_spin_button.set_adjustment(suspend_adjustment)
        self.suspend_spin_button.set_numeric(True)
        suspend_minute = Gtk.Label()
        suspend_minute.set_text(' minutes ')
        suspend_apply = Gtk.Button.new_with_mnemonic('_Apply')
        suspend_apply.connect("clicked", self.on_suspend)
        suspend_cancel = Gtk.Button.new_with_mnemonic('_Cancel')
        suspend_cancel.connect("clicked", self.on_cancel)
        suspend_spinbutton_box.add(self.suspend_spin_button)
        suspend_spinbutton_box.add(suspend_minute)
        suspend_spinbutton_box.set_halign(Gtk.Align.CENTER)

        suspend_button_box = Gtk.Box()
        suspend_button_box.add(suspend_cancel)
        suspend_button_box.add(suspend_apply)
        suspend_button_box.set_halign(Gtk.Align.CENTER)

        activity_box.add(activity_label)
        activity_box.add(self.activity_timer_label)
        activity_box.add(suspend_label)
        activity_box.add(suspend_spinbutton_box)
        activity_box.add(suspend_button_box)
        activity_box.get_row_at_index(0)\
            .do_activate(activity_box.get_row_at_index(0))
        vbox.add(activity_box)

    def on_suspend(self, button):
        monitor.la = datetime.datetime.now() + datetime.timedelta(
            minutes=self.suspend_spin_button.get_value_as_int())
        self.activity_timer_label.set_text('The monitor will resume at: '
            + str(monitor.la)[:19])
        self.suspend_spin_button.set_value(0)

    def on_cancel(self, button):
        self.suspend_spin_button.set_value(0)
        monitor.la = datetime.datetime.now()

    def clock(self):
        now = datetime.datetime.now()
        diff = now - monitor.la
        self.status_time.set_text(str(now)[:19])
        if monitor.la < now:
            self.activity_timer_label.set_text(str(diff.seconds)
                + '.' + str(diff.microseconds)[:1]
                + 's / ' + str(max_inactivity.seconds) + 's')
        self.status_sleep_next.set_text('Next Sleep: '
                + sleepnext.next(schedule, sleep_names))
        self.status_time_remaining.set_text(sleepnext.time_remaining(schedule)
                + ' remaining')
        return True

    def start_clock(self):
        GLib.timeout_add(100, self.clock)

window = Dashboard()


def main():
    w = Waker(alarm_dir, volume_max_command, play_command)

    while 1:
        diff = datetime.datetime.now() - monitor.la
        if diff >= max_inactivity:
            # Label colour change
            window.activity_timer_label.override_background_color(0,
                Gdk.RGBA(red=1.0, green=0.0, blue=0.0, alpha=1.0))
            window.activity_timer_label.override_color(0,
                Gdk.RGBA(red=1.0, green=1.0, blue=1.0, alpha=1.0))
            # Alarm playing
            w.wakeup()
        if diff < max_inactivity:
            w.exit()
            window.activity_timer_label.override_background_color(0, None)
            window.activity_timer_label.override_color(0, None)
        time.sleep(1)


t = []
mouseactivity = threading.Thread(target=monitor.MouseMonitor)
keyboardactivity = threading.Thread(target=monitor.KeyboardMonitor)
main = threading.Thread(target=main)
t.append(mouseactivity)
t.append(keyboardactivity)
t.append(main)
mouseactivity.daemon = True
keyboardactivity.daemon = True
for thread in t:
    thread.daemon = True
    thread.start()


window.connect("destroy", Gtk.main_quit)
window.show_all()
window.start_clock()
Gtk.main()

