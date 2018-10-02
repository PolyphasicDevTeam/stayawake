# StayAwake
A command-line utility that helps you stay awake by playing alarms in response to inactivity.

Prerequisites: vlc <br>
Python modules from PyPI: progressbar, argparse, configparse, pynput

Copy `stayawake.conf` to your `~/.config/stayawake/stayawake.conf`. StayAwake will look for the config here unless otherwise specified.
**Windows Users:** Since ~/.config does not exist on Windows, you have to specify the file with `-c`
