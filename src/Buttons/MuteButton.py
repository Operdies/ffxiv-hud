from tkinter import Button
from PIL import Image, ImageTk


class MuteButton:
    def __init__(self, master, et):
        self.et = et
        self.button = Button
        self.mute_icon = ImageTk.PhotoImage(Image.open('icons/mute.png'))
        self.unmute_icon = ImageTk.PhotoImage(Image.open('icons/unmute.png'))

        self.mute_button = Button(master,
                                  fg='#000000',
                                  bg='#000000',
                                  image=self.mute_icon,
                                  # bg='#9ACD32',
                                  command=self.mute_sound,
                                  width=3,
                                  borderwidth=0,
                                  highlightthickness=0)

        self.mute_sound()

    def mute_sound(self):
        # color = '#7AAD12' if self.et.playing else '#DD0000'
        photo = self.mute_icon if self.et.playing else self.unmute_icon
        # self.mute_button.config(bg=color)
        self.mute_button.config(image=self.mute_icon if self.et.playing else self.unmute_icon)
        self.et.playing = not self.et.playing
