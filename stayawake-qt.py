#!/usr/bin/env python3
import threading
import time
import os
import sys
import datetime
import argparse
import shlex
import warnings

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from configload import configload
from wakeup import Waker
from schedule import Schedule
import monitor

# CLI options
options = argparse.ArgumentParser(
        description='Advanced wakeup alarm utility')
options.add_argument('-c','--config',
                     metavar='CONF', help='specify config file')
options.add_argument('-v','--verbose', action='store_true',
                     help='output more details')
options.parse_args()
verbose = options.parse_args().verbose
path = ''
pathunix = os.path.expandvars('$HOME/.config/stayawake/stayawake.conf')
pathwin32 = os.path.expandvars('%USERPROFILE%\AppData\Roaming\stayawake\stayawake.conf')
if options.parse_args().config:
    path = os.path.expanduser(options.parse_args().config)
elif os.path.isfile('stayawake.conf'):
    path = 'stayawake.conf'
elif os.path.isfile(pathunix):
    path = pathunix
elif os.path.isfile(pathwin32):
    path = pathwin32
else:
    print('Configuration file not found.\n\
It should be named "stayawake.conf" in the same directory as \
the executable or in $HOME/.config/stayawake/ (Unix) \
or in %USERPROFILE%\\AppData\\Roaming\\stayawake\\stayawake.conf (Microsoft)')
    sys.exit()
print('Using configuration file: ', path)

settings = configload(path)
max_inactivity = datetime.timedelta(seconds=settings[0])
alarm_dir = settings[1]
volume_max_command = settings[2]
play_command = settings[3]
schedule_name = settings[4]
sleep_names = settings[6]
schedule = Schedule(settings[5], settings[6])

if verbose:
    print('max-inactivity = ', max_inactivity)
    print('alarm-folder = ', alarm_dir)
    print('volume-max-command = ', volume_max_command)
    print('play-command = ', play_command)
    print('schedule = ', schedule)
    print('sleep-names = ', sleep_names)



class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('StayAwake Qt')
        title = QLabel('StayAwake')
        title.setStyleSheet("font: 30pt")
        configpath_label = QLabel("Configuration file:\n" + path)
        configpath_label.setStyleSheet("font: 10pt")
        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(30, 30, 30, 30)

        self.schedule_box = QGroupBox("Schedule Information")
        vbox1 = QVBoxLayout()
        self.status_box = QGroupBox("Status")
        vbox2 = QVBoxLayout()
        self.monitor_box = QGroupBox("Activity Monitor")
        vbox3 = QVBoxLayout()

        self.schedule_name_label = QLabel("Schedule: " + schedule_name)
        self.schedule_times_label = QLabel(schedule.prettify())
        vbox1.addWidget(self.schedule_name_label)
        vbox1.addWidget(self.schedule_times_label)
        self.schedule_box.setLayout(vbox1)
        
        self.now_label = QLabel()
        self.next_label = QLabel()
        self.remaining_label = QLabel()
        vbox2.addWidget(self.now_label)
        vbox2.addWidget(self.next_label)
        vbox2.addWidget(self.remaining_label)
        self.status_box.setLayout(vbox2)
        
        self.timer_label = QLabel()
        self.suspend_label = QLabel("Suspend Monitor")
        self.suspend_spinbox = QSpinBox()
        self.suspend_spinbox.setMaximum(1200)
        self.suspend_spinbox.setMinimum(0)
        self.suspend_button_box = QWidget()
        self.suspend_button_layout = QHBoxLayout()
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.on_suspend)
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.on_cancel)
        self.suspend_button_layout.addWidget(self.apply_button)
        self.suspend_button_layout.addWidget(self.reset_button)
        self.suspend_button_box.setLayout(self.suspend_button_layout)
        vbox3.addWidget(self.timer_label)
        vbox3.addWidget(self.suspend_label)
        vbox3.addWidget(self.suspend_spinbox)
        vbox3.addWidget(self.suspend_button_box)
        self.monitor_box.setLayout(vbox3)
        

        self.vbox.addWidget(title)
        self.vbox.addWidget(configpath_label)
        self.vbox.addWidget(self.schedule_box)
        self.vbox.addWidget(self.status_box)
        self.vbox.addWidget(self.monitor_box)
        self.setLayout(self.vbox)
        self.show()

        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(100)

  
    def update(self):
        now = datetime.datetime.now()
        diff = now - monitor.la
        awake_msg = "Hey! You should be asleep now. What are you doing?"
        self.now_label.setText(str(datetime.datetime.now())[:19])
        if schedule.isAsleep():
            self.next_label.setText(awake_msg)
            self.remaining_label.setText(awake_msg)
            self.timer_label.setText(awake_msg)
        else:
            self.next_label.setText('Next Sleep: ' + schedule.next())
            self.remaining_label.setText(schedule.remaining() + ' remaining')
            if monitor.la < now: 
                self.timer_label.setText(str(diff.seconds)
                    + '.' + str(diff.microseconds)[:1]
                    + 's / ' + str(max_inactivity.seconds) + 's')


    def on_suspend(self):
        monitor.la = datetime.datetime.now()\
                + datetime.timedelta(minutes=self.suspend_spinbox.value())
        self.timer_label.setText('The monitor will resume at:\n'
            + str(monitor.la)[:19])
        if self.suspend_spinbox.value() is not 0:
            print('[' + str(datetime.datetime.now().time())[:8] + ']'\
                + ' Monitor suspended for '
                + str(self.suspend_spinbox.value())
                + ' minutes until '
                + str(monitor.la)[:19])
        self.suspend_spinbox.setValue(0)

    def on_cancel(self):
        monitor.la = datetime.datetime.now()
        self.suspend_spinbox.setValue(0)
        print(('[' + str(datetime.datetime.now().time())[:8] + ']'\
                + ' Monitor suspension is reset, now resuming...'))


app = QApplication(sys.argv)
window = Dashboard()

def main():
    w = Waker(alarm_dir, volume_max_command, play_command)

    while 1:
        if not schedule.isAsleep():
            diff = datetime.datetime.now() - monitor.la
            if diff >= max_inactivity:
                # Label colour change
                window.timer_label.setStyleSheet("color: #fff;" +
                        "background-color: #f00")
                # Alarm playing
                w.wakeup()
            if diff < max_inactivity:
                window.timer_label.setStyleSheet("")
                w.exit()
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

sys.exit(app.exec_())



