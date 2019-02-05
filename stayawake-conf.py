#!/usr/bin/env python3
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import configparser


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

        # Labels
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
        grid.addWidget(self.button_box_buttom, 17, 0)

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

app = QApplication(sys.argv)
window = ConfigHelper()
sys.exit(app.exec_())
