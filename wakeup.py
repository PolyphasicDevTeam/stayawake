import os, playsound, random
from datetime import datetime
def wakeup(alarm_dir, volume_max_command, play_command):
    timenow = datetime.now().time()
    soundfile = os.path.join(alarm_dir, random.choice(os.listdir(alarm_dir)))
    print("\n", '[' + str(timenow)[:8] + ']', "Wake Up!", "Now Playing ", soundfile)
    if volume_max_command != '':
        os.system(volume_max_command)
    if play_command != '':
        os.system(play_command + ' ' + soundfile)
    else:
        playsound(soundfile)

