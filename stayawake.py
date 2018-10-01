#!/usr/bin/env python3
import threading
import time
import os
import sys
import datetime
import argparse
import shlex
import warnings
import configparser
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from conf import ConfigHelper, OptionDialog
from configload import configload
from wakeup import Waker
from schedule import Schedule
import monitor

# CLI options
options = argparse.ArgumentParser(
        description='Advanced wakeup alarm system written in PyQt5')
options.add_argument('-c','--config',
                     metavar='CONF', help='specify config file')
options.add_argument('-v','--verbose', action='store_true',
                     help='output more details')
options.parse_args()

verbose = options.parse_args().verbose
path = ''






class Dashboard(QWidget):
    wake = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle('StayAwake')
        title = QLabel('StayAwake')
        version = QLabel("Version: 0.5.1")
        title.setStyleSheet("font: 30pt")

        self.wake.connect(self.create_confirmation_dialog)
        self.microsleep_count = 0

        self.path = ''
        pathwin32 = os.path.expandvars('%USERPROFILE%\AppData\Roaming\stayawake\stayawake.conf')

        if sys.platform.startswith("linux"):
            if os.path.isfile('stayawake.conf'):
                self.path = 'stayawake.conf'
                self.path = os.path.abspath(self.path)
            elif os.path.isfile(os.path.expandvars('$HOME/.config/stayawake/stayawake.conf')):
                self.path = os.path.expandvars('$HOME/.config/stayawake/stayawake.conf')
            else:
                self.path = "/etc/stayawake.conf"

        if sys.platform.startswith("win32"):
            pathwin32 = os.path.expandvars('%USERPROFILE%\AppData\Roaming\stayawake\stayawake.conf')
            if os.path.isfile('stayawake.conf'):
                self.path = 'stayawake.conf'
            elif os.path.isfile(pathwin32):
                self.path = pathwin32

        if sys.platform.startswith("darwin"):
            if os.path.isfile('stayawake.conf'):
                self.path = 'stayawake.conf'
            elif os.path.isfile(os.path.expandvars('$HOME/.config/stayawake/stayawake.conf')):
                self.path = os.path.expandvars('$HOME/.config/stayawake/stayawake.conf')
            else:
                self.path = "/etc/stayawake.conf"
        # Alias for option values
        settings = configload(self.path)
        self.max_inactivity = datetime.timedelta(seconds=settings['max_inactivity'])
        self.alarm_dir = settings['alarm_dir']
        self.volume_max_command = settings['volume_max_command']
        self.play_command = settings['play_command']
        self.schedule_name = settings['schedule_name']
        self.sleep_names = settings['sleep_names']
        self.schedule = Schedule(settings['schedule'], settings['sleep_names'])

        configpath_label = QLabel("Configuration file:\n" + os.path.abspath(self.path))
        configpath_label.setStyleSheet("font: 10pt")
        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(30, 30, 30, 30)

        self.vbox.addWidget(title)
        self.vbox.addWidget(version)
        self.vbox.addWidget(configpath_label)
        self.setLayout(self.vbox)

        self.schedule_box = QGroupBox("Schedule Information")
        self.vbox1 = QVBoxLayout()
        self.status_box = QGroupBox("Status")
        vbox2 = QVBoxLayout()
        self.monitor_box = QGroupBox("Activity Monitor")
        vbox3 = QVBoxLayout()

        # Top section
        self.schedule_name_label = QLabel("Schedule: " + self.schedule_name)
        self.schedule_times_label = QLabel(self.schedule.prettify())
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
        self.wakeups_label = QLabel()
        vbox3.addWidget(self.wakeups_label)
        self.monitor_box.setLayout(vbox3)
        self.vbox.addWidget(self.monitor_box)


        options_button = QPushButton("Options..")
        options_button.clicked.connect(self.on_options)
        self.vbox.addWidget(options_button)

        configure_button = QPushButton("Configure..")
        configure_button.clicked.connect(self.on_configure)
        self.vbox.addWidget(configure_button)


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
        if self.schedule.isAsleep():
            self.next_label.setText(awake_msg)
            self.remaining_label.setText(awake_msg)
            self.timer_label.setText(awake_msg)
        else:
            self.next_label.setText('Next Sleep: ' + self.schedule.next())
            self.remaining_label.setText(self.schedule.remaining() + ' remaining')
            if monitor.la < now:
                self.timer_label.setText(str(diff.seconds)
                    + '.' + str(diff.microseconds)[:1]
                    + 's / ' + str(self.max_inactivity.seconds) + 's')


    def on_suspend(self):
        'Callback function when the Apply button is pressed'
        monitor.la = datetime.datetime.now()\
                + datetime.timedelta(minutes=self.dialog.suspend_spinbox.value())
        self.timer_label.setText('The monitor will resume at:\n'
            + str(monitor.la)[:19])
        if self.dialog.suspend_spinbox.value() != 0:
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
        self.schedule.pristine()
        self.schedule.flex_next_sleep(self.dialog.flex_spinbox.value())
        self.schedule_times_label.setText(self.schedule.prettify())
        print('[' + str(datetime.datetime.now().time())[:8] + ']' +
                ' Next sleep flexed ' + str(self.dialog.flex_spinbox.value())
                + ' minutes')
        self.dialog.flex_spinbox.setValue(0)

    def on_pristine(self):
        'Callback function to restore the schedule into its pristine state'
        self.dialog.flex_spinbox.setValue(0)
        self.schedule.pristine()
        self.schedule_times_label.setText(self.schedule.prettify())
        print('[' + str(datetime.datetime.now().time())[:8] + ']' + ' Schedule reset to pristine conditions')

    def on_configure(self):
        self.conf_helper = ConfigHelper()
        self.conf_helper.show()

    def create_confirmation_dialog(self):
        val = QMessageBox.question(self, 'Confirm Microsleep', "Was that an actual microsleep?", QMessageBox.Yes | QMessageBox.No)
        if val == QMessageBox.Yes:
            self.microsleep_count += 1
        if val == QMessageBox.No:
            pass

    def get_confirmation_dialog(self):
        self.wake.emit()

app = QApplication(sys.argv)
window = Dashboard()


def main():
    start_time = datetime.datetime.now()
    ringing = False
    prev_ringing = False
    waking = False
    wakeups = 0
    w = Waker(window.alarm_dir, window.volume_max_command, window.play_command)

    while not window.schedule.isAsleep():
        diff = datetime.datetime.now() - monitor.la
        if diff >= window.max_inactivity:
            # Label colour change
            window.timer_label.setStyleSheet("color: #fff;" +
                    "background-color: #f00")
            # Alarm playing
            prev_ringing = ringing
            ringing = 1
            w.wakeup()
            if(prev_ringing != ringing):
                wakeups += 1
                waking = True

        if diff < window.max_inactivity:
            if(waking):
                window.get_confirmation_dialog();
                waking = False
            prev_ringing = ringing
            ringing = 0
            window.timer_label.setStyleSheet("")
            w.exit()
        window.wakeups_label.setText(str(window.microsleep_count) + " microsleeps in this session since " + str(start_time)[5:19])
        time.sleep(1)


mouseactivity = threading.Thread(target=monitor.MouseMonitor)
mouseactivity.daemon = True
mouseactivity.start()

keyboardactivity = threading.Thread(target=monitor.KeyboardMonitor)
keyboardactivity.daemon = True
keyboardactivity.start()

main = threading.Thread(target=main)
main.daemon = True
main.start()

sys.exit(app.exec_())
