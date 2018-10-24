import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

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
        schedule_name_label = QListWidgetItem('E2')
        schedule_times_label = QListWidgetItem('uwu') 
        schedule_box.addItem(current_schedule_label)
        schedule_box.addItem(schedule_name_label)
        schedule_box.addItem(schedule_times_label)
        schedule_box.setCurrentRow(0)
        for i in range(0, schedule_box.count()):
            schedule_box.item(i).setTextAlignment(Qt.AlignCenter)
        status_label = QListWidgetItem('Current Time')
        status_time = QListWidgetItem('4:10')
        status_next_sleep = QListWidgetItem('Next Sleep:')
        status_time_remaining = QListWidgetItem('0:40:13 remainging')
        status_box.addItem(status_label) 
        status_box.addItem(status_time)
        status_box.addItem(status_next_sleep)
        status_box.addItem(status_time_remaining)
        for i in range(0, status_box.count()):
            status_box.item(i).setTextAlignment(Qt.AlignCenter)

        monitor_label = QListWidgetItem('Activity Monitor')
        monitor_timer = QListWidgetItem('5.3s / 90s')
        suspend_label = QListWidgetItem('Suspend Monitor')
        suspend_box = QWidget()
        suspend_box_layout = QHBoxLayout()
        suspend_spin_button = QSpinBox()
        minute_label = QLabel(' minutes')
        suspend_box_layout.addWidget(suspend_spin_button)
        suspend_box_layout.addWidget(minute_label)
        suspend_spin_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        suspend_box.setLayout(suspend_box_layout)
        button_box = QWidget()
        button_box_layout = QHBoxLayout()
        apply_button = QPushButton('Apply')
        cancel_button = QPushButton('Cancel')
        button_box_layout.addWidget(apply_button)
        button_box_layout.addWidget(cancel_button)
        button_box.setLayout(button_box_layout)
        suspend_box.setMaximumSize(QSize(200,90))

        suspend_box_row = QListWidgetItem()
        button_box_row = QListWidgetItem()

        monitor_box.addItem(monitor_label)
        monitor_box.addItem(monitor_timer)
        monitor_box.addItem(suspend_label)
        monitor_box.addItem(suspend_box_row)
        monitor_box.addItem(button_box_row)
        suspend_box_row.setSizeHint(QSize(100,60))
        monitor_box.setItemWidget(suspend_box_row, suspend_box)
        button_box_row.setSizeHint(QSize(10,60))
        monitor_box.setItemWidget(button_box_row, button_box)

        for i in range(0, monitor_box.count()):
            monitor_box.item(i).setTextAlignment(Qt.AlignCenter)

        vbox.addWidget(title)
        vbox.setAlignment(title, Qt.AlignCenter)
        vbox.addWidget(schedule_box)
        vbox.addWidget(status_box)
        vbox.addWidget(monitor_box)
        self.setLayout(vbox)
        self.show()


app = QApplication(sys.argv)
window = Dashboard()
sys.exit(app.exec_())



