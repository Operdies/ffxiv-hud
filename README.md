# ffxiv-hud
This is a simple overlay I use when playing FFXIV. It is intended to stay on top of all other programs,
but never take focus. This is not a bot or cheating suite. It is just meant to show relevant information
in a concise manner. How often do you tab out of the game to google something while playing an MMO?


For now, it has limited features, but I plan to extend it whenever I have time.
Currently, python is required to run it until I work out some kinks with PyInstaller, but this is not a priority
at this stage since I develop it for personal use, and I extend it with features when I feel something is missing, or I am bored.


# Current features:
## A textbox with the next unspoiled / ephemereal botanist node I am farming
This can be edited manually edited by making changes to data/schedule.txt
The format should be pretty straight forward from reading the file, and supports python-style comments.
Everything after a '#' sign is ignored. The program checks for changes to this file while it's running,
and updates automatically if the line parses correctly.

I plan to enable easy editing of this in the GUI in a future release.

Furthermore, right-clicking the text box toggles whether it should highlight when less than a minute remains.

## Mute button
A sound plays 30 seconds before the next node spawns if enabled.
The alert sound can be changed by changing the sound file data/alert.wav
Click to toggle.

I have not tested this with anything but .wav files, but other filetypes might be supported. (I use the playsound module)

## Venture buttons
Clicking these buttons start a timer of 1 hour right now, but the duration can be specified
in a future release. When no venture is active, they display the names of my own retainers, but this, as well
as the colors of the buttons, will also be customisable soon. Right-click to reset the timer. 


## Future stuff
See ./ideas.md file for planned features. I do not intend to implement anything that could
be perceived as cheating. This is only meant as a way to keep track of timers and information,
especially while logged out. I only started working on this as a pet project to learn TKinter very recently,
so stay tuned for updates.
