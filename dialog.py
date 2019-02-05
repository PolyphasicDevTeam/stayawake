#!/usr/bin/env python
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

class OptionDialog(QDialog):
    def __init__(self, parent=None):
        super(OptionDialog, self).__init__(parent)
        self.setWindowTitle('StayAwake Options')
        self.label = QLabel("uwuuw")
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.label)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = OptionDialog()
    dialog.show()
    sys.exit(app.exec_())

