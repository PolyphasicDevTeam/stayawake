import os, configparser
def configload(path):
    config = configparser.ConfigParser()
    config.read(path)
    max_inactivity = int(config['Settings']['max-inactivity'])
    alarm_dir = os.path.expanduser(config['Settings']['alarm-folder'])
    volume_max_command = config['Settings']['volume-max-command'] 
    play_command = config['Settings']['play-command']
    schedule_name = config['Settings']['schedule-name']
    schedule = config['Settings']['schedule']
    sleep_names = config['Settings']['sleep-names']
    if volume_max_command == '':
        print("Remember to turn the volume up to an unbearably high level!")
    retdict = {"max_inactivity": max_inactivity,
                "alarm_dir": alarm_dir, 
                "volume_max_command": volume_max_command, 
                "play_command": play_command, 
                "schedule_name": schedule_name,
                "schedule": schedule, 
                "sleep_names": sleep_names}
    return retdict
