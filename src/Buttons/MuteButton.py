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
                                  #bd=2,
                                  padx=0,
                                  highlightthickness=0,
                                  highlightcolor="#37d3ff",
                                  highlightbackground="#37d3ff")

        self.mute_sound()

    def mute_sound(self):
        color = '#7AAD12' if self.et.playing else '#DD0000'
        # color = '#DDDDDD'
        s = 36
        self.mute_button.config(bg=color)  # , image=img, width=s, height=s)#, bd=3)
        self.et.playing = not self.et.playing
