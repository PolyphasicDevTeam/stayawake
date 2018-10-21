# StayAwake
A GTK+ application that helps you stay awake by playing alarms in response to inactivity.

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
Python modules: pynput, pygobject
`pulseaudio` is used for auto-adjusting volume on Linux(It comes by default on most systems).
On Windows, install nircmd.
`mpg123` is the default player. It is available for both Windows and Linux under LGPLv2.1. It is included in the release binaries.

### Setup
Linux:  
Clone the repo, use either pip or your distro's package manager to install the dependencies, and run `./stayawake.py`.
Copy `stayawake.conf.sample` to your `~/.config/stayawake/stayawake.conf`. StayAwake will look for the config here unless there is a file name `stayawake.conf in the same directory as the executable or another file is specified with CLI options.  

Windows:  
Download the release binaries and extract the folder. Rename `stayawake.conf.sample` to `stayawake.conf` and edit it. To prevent errors, use a text editor that support UNIX line endings.
 
### Alarm Sounds
You can select files from [this](https://www.dropbox.com/s/dihn9m58wfnyxwk/alarm.rar) which is linked to by the now-abandoned [NMO](https://github.com/PolyphasicDevTeam/NoMoreOversleeps). Choose shorter alarms over longer ones.

### Todo
#### Near future
- GTK+ config helper
- time blocks for monitoring
#### Intermediate future
- Schedule statistics
- Discord integration
#### And the beyond
- Web integration
- Qt interface
