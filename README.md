# StayAwake
A command-line utility that helps you stay awake by playing alarms in response to inactivity.

### Features
- Play alarms in response to inactivity
- Auto-adjust volume for playing alarms
- Log each lapse in alertness

### Planned Features
- Monitor suspend
- Time block config
- Schedule dashboard

### Prerequisites
Python modules: progressbar, argparse, configparse, pynput, playsound, pygobject
`pulseaudio` is required for auto-adjusting volume on Linux.
`mpg123` will be used as the preferred player, with fallback being `playsound` python module.
### Setup
Linux:
Copy `stayawake.conf` to your `~/.config/stayawake/stayawake.conf`. StayAwake will look for the config here unless otherwise specified. <br>
Use either pip or your distro's package manager to install the dependencies.<br>

Windows Users: The only way to install `pygobject` on windows is through MSYS2. You can copy the config file to MSYS2 home config folder. You can also choose to use the console version instead, which do not require `pygobject`. For that, you always need to specify a config file with option `-c` since the default config path only works on Linux. 
### Alarm Sounds
You can select files from [this](https://www.dropbox.com/s/dihn9m58wfnyxwk/alarm.rar) which is linked to by the now-abandoned [NMO](https://github.com/PolyphasicDevTeam/NoMoreOversleeps). Choose shorter alarms over longer ones.

### Todo
#### Near future
- schedule configuration
- GTK+ config helper
- suspend feature
- time blocks
#### Intermediate future
- Schedule dashboard/statistics
- Discord integration
#### And the beyond
- Central server
- Qt interface
