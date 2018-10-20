import os, configparser
def configload(path):
    config = configparser.ConfigParser()
    if path:
        config.read(path)
    else:
        config.read(os.path.expanduser('~/.config/stayawake/stayawake.conf'))
    max_inactivity = int(config['Settings']['max-inactivity'])
    alarm_dir = os.path.expanduser(config['Settings']['alarm-folder'])
    volume_max_command = config['Settings']['volume-max-command'] 
    play_command = config['Settings']['play-command']
    schedule_name = config['Settings']['schedule-name']
    schedule = config['Settings']['schedule']
    sleep_names = config['Settings']['sleep-names']
    if volume_max_command == '':
        print("Remember to turn the volume up to an unbearably high level!")
    return [max_inactivity, alarm_dir, volume_max_command, play_command, schedule_name, schedule, sleep_names]
