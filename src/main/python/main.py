from fbs_runtime.application_context.PyQt5 import ApplicationContext
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

from configload import configload
from wakeup import Waker
from schedule import Schedule
import monitor
options = argparse.ArgumentParser(
        description='Advanced wakeup alarm utility')
options.add_argument('-c','--config',
                     metavar='CONF', help='specify config file')
options.add_argument('-v','--verbose', action='store_true',
                     help='output more details')
options.parse_args()

verbose = options.parse_args().verbose



#
class ConfigHelper(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = configparser.ConfigParser()
        self.settings.add_section('Settings')
        if os.name == 'posix':
            self.userconfdir = os.path.join(os.path.expandvars('$HOME'),
                    '.config', 'stayawake')
        if os.name == 'nt':
            self.userconfdir = os.path.join(os.path.expandvars('%USERPROFILE%'),
                    'AppData', 'Roaming', 'stayawake')
        if not os.path.exists(self.userconfdir):
                os.makedirs(self.userconfdir)
        self.userconf = os.path.join(self.userconfdir, 'stayawake.conf')

        self.setWindowTitle("Configure StayAwake")

        self.max_inactivity = ''
        self.alarm_folder = ''
        self.volume_max_command = ''
        self.play_command = ''
        self.schedule_name = ''
        self.schedule = ''
        self.sleep_names = ''

        grid = QGridLayout()
        grid.setSpacing(20)
        grid.setContentsMargins(20, 20, 20, 20)

        boldFont=QFont()
        boldFont.setBold(True)
        # Labels
        restart_notice_label = QLabel("Restart StayAwake for changes to take effect.")
        restart_notice_label.setFont(boldFont)
        restart_notice_label.setAlignment(Qt.AlignCenter)
        inactv_label = QLabel("Maximum inactivity, in seconds")
        folder_label = QLabel("Alarm folder")
        vmaxcmd_label = QLabel("Command to maximise volume")
        playcmd_label = QLabel("Command to play audio")
        schedule_name_label = QLabel("Schedule name")
        schedule_times_label = QLabel("Sleep Times")
        schedule_ex_label = QLabel("\tExample: 22:00-2:30 7:00-7:30 13:40-14:00")
        sleep_names_label = QLabel("Sleep names")
        sn_ex_label = QLabel('\tExample: "Core" "Dawn Nap" "Noon Nap"')
        # Widgets
        self.inactv = QSpinBox()
        self.inactv.setMaximum(3600)
        self.folder = QPushButton("Choose a folder..")
        self.folder.clicked.connect(self.chooseFolder)
        self.vmaxcmd = QLineEdit()
        self.playcmd = QLineEdit()
        self.schedname = QLineEdit()
        self.sched = QLineEdit()
        self.sln = QLineEdit()

        self.button_box_top = QGroupBox()
        self.defaults = QPushButton("Use defaults")
        self.defaults.clicked.connect(self.toDefaults)
        self.read_local = QPushButton("Read Local")
        self.read_local.clicked.connect(self.readLocal)
        self.read_user = QPushButton("Read User")
        self.read_user.clicked.connect(self.readUser)
        hbox0 = QHBoxLayout()
        hbox0.addWidget(self.defaults)
        hbox0.addWidget(self.read_local)
        hbox0.addWidget(self.read_user)
        self.button_box_top.setLayout(hbox0)

        self.button_box_buttom = QGroupBox()
        self.delete_local = QPushButton("Delete Local")
        self.delete_local.clicked.connect(self.deleteLocal)
        self.save_user = QPushButton("Save User")
        self.save_user.clicked.connect(self.saveUser)
        self.save_local = QPushButton("Save Local")
        self.save_local.clicked.connect(self.saveLocal)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.delete_local)
        hbox1.addWidget(self.save_local)
        hbox1.addWidget(self.save_user)
        self.button_box_buttom.setLayout(hbox1)

        grid.addWidget(self.button_box_top, 0, 0)
        grid.addWidget(inactv_label, 1, 0)
        grid.addWidget(self.inactv, 2, 0)
        grid.addWidget(folder_label, 3, 0)
        grid.addWidget(self.folder, 4, 0)
        grid.addWidget(vmaxcmd_label, 5, 0)
        grid.addWidget(self.vmaxcmd, 6, 0)
        grid.addWidget(playcmd_label, 7, 0)
        grid.addWidget(self.playcmd, 8, 0)
        grid.addWidget(schedule_name_label, 9, 0)
        grid.addWidget(self.schedname, 10, 0)
        grid.addWidget(schedule_times_label, 11, 0)
        grid.addWidget(schedule_ex_label, 12, 0)
        grid.addWidget(self.sched, 13, 0)
        grid.addWidget(sleep_names_label, 14, 0)
        grid.addWidget(sn_ex_label, 15, 0)
        grid.addWidget(self.sln, 16, 0)
        grid.addWidget(restart_notice_label, 17, 0)
        grid.addWidget(self.button_box_buttom, 18, 0)

        self.setLayout(grid)
        self.show()

    def chooseFolder(self):
        self.alarm_folder = QFileDialog.getExistingDirectory(self, 'Choose a folder')
        self.folder.setText(self.alarm_folder)

    def configWrite(self, path):
        self.settings.set('Settings', 'max-inactivity',
                str(self.inactv.value()))
        self.settings.set('Settings', 'alarm-folder', self.alarm_folder)
        self.settings.set('Settings', 'volume-max-command',
                self.vmaxcmd.text())
        self.settings.set('Settings', 'play-command', self.playcmd.text())
        self.settings.set('Settings', 'schedule-name',
                self.schedname.text())
        self.settings.set('Settings', 'schedule', self.sched.text())
        self.settings.set('Settings', 'sleep-names', self.sln.text())
        with open(path, 'w') as configfile:
            self.settings.write(configfile)
            print('Configuration saved to ' + path + '.')

    def toDefaults(self):
        if os.name == 'posix':
            self.max_inactivity = 50
            self.alarm_folder = '~/Music/Alarms'
            self.volume_max_command = "pactl set-sink-mute 0 0 & pactl \
set-sink-volume 0 65535"
            self.play_command = 'mpg123 -q'
            self.schedule_name = 'E1'
            self.schedule = '22:00-04:00 11:00-11:20'
            self.sleep_names = '"Core" "Nap"'
            self.load()

        if os.name == 'nt':
            self.max_inactivity = 50
            self.alarm_folder = 'alarms'
            self.volume_max_command = ''
            self.play_command = '.\mpg123.exe -q'
            self.schedule_name = 'E1'
            self.schedule = '22:00-04:00 11:00-11:20'
            self.sleep_names = '"Core" "Nap"'
            self.load()

    def load(self):
        self.inactv.setValue(int(self.max_inactivity))
        self.folder.setText(self.alarm_folder)
        self.vmaxcmd.setText(self.volume_max_command)
        self.playcmd.setText(self.play_command)
        self.schedname.setText(self.schedule_name)
        self.sched.setText(self.schedule)
        self.sln.setText(self.sleep_names)

    def read(self):
        options = self.settings['Settings']
        self.max_inactivity = options.get('max-inactivity')
        self.alarm_folder = options.get('alarm-folder')
        self.volume_max_command = options.get('volume-max-command')
        self.play_command = options.get('play-command')
        self.schedule_name = options.get('schedule-name')
        self.schedule = options.get('schedule')
        self.sleep_names = options.get('sleep-names')

    def readLocal(self):
        print('Reading from stayawake.conf (Local)')
        self.settings.read('stayawake.conf')
        self.read()
        self.load()

    def readUser(self):
        print('Reading from user configuration: ' + self.userconf)
        self.settings.read(self.userconf)
        self.read()
        self.load()

    def deleteLocal(self):
        if os.path.isfile('stayawake.conf'):
            os.remove('stayawake.conf')
            print('Removed stayawake.conf (Local)')
        else:
            print("No local configuration file found.")

    def saveLocal(self):
        path = 'stayawake.conf'
        self.configWrite(path)

    def saveUser(self):
        self.configWrite(self.userconf)

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

