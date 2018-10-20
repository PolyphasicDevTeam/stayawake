import subprocess, os, playsound, random
from threading import Thread
from datetime import datetime
import signal
class Waker(Thread):
    def __init__(self, alarm_dir, volume_max_command, play_command):
        super().__init__(target=self.wakeup, args=(alarm_dir, volume_max_command, play_command))
        self.dir = alarm_dir
        self.vup = volume_max_command 
        self.pcd = play_command
        self.file = os.path.join(self.dir, random.choice(os.listdir(self.dir)))
        self.c = None
    def wakeup(self):
        timenow = datetime.now().time()
        print('[' + str(timenow)[:8] + ']', "Wake Up!", "Now Playing ", self.file)
        if self.vup != '':
            os.system(self.vup)
        command = self.pcd + ' ' + self.file
        command = command.split()
        print(command)
        self.c = subprocess.Popen(command)

    def exit(self):
        os.kill(self.c.pid, signal.SIGTERM)
