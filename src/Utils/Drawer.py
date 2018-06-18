import win32api
from PIL import Image, ImageFont, ImageDraw, ImageTk
from tkinter import Label
import re
import numpy as np


class Outliner:
    def __init__(self):
        self.photo = None  # don't let the GC take you
        self.font = win32api.GetWindowsDirectory() + "\\Fonts\\ARIALBD.TTF"
        pointsize = 11
        self.font = ImageFont.truetype(self.font, pointsize)

    def outline(self, text, w, h, bg=None, bg_fraction=None, center=False):
        if bg is not None:
            bg_fraction = w if bg_fraction is None else bg_fraction
            im = Image.new('RGBA', (w, h), bg)
            arr = np.array(im)
            x, y, z = arr.shape
            bt=3
            arr[bt:-bt, max(bt, int(y * bg_fraction)):-bt, :] = bg#[0, 0, 0, 0]
            im = Image.fromarray(arr)
        else:
            im = Image.new('RGBA', (w, h), (255, 255, 255, 0))

        font = self.font
        text_x, text_y = font.getsize(text)
        if center:
            x = (w - text_x) / 2
        else:
            x = 5
        y = (h - text_y) / 2

        fillcolor = "white"
        shadowcolor = "#222222"
        draw = ImageDraw.Draw(im)

        # thin border
        # draw.text((x - 1, y), text, font=font, fill=shadowcolor)  #
        # draw.text((x + 1, y), text, font=font, fill=shadowcolor)  #
        # draw.text((x, y - 1), text, font=font, fill=shadowcolor)  #
        # draw.text((x, y + 1), text, font=font, fill=shadowcolor)  #

        # thicker border
        # draw.text((x - 1, y - 1), text, font=font, fill=shadowcolor)
        # draw.text((x + 1, y - 1), text, font=font, fill=shadowcolor)
        # draw.text((x - 1, y + 1), text, font=font, fill=shadowcolor)
        # draw.text((x + 1, y + 1), text, font=font, fill=shadowcolor)
        #
        draw.text((x, y), text, font=font, fill=fillcolor)

        self.photo = ImageTk.PhotoImage(im)
        return self.photo
