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
# Reading config file
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

# Alias for option values
settings = configload(path)
max_inactivity = datetime.timedelta(seconds=settings['max_inactivity'])
alarm_dir = settings['alarm_dir']
volume_max_command = settings['volume_max_command']
play_command = settings['play_command']
schedule_name = settings['schedule_name']
sleep_names = settings['sleep_names']
schedule = Schedule(settings['schedule'], settings['sleep_names'])

if verbose:
    print('max-inactivity = ', max_inactivity)
    print('alarm-folder = ', alarm_dir)
    print('volume-max-command = ', volume_max_command)
    print('play-command = ', play_command)
    print('schedule = ', schedule)
    print('sleep-names = ', sleep_names)


# Main window
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

        self.vbox.addWidget(title)
        self.vbox.addWidget(configpath_label)
        self.setLayout(self.vbox)

        self.schedule_box = QGroupBox("Schedule Information")
        self.vbox1 = QVBoxLayout()
        self.status_box = QGroupBox("Status")
        vbox2 = QVBoxLayout()
        self.monitor_box = QGroupBox("Activity Monitor")
        vbox3 = QVBoxLayout()

        # Top section
        self.schedule_name_label = QLabel("Schedule: " + schedule_name)
        self.schedule_times_label = QLabel(schedule.prettify())
        self.vbox1.addWidget(self.schedule_name_label)
        self.vbox1.addWidget(self.schedule_times_label)
        self.schedule_box.setLayout(self.vbox1)
        self.vbox.addWidget(self.schedule_box)
        
        # Middle section
        self.now_label = QLabel()
        self.next_label = QLabel()
        self.remaining_label = QLabel()
        vbox2.addWidget(self.now_label)
        vbox2.addWidget(self.next_label)
        vbox2.addWidget(self.remaining_label)
        self.status_box.setLayout(vbox2)
        self.vbox.addWidget(self.status_box)
        
        # Bottom section
        self.timer_label = QLabel()
        vbox3.addWidget(self.timer_label)
        self.monitor_box.setLayout(vbox3)
        self.vbox.addWidget(self.monitor_box)

        
        options_button = QPushButton("Options..")
        options_button.clicked.connect(self.on_options)
        self.vbox.addWidget(options_button)
        

        self.show()

        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(100)

  
    def update(self):
        'Update datetime and time remaining until next sleep'
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
        'Callback function when the Apply button is pressed'
        monitor.la = datetime.datetime.now()\
                + datetime.timedelta(minutes=self.dialog.suspend_spinbox.value())
        self.timer_label.setText('The monitor will resume at:\n'
            + str(monitor.la)[:19])
        if self.dialog.suspend_spinbox.value() is not 0:
            print('[' + str(datetime.datetime.now().time())[:8] + ']'\
                + ' Monitor suspended for '
                + str(self.dialog.suspend_spinbox.value())
                + ' minutes until '
                + str(monitor.la)[:19])
        self.dialog.suspend_spinbox.setValue(0)

    def on_cancel(self):
        'Callback function when Reset button is pressed'
        monitor.la = datetime.datetime.now()
        self.dialog.suspend_spinbox.setValue(0)
        print(('[' + str(datetime.datetime.now().time())[:8] + ']'\
                + ' Monitor suspension is reset, now resuming...'))

    def on_options(self):
        'Callback function when Options button is pressed'
        self.dialog = OptionDialog(self)
        self.dialog.show()

    def on_flex(self):
        'Callback function when Flex in Options is Applied'
        schedule.pristine()
        schedule.flex_next_sleep(self.dialog.flex_spinbox.value())
        self.schedule_times_label.setText(schedule.prettify())
        print('[' + str(datetime.datetime.now().time())[:8] + ']' + ' Next sleep flexed ' + str(self.dialog.flex_spinbox.value()) + ' minutes')
        self.dialog.flex_spinbox.setValue(0)

    def on_pristine(self):
        'Callback function to restore the schedule into its pristine state'
        self.dialog.flex_spinbox.setValue(0)
        schedule.pristine()
        self.schedule_times_label.setText(schedule.prettify())
        print('[' + str(datetime.datetime.now().time())[:8] + ']' + ' Schedule reset to pristine conditions')


app = QApplication(sys.argv)
window = Dashboard()

class OptionDialog(QDialog):
    def __init__(self, parent=None):
        super(OptionDialog, self).__init__(parent)
        self.setWindowTitle('StayAwake Options')
        label = QLabel("Options")
        label.setStyleSheet('font: 18pt')
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.addWidget(label)

        suspend_box = QGroupBox('Suspend Monitor')
        self.vbox1 = QVBoxLayout()
        self.suspend_spinbox = QSpinBox()
        self.suspend_spinbox.setMaximum(1200)
        self.suspend_spinbox.setMinimum(0)
        self.suspend_spinbox.setSuffix(' minutes')
        suspend_button_box = QWidget()
        suspend_button_layout = QHBoxLayout()
        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(parent.on_suspend)
        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(parent.on_cancel)
        suspend_button_layout.addWidget(apply_button)
        suspend_button_layout.addWidget(reset_button)
        suspend_button_box.setLayout(suspend_button_layout)
        self.vbox1.addWidget(self.suspend_spinbox)
        self.vbox1.addWidget(suspend_button_box)
        suspend_box.setLayout(self.vbox1)

        flex_box = QGroupBox('Flex Next Sleep')
        vbox2 = QVBoxLayout()
        flex_box.setLayout(vbox2)

        self.flex_spinbox = QSpinBox()
        self.flex_spinbox.setMaximum(720)
        self.flex_spinbox.setMinimum(-720)
        self.flex_spinbox.setSuffix(' minutes')

        flex_button_box = QWidget()
        flex_button_layout = QHBoxLayout()
        flex_button_box.setLayout(flex_button_layout)
        flex_button = QPushButton('Apply')
        flex_button.clicked.connect(parent.on_flex)
        pristine_button = QPushButton('Reset')
        pristine_button.clicked.connect(parent.on_pristine)
        flex_button_layout.addWidget(flex_button)
        flex_button_layout.addWidget(pristine_button)

        vbox2.addWidget(self.flex_spinbox)
        vbox2.addWidget(flex_button_box)
                
        layout.addWidget(suspend_box)
        layout.addWidget(flex_box)
        self.show()


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



