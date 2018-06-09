## tabs:
* botanist gathering cycle with option to add or remove entry
   * x untracks entry and moves it to separate list
   * x in separate list removes permantently (with warning?)
   * v in separate list restores
   * cycle list could have x repeating entries if there aren't enough in a single day
   * cycle could expand and shrink according to size of window
   * '+' button to add new entries

* button above each element to toggle hide / show in minimal view

## data management:
* implement a database instead of pickling / unpickling dictionaries
* allow user to manage simple databases


## graphics:
* support for adding graphics to buttons - design own graphics in photoshop

## QOL / features:
* support for specifying venture duration
* support for specifying when the button should highlight / alert sound should play
* enable changing default and highlight color
* enable changing color of other buttons as well
* support for adding alerts for ventures
* first-time setup instead of using my own settings lol
* up-arrow button to expand frame to window
* support for specifying the format string on botanist bar
* quick notes
* make mute state persistent
* allow resizing of minimized version (perhaps make a slim top-bar that is draggable and has resizing hooks)
* option to lock movement / resizing separately
* lock-button could drag the window


## Project-stuff:
* implement different button types as Widgets instead of just exposing tkinter elements
* make everything neater and less shitty
* Setup continous integration and change workflow to add new features through feature branches 
* more clever implementation of mute than changing "playing" flag perhaps
* organise data folder
