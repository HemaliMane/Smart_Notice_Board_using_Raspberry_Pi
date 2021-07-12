import tkinter
from PIL import Image
from PIL import ImageTk
import tkinter as tk
from itertools import cycle
import io
import glob
import os
import sys

import PIL


download = tkinter.Tk()

global img_list
img_list = []

def image_123(tkinter.Tk):  
    folder = r"/home/pi/smart notice board1/storage/*.jpg"
    files = glob.glob(folder)

    #for files in files: 
    img_list.append(files)


            
    self.x = 800
    self.y = 800
    self.delay = 5200

    self.pictures = cycle((self.photo_image(image), image) for image in img_list)

    self.picture_display.destroy()

    self.picture_display = Label(self)
    self.picture_display.pack(side=TOP, anchor=E)
    self.show_slides()
    self.after(60000, self.image123)
    print('image 123')

def show_slides(self):
    '''cycle through the images and show them'''

    img_object, img_name = next(self.pictures)
    self.picture_display.config(image=img_object)
    #time.sleep(1)
    self.after(self.delay, self.show_slides)
        



def photo_image(self, jpg_filename):

    with io.open(jpg_filename, 'rb') as ifh:
        pil_image = Image.open(ifh)
        return ImageTk.PhotoImage(pil_image)
        
download.mainloop()
