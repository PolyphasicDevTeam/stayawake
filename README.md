# StayAwake
Advanced wakeup alarm system written using PyQt5

### Screenshot
![foobar](screenshot.png "StayAwake on GNOME with Arc OSX Qt Theme")
### Features
- Play alarms after to predefined period of inactivity
- Auto-adjust volume for playing alarms
- Log each inactivity
- Count microsleeps
- Schedule dashboard
- Monitor suspend
- Move sleep times
- Automatically suspends during defined sleep times

### How to Install
Go to the [Releases](https://github.com/PolyphasicDevTeam/stayawake/releases)
tab and download the most recent release.
On Linux it requires mpg123 to work properly.
Arch Linux Users: It is available as AUR package `stayawake-bin`
 
### Alarm Sounds
Collect many alarm sounds from whatever source you prefer. The program
randomly plays a file from the folder. Using many files is preferred to avoid
building tolerance too quickly. Choose shorter alarms over longer ones.

### Safety Warning
Please note that I am in NO WAY responsible over ANY damage caused to you through the use of this tool. You are recommended to do something other than using a computer if you still fall asleep after several alarms. Repeated use of sound alarms might cause hearing damage and/or tolerance to alarms. YOU HAVE BEEN WARNED. 

### Known Issues:
- May not work on Wayland:
    This program depends on pynput to detect input activity, which does not include full wayland support yet. This might change in the future.
- `Xlib.error.DisplayConnectionError: Can't connect to display ":0": b'Invalid MIT-MAGIC-COOKIE-1 key'`
    This appears to be a pynput bug. For the time being, use `xhost +` command
to circumvent this.

### Report a Bug
If you encounter any problems, please submit an issue.  
Try to provide the following information:  
- Your operating system
- Your python version
- Steps to reproduce
- Your config file
