import win32api
from tkinter import *
from PIL import Image, ImageFont, ImageDraw, ImageTk


class Outliner:
    def __init__(self):
        self.photo = None
        self.font = win32api.GetWindowsDirectory() + "\\Fonts\\ARIALBD.TTF"
        pointsize = 11
        self.font = ImageFont.truetype(self.font, pointsize)

    def outline(self, text, w, h):
        im = Image.new('RGBA', (w, h), (255, 255, 255, 0))
        font = self.font
        text_x, text_y = font.getsize(text)
        x, y = (w - text_x) / 2, (h - text_y) / 2
        fillcolor = "white"
        shadowcolor = "black"
        draw = ImageDraw.Draw(im)

        # thin border
        # draw.text((x - 1, y), text, font=font, fill=shadowcolor)  #
        # draw.text((x + 1, y), text, font=font, fill=shadowcolor)  #
        # draw.text((x, y - 1), text, font=font, fill=shadowcolor)  #
        # draw.text((x, y + 1), text, font=font, fill=shadowcolor)  #

        # thicker border
        draw.text((x - 1, y - 1), text, font=font, fill=shadowcolor)
        draw.text((x + 1, y - 1), text, font=font, fill=shadowcolor)
        draw.text((x - 1, y + 1), text, font=font, fill=shadowcolor)
        draw.text((x + 1, y + 1), text, font=font, fill=shadowcolor)

        draw.text((x, y), text, font=font, fill=fillcolor)
        self.photo = ImageTk.PhotoImage(im)
        return self.photo
