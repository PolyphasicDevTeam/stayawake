# StayAwake
Advanced wakeup alarm system

### Features
- Play alarms in response to predefined period of inactivity
- Auto-adjust volume for playing alarms
- Log each lapse in alertness
- Schedule dashboard
- Monitor suspend
- Automatically stays suspends during defined sleep times

### Prerequisites
Python 3.7
Python modules: `pynput`, `pygobject`(for GTK+) or `pyqt5`(for Qt)
`pulseaudio` is used for auto-adjusting volume on Linux(It comes by default on most systems).
On Windows, install `nircmd` and uncomment the line in the config.
`mpg123` is the default player. It is available for both Windows and Linux under LGPLv2.1. It is included in the Windows release binaries.

### Setup
Linux from source:  
Clone the repo, use either pip or your distro's package manager to install the dependencies, and Copy `stayawake.conf.sample` to your `~/.config/stayawake/stayawake.conf` and edit it according to your needs. Place the alarm sounds in the folder specified in the config file.(default: ~/Music/alarms) StayAwake looks for the config in the following places, with fallback:  
 - The file specified with `-c CONF` CLI option
 - In the same folder as the executable(`./stayawake.conf`)
 - ~/.config/stayawake/stayawake.conf  
Finally, run `./stayawake-gtk.py` or `./stayawake-qt.py`.

Linux with binary:  
Only the Qt frontend is provided in binaries.  
Install `mpg123`. Download the release binaries, place sound files in the alarms folder, rename and edit the config, and run the executable.

Windows with binary:  
Download the release binaries and extract the folder. Run 'stayawake-conf.exe' to configure StayAwake. "Save local" means to save the config file in the same folder as the executable and "Save user" means to save the file in your user config folder. You can only have a one user config, but any number of local configs. StayAwake always try to read the local config first. It will try to read your user config only when there is no file named 'stayawake.conf' in the same folder as the executable.
 
### GTK+ or Qt
StayAwake offers two frontends: GTK+3 and Qt5.  
GTK+ is better decorated, but the Qt5 frontend is more cross-platform.  
Linux users:  
If you are using a GTK+ based desktop environment(GNOME, LXDE, Xfce, MATE etc.), use the GTK+ frontend.  If you are using a Qt based desktop environment(KDE, LXQt), use the Qt frontend.  
Everyone else:  
Use the Qt frontend.

### Alarm Sounds
You can select files from [this](https://www.dropbox.com/s/dihn9m58wfnyxwk/alarm.rar) which is linked to by the now-abandoned [NMO](https://github.com/PolyphasicDevTeam/NoMoreOversleeps). Choose shorter alarms over longer ones.

### Safety Warning
Please note that I am in NO WAY responsible over ANY damage caused to you through the use of this tool. You are recommended to do something other than using a computer if you still fall asleep after several alarms. Repeated use of sound alarms might cause hearing damage and/or tolerance to alarms. YOU HAVE BEEN WARNED. 

### Known Issues:
- May not work on Wayland:
    This program depends on pynput to detect input activity, which does not include full wayland support yet. This might change in the future.
### Report a Bug
If you encounter any problems, please submit an issue.  
Try to provide the following information:  
- Your operating system
- Your python version
- Steps to reproduce
- The output with `-v` option
- Your config file

#### Near future
- Log file support
#### Intermediate future
- Integration with [thyme](https://github.com/sourcegraph/thyme)
- Schedule statistics
- Discord integration
#### And the beyond
- Web integration
