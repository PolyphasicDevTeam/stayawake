import os, configparser
def configload(path, config):
    if path:
        config.read(path)
    else:
        config.read(os.path.expanduser('~/.config/stayawake/stayawake.conf'))
    max_inactivity = int(config['Settings']['max-inactivity'])
    alarm_dir = os.path.expanduser(config['Settings']['alarm-folder'])
    volume_max_command = config['Settings']['volume-max-command'] 
    play_command = config ['Settings']['play-command']
    if volume_max_command == '':
        print("Remember to turn the volume up to an unbearably high level!")
    return [max_inactivity, alarm_dir, volume_max_command, play_command]
