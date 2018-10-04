# StayAwake
A command-line utility that helps you stay awake by playing alarms in response to inactivity.

## Prerequisites<br>
Python modules from PyPI: progressbar, argparse, configparse, pynput, playsound

Copy `stayawake.conf` to your `~/.config/stayawake/stayawake.conf`. StayAwake will look for the config here unless otherwise specified. <br>
**Windows Users:** Since ~/.config does not exist on Windows, you have to specify the file with `-c`
