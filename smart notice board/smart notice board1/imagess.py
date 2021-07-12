''' tk_image_slideshow3.py
create a Tkinter image repeating slide show
tested with Python27/33  by  vegaseat  03dec2013

Taken from https://www.daniweb.com/programming/software-development/code/468841/tkinter-image-slide-show-python

'''

import boto3
from botocore.client import Config
from PIL import Image
from PIL import ImageTk
import tkinter as tk
from itertools import cycle
import io
import glob
import os
import sys

import PIL


class App(tk.Tk):
    '''Tk window/label adjusts to size of image'''
    

    def __init__(self, image_files,delay):
        # the root will be self
        tk.Tk.__init__(self)
        # set x, y position only
        #self.geometry('+{}+{}'.format(x, y))
        self.delay = delay

        # allows repeat cycling through the pictures
        # store as (img_object, img_name) tuple
        self.pictures = cycle((self.photo_image(image), image) for image in image_files)
        self.picture_display = tk.Label(self)
        self.picture_display.pack()

    def show_slides(self):
        '''cycle through the images and show them'''

        # next works with Python26 or higher
        img_object, img_name = next(self.pictures)
        self.picture_display.config(image=img_object)
        # shows the image filename, but could be expanded
        # to show an associated description of the image
        self.title(img_name)
        self.after(self.delay, self.show_slides)


    def photo_image(self, jpg_filename):

        with io.open(jpg_filename, 'rb') as ifh:
            pil_image = Image.open(ifh)
            return ImageTk.PhotoImage(pil_image)

    def run(self):
        self.mainloop()
        run.after(30000000000, lambda: run.destroy())

global img_list
img_list = []
folder = r"/home/pi/smart notice board1/storage/*.jpg"
files = glob.glob(folder)
for files in files:
    img_list.append(files)

app = App(img_list, 3500)
app.show_slides()
app.run()