# Main window
class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('StayAwake Qt')
        title = QLabel('StayAwake')
        version = QLabel("Version: 0.5")
        title.setStyleSheet("font: 30pt")
        self.path = ''
        pathunix = os.path.expandvars('$HOME/.config/stayawake/stayawake.conf')
        pathwin32 = os.path.expandvars('%USERPROFILE%\AppData\Roaming\stayawake\stayawake.conf')
        if options.parse_args().config:
            path = os.self.path.expanduser(options.parse_args().config)
        elif os.path.isfile('stayawake.conf'):
            self.path = 'stayawake.conf'
        elif os.path.isfile(pathunix):
            self.path = pathunix
        elif os.path.isfile(pathwin32):
            self.path = pathwin32
        else:
            self.path = None
            print('Configuration file not found.\n\
        It should be named "stayawake.conf" in the same directory as \
        the executable or in $HOME/.config/stayawake/ (Unix) \
        or in %USERPROFILE%\\AppData\\Roaming\\stayawake\\stayawake.conf (Windows)')
            #sys.exit()
        print('Using configuration file: ', os.path.abspath(self.path))
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
        print('[' + str(datetime.datetime.now().time())[:8] + ']' + ' Next sleep flexed ' + str(self.dialog.flex_spinbox.value()) + ' minutes')
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

class AppContext(ApplicationContext):           # 1. Subclass ApplicationContext
    def run(self):                              # 2. Implement run()

        path = ''
        pathunix = os.path.expandvars('$HOME/.config/stayawake/stayawake.conf')
        pathwin32 = os.path.expandvars('%USERPROFILE%\AppData\Roaming\stayawake\stayawake.conf')
        if options.parse_args().config:
            path = os.self.path.expanduser(options.parse_args().config)
        elif os.path.isfile('stayawake.conf'):
            path = 'stayawake.conf'
        elif os.path.isfile(pathunix):
            path = pathunix
        elif os.path.isfile(pathwin32):
            path = pathwin32
        else:
            path = None
            #sys.exit()
        #print('Using configuration file: ', self.path)

        if path:
            window = Dashboard()
            version = self.build_settings['version']
            window.setWindowTitle("HelloWorld v" + version)
            window.resize(250, 150)


        else:
            window = ConfigHelper()

        window.show()
        def main():
            w = Waker(window.alarm_dir, window.volume_max_command, window.play_command)

            while 1:
                if not window.schedule.isAsleep():
                    diff = datetime.datetime.now() - monitor.la
                    if diff >= window.max_inactivity:
                        # Label colour change
                        window.timer_label.setStyleSheet("color: #fff;" +
                                "background-color: #f00")
                        # Alarm playing
                        w.wakeup()
                    if diff < window.max_inactivity:
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

        return self.app.exec_()                 # 3. End run() with this line

if __name__ == '__main__':
    appctxt = AppContext()
                  # 4. Instantiate the subclass
    exit_code = appctxt.run()                   # 5. Invoke run()
    sys.exit(exit_code)
