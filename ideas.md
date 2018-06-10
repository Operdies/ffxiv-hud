## tabs:
* botanist gathering cycle with option to add or remove entry
   * x untracks entry and moves it to separate list
   * x in separate list removes permantently (with warning?)
   * check symbol in separate list restores
   * cycle list could have x repeating entries if there aren't enough in a single day
   * cycle could expand and shrink according to size of window
   * '+' button to add new entries


* button above each element to toggle hide / show in minimal view

## data management:
* implement a database instead of pickling / unpickling dictionaries
* allow user to manage simple databases
* Optimistically add local text-based database of items and mobs

## graphics:
* support for adding graphics to buttons - design own graphics in photoshop
* rework mute button so mute / unmute are more uniform. Maybe just steal windows icon
* enable changing default and highlight color
* enable changing color of other buttons as well

## QOL / features:
* support for specifying venture duration 
(context menu?)
* support for specifying when the button should highlight / alert sound should play
* support for adding alerts for ventures 
(add more generic stock sound effects)
* first-time setup instead of using my own settings lol 
(default values in filedict?)
* up-arrow button to expand frame to window
* support for specifying the format string on botanist bar
* quick notes (tab in full-size window with support to add rows from database?)
* allow resizing of minimized version (perhaps make a slim top-bar that is draggable and has resizing hooks)
* option to lock movement / resizing separately
* lock-button could drag the window
* support for airship stuff when I get to build those myself


## Project-stuff:
* implement different button types as Widgets instead of just exposing tkinter elements
* make everything neater and less shitty
* create unittests
* Setup continous integration and change workflow to add new features through feature branches 
* more clever implementation of mute than changing "playing" flag perhaps 
(current solution may be fine if we add a mutex lock)
