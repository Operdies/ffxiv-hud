import win32api
from tkinter import *
from PIL import Image, ImageFont, ImageDraw, ImageTk


class Outliner:
    def __init__(self):
        self.photo = None

    def outline(self, text, w, h):
        im = Image.new('RGBA', (w, h), (255, 255, 255, 0))
        pointsize = 11
        font = win32api.GetWindowsDirectory() + "\\Fonts\\ARIALBD.TTF"
        font = ImageFont.truetype(font, pointsize)
        text_x, text_y = font.getsize(text)
        x, y = (w - text_x) / 2, (h - text_y) / 2
        fillcolor = "white"
        shadowcolor = "black"
        draw = ImageDraw.Draw(im)
        # thin border

        #draw.text((x - 1, y), text, font=font, fill=shadowcolor)  #
        #draw.text((x + 1, y), text, font=font, fill=shadowcolor)  #
        #draw.text((x, y - 1), text, font=font, fill=shadowcolor)  #
        #draw.text((x, y + 1), text, font=font, fill=shadowcolor)  #

        # thicker border
        draw.text((x-1, y-1), text, font=font, fill=shadowcolor)
        draw.text((x+1, y-1), text, font=font, fill=shadowcolor)
        draw.text((x-1, y+1), text, font=font, fill=shadowcolor)
        draw.text((x+1, y+1), text, font=font, fill=shadowcolor)

        # now draw the text over it
        draw.text((x, y), text, font=font, fill=fillcolor)
        self.photo = ImageTk.PhotoImage(im)
        return self.photo


if __name__ == '__main__':
    root = Tk()
    w = Canvas(root, width=400, height=100)
    # im = im.tobitmap()
    # im = Image.open(fname2)

    # w.create_image((100, 100), image=PhotoImage(file=fname2))
    # w.pack()
    # photo = PhotoImage(file=fname2)

    # photo = PhotoImage(Image.open(fname2))
    photo = ImageTk.PhotoImage(im)
    frame = Label(root, text="Hello there", image=photo)
    frame.pack()
    canvas = Canvas(root, width=999, height=999)

    while True:
        root.update_idletasks()
        root.update()
