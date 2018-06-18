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
* associate records with patch in case of changes

## graphics:
* support for adding own graphics to buttons - design own graphics in photoshop
* enable changing default and highlight color
* enable changing color of other buttons as well

## QOL:
* specify when the button should highlight / alert sound should play
* first-time setup instead of using my own settings lol 
(default values in filedict?)

## features:
* add alerts for ventures 
(add more generic stock sound effects)
* GP bar / time to full - check whether 6gp per tick is unlocked
* support for airship stuff when I get to build those myself
* macro builder / parser + help with crafting rotation
* allow resizing of minimized version (perhaps make a slim top-bar that is draggable and has resizing hooks)
* quick notes (tab in full-size window with support to add rows from database?)
* specify the format string on botanist bar
* cactpot solver like https://ff14-cactpot.wotax.net/


## Project-stuff:
* implement different button types as Widgets instead of just exposing tkinter elements
* make everything neater and less shitty
* create unittests
* Setup continous integration and change workflow to add new features through feature branches 

