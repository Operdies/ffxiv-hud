from tkinter import Button


class MuteButton:
    def __init__(self, master, et):
        self.et = et
        self.button = Button
        self.mute_button = Button(master,
                                  fg='#000000',
                                  bg='#9ACD32',
                                  command=self.mute_sound,
                                  width=3,
                                  borderwidth=0,
                                  highlightthickness=0)

        self.mute_sound()

    def mute_sound(self):
        color = '#7AAD12' if self.et.playing else '#DD0000'
        self.mute_button.config(bg=color)
        self.et.playing = not self.et.playing
