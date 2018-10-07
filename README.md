# StayAwake
A command-line utility that helps you stay awake by playing alarms in response to inactivity.

### stayawake-gtk
Currently, this is just a model of what the future interface will look like. It does not have any features beyond what it looks.
### Prerequisites
Python modules from PyPI: progressbar, argparse, configparse, pynput, playsound
Modules for stayawake-gtk: gobject

### Setup
Copy `stayawake.conf` to your `~/.config/stayawake/stayawake.conf`. StayAwake will look for the config here unless otherwise specified. <br>
**Windows Users:** Since ~/.config does not exist on Windows, you must specify the file with `-c`. Since I don't have a Windows computer, other features might not work as well. If you found a bug specifically on Windows and you can fix it, please submit a pull request. I will happily accept them as long as they don't alter the program's functionality on Linux.
### Alarm Sounds
You can select files from [this](https://www.dropbox.com/s/dihn9m58wfnyxwk/alarm.rar) which is linked to by the now-abandoned [NMO](https://github.com/PolyphasicDevTeam/NoMoreOversleeps). Choose shorter alarms over longer ones.

### Todo
#### Near future
- suspend feature
- systemd service file
- time blocks
#### Intermediate future
- GTK+ interface for both program and config
- Schedule dashboard/statistics
- Discord integration
#### And the beyond
- Central server
- Qt interface
