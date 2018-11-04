#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import configparser

settings = configparser.ConfigParser()

class ConfigHelper(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Configuration Helper"
        
        self.max_inactivity = ''
        self.alarm_folder = ''
        self.volume_max_command = ''
        self.play_command = ''
        self.schedule_name = ''
        self.schedule = ''
        self.sleep_names = ''

        grid = QGridLayout()
        
        inactv_label = QLabel("Maximum Inactivity, in seconds")
        sec_label = QLabel()

        
        self.inactv = QSlider(Qt.Horizontal)
        self.inactv.setTickPosition(QSlider.TicksBothSides)
        self.inactv.setTickInterval(30)
        self.inactv.setSingleStep(1)
        self.inactv.setMinimum(0)
        self.inactv.setMaximum(600)

        
        self.folder = QLineEdit()

        
        grid.addWidget(self.inactv, 0, 0)
        grid.addWidget(inactv_label, 1, 0)
        grid.addWidget(self.folder, 2, 0)

        self.setLayout(grid)
        self.show()

app = QApplication(sys.argv)
window = ConfigHelper()
sys.exit(app.exec_())


