# ffxiv-hud
This is a simple overlay I use when playing FFXIV. It is intended to stay on top of all other programs,
but never take focus. This is not a bot or cheating suite. It is just meant to show relevant information
in a concise manner. How often do you tab out of the game to google something while playing an MMO?
This is the process I seek to streamline.

For now, it has limited features, but I plan to extend it whenever I have time.
I am testing everything with ``python 3.6.5`` and the libraries specified in ``./requirements.txt.``
Currently, python is required to run it until I work out some kinks with PyInstaller, but this is not a priority
at this stage since I develop it for personal use, and I extend it with features when I feel something is missing, or I am bored.


# Current features:
## A textbox with the next unspoiled / ephemereal botanist node I am farming
This can be edited manually edited by making changes to data/schedule.txt
The format should be pretty straight forward from reading the file, and supports python-style comments.
Everything after a `#` sign is ignored. The program checks for changes to this file while it's running,
and updates automatically if the line parses correctly.

I plan to enable easy editing of this in the GUI in a future release.

Right-clicking the text box toggles whether it should highlight when less than a minute remains.

## Mute button
A sound plays 30 seconds before the next node spawns if enabled.
The alert sound can be changed by changing the sound file data/alert.wav
Click to toggle.

I have not tested this with anything but `.wav` files, but other filetypes might be supported. (I use the playsound module)

## Venture buttons
Clicking these buttons start a timer of 1 hour right now. Righ-clicking exposes a context
 menu where the venture timer can be set to 18 hours. When no venture is active, they display the names of my own retainers, 
 but this, as well as the colors of the buttons, will also be customisable in a future release. 
 Right-click to reset the timer. 
 
 ## GP bar
 Allows you to track your GP when you're in another spec. It currently assumes
 that you have unlocked 6 GP / tick. It is not entirely accurate because it seems
 GP generates at different speeds in non-gathering specs. Scrolling increments / decrements
 GP by 10, and right clicking allows specifying GP in ranges of 100 from 0 to 700.
 
 ## Expansion button
 Left-clicking this button toggles whether the default Windows window borders should be visible.
 Right-clicking also toggles borders, but also makes the window larger when borders are enabled,
 and smaller when borders are disabled.
 
 ## Search bar
 Whatever is typed into the search bar the program will look up on gamerescape. If it finds an entry,
 it will attempt to collect the information on the site and display in tables similar to the ones on that site.
 
 This feature currently supports only _sold by merchant, harvest, mining, logging, and venture_ tables.
 Support for additional tables will be implemented in a later release.
  
 To spare their servers, and speed up searches, the html of the item's  page is cached in ``./data/html_files``.
 When the feature is more mature, this will probably be stored in a more efficient way.


## Future stuff
See ./ideas.md file for planned features. I do not intend to implement anything that could
be perceived as cheating. This is only meant as a way to keep track of timers and information,
especially while logged out. I only started working on this as a pet project to learn TKinter very recently,
so stay tuned for updates.
