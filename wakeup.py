import subprocess, os, playsound, random
from multiprocessing import Process
from datetime import datetime
import signal
class Waker(Process):
    def __init__(self, alarm_dir, volume_max_command, play_command):
        super().__init__(target=self.wakeup, args=(alarm_dir, volume_max_command, play_command))
        signal.signal(signal.SIGTERM, self.exit)
        self.dir = alarm_dir
        self.vup = volume_max_command 
        self.pcd = play_command
        self.file = os.path.join(self.dir, random.choice(os.listdir(self.dir)))
        self.c = None
    def wakeup(self):
        timenow = datetime.now().time()
        print('[' + str(timenow)[:8] + ']', "Wake Up!", "Now Playing ", self.file)
        if self.vup != '':
            p = Process(target=subprocess.run, args=(self.vup,))
            p.daemon = True
            #p.start()
            print('volume maximised')
        if self.pcd != '':
            command = self.pcd + ' ' + self.file
            command = command.split()
            print(command)
            self.c = subprocess.Popen(command)
            print(self.c.pid)
            print('playing')
        else:
            p = Process(target=playsound.playsound, args=(self.file,))
            p.daemon = True
            p.start()
            print('playing')
            p.join()
    def exit(self):
            self.c.kill()
            super().terminate() 
    
