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



class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('StayAwake Qt')
        title = QLabel('StayAwake')
        title.setStyleSheet("font: 30pt")

        vbox = QVBoxLayout()
        vbox.setContentsMargins(30, 30, 30, 30)
        schedule_box = QListWidget() 
        status_box = QListWidget()
        monitor_box = QListWidget()
        schedule_box.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        current_schedule_label = QListWidgetItem("Current Schedule")
        schedule_name_label = QListWidgetItem(schedule_name)
        schedule_times_label = QListWidgetItem(schedule_pretty) 
        schedule_box.addItem(current_schedule_label)
        schedule_box.addItem(schedule_name_label)
        schedule_box.addItem(schedule_times_label)
        schedule_box.setCurrentRow(0)
        for i in range(0, schedule_box.count()):
            schedule_box.item(i).setTextAlignment(Qt.AlignCenter)
        status_label = QListWidgetItem('Current Time')
        self.status_time = QListWidgetItem()
        self.status_sleep_next = QListWidgetItem()
        self.status_remaining = QListWidgetItem()
        status_box.addItem(status_label) 
        status_box.addItem(self.status_time)
        status_box.addItem(self.status_sleep_next)
        status_box.addItem(self.status_remaining)
        status_box.setCurrentRow(0)
        status_box.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        for i in range(0, status_box.count()):
            status_box.item(i).setTextAlignment(Qt.AlignCenter)

        monitor_label = QListWidgetItem('Activity Monitor')
        self.monitor_timer = QListWidgetItem('5.3s / 90s')
        suspend_label = QListWidgetItem('Suspend Monitor')
        suspend_box = QWidget()
        suspend_box_layout = QHBoxLayout()
        self.suspend_spin_button = QSpinBox()
        minute_label = QLabel(' minutes')
        suspend_box_layout.addStretch()
        suspend_box_layout.addWidget(self.suspend_spin_button)
        suspend_box_layout.addWidget(minute_label)
        suspend_box_layout.addStretch()
        self.suspend_spin_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        suspend_box.setLayout(suspend_box_layout)
        button_box = QWidget()
        button_box_layout = QHBoxLayout()
        apply_button = QPushButton('Apply')
        apply_button.clicked.connect(self.on_suspend)
        cancel_button = QPushButton('Reset')
        cancel_button.clicked.connect(self.on_cancel)
        button_box_layout.addWidget(apply_button)
        button_box_layout.addWidget(cancel_button)
        button_box.setLayout(button_box_layout)
        suspend_box.setMaximumSize(QSize(1000, 90))

        suspend_box_row = QListWidgetItem()
        button_box_row = QListWidgetItem()

        monitor_box.addItem(monitor_label)
        monitor_box.addItem(self.monitor_timer)
        monitor_box.addItem(suspend_label)
        monitor_box.addItem(suspend_box_row)
        monitor_box.addItem(button_box_row)
        suspend_box_row.setSizeHint(QSize(100,60))
        monitor_box.setItemWidget(suspend_box_row, suspend_box)
        monitor_box.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        button_box_row.setSizeHint(QSize(10,60))
        monitor_box.setItemWidget(button_box_row, button_box)
        
        monitor_box.setCurrentRow(0)
        
        for i in range(0, monitor_box.count()):
            monitor_box.item(i).setTextAlignment(Qt.AlignCenter)

        vbox.addWidget(title)
        vbox.setAlignment(title, Qt.AlignCenter)
        vbox.addWidget(schedule_box)
        vbox.addWidget(status_box)
        vbox.addWidget(monitor_box)
        vbox.setAlignment(suspend_box, Qt.AlignCenter)
        self.setLayout(vbox)
        self.show()

        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(100)

    def update(self):
        now = datetime.datetime.now()
        diff = now - monitor.la
        self.status_time.setText(str(datetime.datetime.now())[:19])
        self.status_sleep_next.setText('Next Sleep: ' + sleepnext.next(schedule, sleep_names))
        self.status_remaining.setText(sleepnext.time_remaining(schedule) + ' remaining')

        if monitor.la < now: 
            self.monitor_timer.setText(str(diff.seconds)
                + '.' + str(diff.microseconds)[:1]
                + 's / ' + str(max_inactivity.seconds) + 's')

    def on_suspend(self):
        monitor.la = datetime.datetime.now()\
                + datetime.timedelta(minutes=self.suspend_spin_button.value())
        self.monitor_timer.setText('The monitor will resume at: '
            + str(monitor.la)[:19])
        if self.suspend_spin_button.value() is not 0:
            print('[' + str(datetime.datetime.now().time())[:8] + ']'\
                + ' Monitor suspended for '
                + str(self.suspend_spin_button.value())
                + ' minutes until '
                + str(monitor.la)[:19])
        self.suspend_spin_button.setValue(0)

    def on_cancel(self):
        monitor.la = datetime.datetime.now()
        self.suspend_spin_button.setValue(0)
        print(('[' + str(datetime.datetime.now().time())[:8] + ']'\
                + ' Monitor suspension is reset, now resuming...'))



def main():
    w = Waker(alarm_dir, volume_max_command, play_command)

    while 1:
        diff = datetime.datetime.now() - monitor.la
        if diff >= max_inactivity:
            # Label colour change
            # Alarm playing
            w.wakeup()
        if diff < max_inactivity:
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



app = QApplication(sys.argv)
window = Dashboard()
sys.exit(app.exec_())



