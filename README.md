# StayAwake
An application that helps you stay awake by playing alarms in response to inactivity.

### Features
- Play alarms in response to predefined inactivity
- Auto-adjust volume for playing alarms
- Log each lapse in alertness
- Schedule dashboard
- Monitor suspend

### Planned Features
- Time block config
- Arctimes

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

Windows:  
Download the release binaries and extract the folder. Rename `stayawake.conf.sample` to `stayawake.conf` and edit it. To prevent errors, use a text editor that support UNIX line endings. Place the alarm sounds in the `alarms` folder or specify another folder in the config file. The GTK+ frontend is not supported on Windows.
 
### GTK+ or Qt
StayAwake offers two frontends: GTK+3 and Qt5.  
GTK+ is better decorated, but the Qt5 frontend is more cross-platform.  
Linux users:  
If you are using a GTK+ based desktop environment(GNOME, LXDE, Xfce, MATE etc.), use the GTK+ frontend.  
If you are using a Qt based desktop environment(KDE, LXQt), use the Qt frontend.  
Everyone else:  
Use the Qt frontend.

### Alarm Sounds
You can select files from [this](https://www.dropbox.com/s/dihn9m58wfnyxwk/alarm.rar) which is linked to by the now-abandoned [NMO](https://github.com/PolyphasicDevTeam/NoMoreOversleeps). Choose shorter alarms over longer ones.

### Issues
If you encounter any problems, please submit an issue.  
Provide the following information:  
- Your operating system
- Your python version
- The output with `-v` option
- Your config file

### Todo
#### Near future
- Log file support
- GUI config helper
- time blocks for monitoring
#### Intermediate future
- Schedule statistics
- Discord integration
#### And the beyond
- Web integration
