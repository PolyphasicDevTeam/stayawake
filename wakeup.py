import subprocess, os, random
from threading import Thread
from datetime import datetime
import signal
class Waker(Thread):
    def __init__(self, alarm_dir, volume_max_command, play_command):
        super().__init__(target=self.wakeup, args=(alarm_dir, volume_max_command, play_command))
        self.dir = alarm_dir
        self.vup = volume_max_command 
        self.pcd = play_command
        self.file = None
        self.c = None
        self.first = True
    def wakeup(self):
        timenow = datetime.now().time()
        message = '[' + str(timenow)[:8] + ']' + " Wake Up! "\
            + "Now Playing " + os.path.join(
            self.dir, random.choice(os.listdir(self.dir)))
        if self.vup != '':
            os.system(self.vup)
        self.file = os.path.join(self.dir, random.choice(os.listdir(self.dir)))
        command = self.pcd + ' ' + self.file
        command = command.split()
        if self.first is True:
            self.first = False
            print(message)
            self.c = subprocess.Popen(command)
        if self.c.poll() is not None:
            print(message)
            self.c = subprocess.Popen(command)

    def exit(self):
        if self.c:
                if self.c.poll() is None:
                    self.c.kill()
