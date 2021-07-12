
# requirements
# requests, feedparser, traceback, Pillow

import sys
from Tkinter import *
import locale
import threading
import time
import calendar
import requests
import json
import traceback
import feedparser
import datetime
import os
import socket
import ssl
import unicodedata
import sqlite3
global d
import boto3
from botocore.client import Config
from PIL import Image
from PIL import ImageTk
from itertools import cycle
import io
import sys
import glob
import PIL
from PIL import Image, ImageTk
from contextlib import contextmanager
from firebase import firebase
from google.cloud import storage
from firebase import firebase 
from oauth2client.client import GoogleCredentials
from google.cloud.storage import blob


LOCALE_LOCK = threading.Lock()

ui_locale = '' # e.g. 'fr_FR' fro French, '' as default
time_format = 12 # 12 or 24
date_format = "%b %d, %Y" # check python doc for strftime() for options
now = datetime.datetime.now()
month = int(now.strftime("%m"))
year = int(now.strftime("%y"))
calendarEventContainer = calendar.month(year, month)
news_country_code = 'in'
weather_api_token = 'b06c2afad52bbdd94d3f2dd0712766eb' # create account at https://darksky.net/dev/
weather_lang = 'en' # see https://darksky.net/dev/docs/forecast for full list of language parameters values
weather_unit = 'si' # see https://darksky.net/dev/docs/forecast for full list of unit parameters values
latitude = 19.136326 # Set this if IP location lookup does not work for you (must be a string)
longitude = 72.827660 # Set this if IP location lookup does not work for you (must be a string)
xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 14
#firebase = firebase.FirebaseApplication('https://notice-64ce2.firebaseio.com/',None)
storage_client = storage.Client.from_service_account_json('Notice-818fa150ed19.json')
firebase = firebase.FirebaseApplication('https://notice-64ce2.firebaseio.com/', None)
bucket = storage_client.get_bucket("notice-64ce2.appspot.com")
        


@contextmanager
def setlocale(name): #thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

# maps open weather icons to
# icon reading is not impacted by the 'lang' parameter
icon_lookup = {
    'clear-day': "assets/Sun.png",  # clear sky day
    'wind': "assets/Wind.png",   #wind
    'cloudy': "assets/Cloud.png",  # cloudy day
    'partly-cloudy-day': "assets/PartlySunny.png",  # partly cloudy day
    'rain': "assets/Rain.png",  # rain day
    'snow': "assets/Snow.png",  # snow day
    'snow-thin': "assets/Snow.png",  # sleet day
    'fog': "assets/Haze.png",  # fog day
    'clear-night': "assets/Moon.png",  # clear sky night
    'partly-cloudy-night': "assets/PartlyMoon.png",  # scattered clouds night
    'thunderstorm': "assets/Storm.png",  # thunderstorm
    'tornado': "assests/Tornado.png",    # tornado
    'hail': "assests/Hail.png"  # hail
}

'''
class Clock(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        
        # initialize time label
        self.time1 = ''
        self.timeLbl = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.timeLbl.pack(side=TOP, anchor=E)
        
        # initialize calender label
        self.calendarEventContainer = Frame(self, bg='black')
        self.calendarEventContainerLb1 = Label(self, text=calendarEventContainer, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.calendarEventContainerLb1.pack(side=TOP, anchor=E)
        self.get_events()
        # initialize day of week
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dayOWLbl.pack(side=TOP, anchor=E)
        # initialize date label
        self.date1 = ''
        self.dateLbl = Label(self, text=self.date1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dateLbl.pack(side=TOP, anchor=E)
        self.tick()


    def get_events(self):
        
        #TODO: implement this method
        #reference https://developers.google.com/google-apps/calendar/quickstart/python

        try:
            if calendarEventContainer == calendar.month(year, month):
                self.calendarEventContainer.pack(side=RIGHT, anchor=E)
            
                
        except Exception as e:
            traceback.print_exc()
            print ("Error: %s. Cannot get calendar.") % e

    def tick(self):
        with setlocale(ui_locale):
            if time_format == 12:
                time2 = time.strftime('%I:%M %p') #hour in 12h format
            else:
                time2 = time.strftime('%H:%M') #hour in 24h format

            day_of_week2 = time.strftime('%A')
            date2 = time.strftime(date_format)
            # if time string has changed, update it
            if time2 != self.time1:
                self.time1 = time2
                self.timeLbl.config(text=time2)
            if day_of_week2 != self.day_of_week1:
                self.day_of_week1 = day_of_week2
                self.dayOWLbl.config(text=day_of_week2)
            if date2 != self.date1:
                self.date1 = date2
                self.dateLbl.config(text=date2)
            # calls itself every 200 milliseconds
            # to update the time display as needed
            # could use >200 ms, but display gets jerky
            self.timeLbl.after(200, self.tick)

'''     

class Weather(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.temperature = ''
        self.forecast = ''
        self.location = ''
        self.currently = ''
        self.icon = ''
        self.degreeFrm = Frame(self, bg="black")
        self.degreeFrm.pack(side=TOP, anchor=W)
        self.temperatureLbl = Label(self.degreeFrm, font=('Helvetica', small_text_size),fg="white", bg="black")
        self.temperatureLbl.pack(side=LEFT, anchor=N)
        self.iconLbl = Label(self.degreeFrm, bg="black")
        self.iconLbl.pack(side=LEFT, anchor=N, padx=20)
        self.currentlyLbl = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.currentlyLbl.pack(side=TOP, anchor=W)
        self.forecastLbl = Label(self, font=('Helvetica', small_text_size) ,wraplength =300, fg="white", bg="black")
        self.forecastLbl.pack(side=TOP, anchor=W)
        self.locationLbl = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.locationLbl.pack(side=TOP, anchor=W)

        self.get_weather()

        
        # initialize time label
        self.time1 = ''
        self.timeLbl = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.timeLbl.pack(side=TOP, anchor=E)
        
        # initialize calender label
        self.calendarEventContainer = Frame(self, bg='black')
        self.calendarEventContainerLb1 = Label(self, text=calendarEventContainer, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.calendarEventContainerLb1.pack(side=TOP, anchor=E)
        self.get_events()
        # initialize day of week
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dayOWLbl.pack(side=TOP, anchor=E)
        # initialize date label
        self.date1 = ''
        self.dateLbl = Label(self, text=self.date1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dateLbl.pack(side=TOP, anchor=E)

        
        self.tick()


    def get_ip(self):
        try:
            ip_url = "http://jsonip.com/"
            req = requests.get(ip_url)
            ip_json = json.loads(req.text)
            return ip_json['ip']
        except Exception as e:
            traceback.print_exc()
            return ("Error: %s. Cannot get ip.") % e

    def get_weather(self):
        try:

            if latitude is None and longitude is None:
                # get location
                location_req_url = "http://freegeoip.net/json/%s" % self.get_ip()
                r = requests.get(location_req_url)
                location_obj = json.loads(r.text)

                lat = location_obj['latitude']
                lon = location_obj['longitude']

                location2 = "%s, %s" % (location_obj['city'], location_obj['region_code'])

                # get weather
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, lat,lon,weather_lang,weather_unit)
            else:
                location2 = ""
                # get weather
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, latitude, longitude, weather_lang, weather_unit)

            r = requests.get(weather_req_url)
            weather_obj = json.loads(r.text)

            degree_sign= u'\N{DEGREE SIGN}'
            temperature2 = "%s%s" % (str(int(weather_obj["currently"]["temperature"])), degree_sign)
            currently2 = weather_obj["currently"]["summary"]
            forecast2 = weather_obj["hourly"]["summary"]

            icon_id = weather_obj["currently"]["icon"]
            icon2 = None

            if icon_id in icon_lookup:
                icon2 = icon_lookup[icon_id]

            if icon2 is not None:
                if self.icon != icon2:
                    self.icon = icon2
                    image = Image.open(icon2)
                    image = image.resize((100, 100), Image.ANTIALIAS)
                    image = image.convert('RGB')
                    photo = ImageTk.PhotoImage(image)

                    self.iconLbl.config(image=photo)
                    self.iconLbl.image = photo
            else:
                # remove image
                self.iconLbl.config(image='')

            if self.currently != currently2:
                self.currently = currently2
                self.currentlyLbl.config(text=currently2)
            if self.forecast != forecast2:
                self.forecast = forecast2
                self.forecastLbl.config(text=forecast2)
            if self.temperature != temperature2:
                self.temperature = temperature2
                self.temperatureLbl.config(text=temperature2)
            if self.location != location2:
                if location2 == ", ":
                    self.location = "Cannot Pinpoint Location"
                    self.locationLbl.config(text="Cannot Pinpoint Location")
                else:
                    self.location = location2
                    self.locationLbl.config(text=location2)
        except Exception as e:
            traceback.print_exc()
            print ("Error: %s. Cannot get weather.") % e

        self.after(1000000, self.get_weather)
        print('weather')

    @staticmethod
    def convert_kelvin_to_fahrenheit(kelvin_temp):
        return 1.8 * (kelvin_temp - 273) + 32

        

        

    def get_events(self):
        
        #TODO: implement this method
        #reference https://developers.google.com/google-apps/calendar/quickstart/python

        try:
            if calendarEventContainer == calendar.month(year, month):
                self.calendarEventContainer.pack(side=RIGHT, anchor=E)
            
                
        except Exception as e:
            traceback.print_exc()
            print ("Error: %s. Cannot get calendar.") % e

    def tick(self):
        with setlocale(ui_locale):
            if time_format == 12:
                time2 = time.strftime('%I:%M %p') #hour in 12h format
            else:
                time2 = time.strftime('%H:%M') #hour in 24h format

            day_of_week2 = time.strftime('%A')
            date2 = time.strftime(date_format)
            # if time string has changed, update it
            if time2 != self.time1:
                self.time1 = time2
                self.timeLbl.config(text=time2)
            if day_of_week2 != self.day_of_week1:
                self.day_of_week1 = day_of_week2
                self.dayOWLbl.config(text=day_of_week2)
            if date2 != self.date1:
                self.date1 = date2
                self.dateLbl.config(text=date2)
            # calls itself every 200 milliseconds
            # to update the time display as needed
            # could use >200 ms, but display gets jerky
            self.timeLbl.after(200, self.tick)
            


class News(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.title = 'News' # 'News' is more internationally generic
        self.newsLbl = Label(self, text=self.title, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.newsLbl.pack(side=TOP, anchor=W)
        self.headlinesContainer = Frame(self, bg="black")
        self.headlinesContainer.pack(side=TOP)
        self.get_headlines()

    def get_headlines(self):
        try:
            # remove all children
            for widget in self.headlinesContainer.winfo_children():
                widget.destroy()
            if news_country_code == 'in':
                headlines_url = "https://news.google.com/news?ned=in&output=rss"
            else:
                headlines_url = "https://news.google.com/news?ned=%s&output=rss" % news_country_code

            feed = feedparser.parse(headlines_url)

            for post in feed.entries[1:6]:
                headline = NewsHeadline(self.headlinesContainer, post.title)
                headline.pack(side=TOP, anchor=W)
        except Exception as e:
            traceback.print_exc()
            print ("Error: %s. Cannot get news.") % e

        self.headlinesContainer.after(1000000, self.get_headlines)
        
        print('news')


class NewsHeadline(Frame):
    def __init__(self, parent, event_name=""):
        Frame.__init__(self, parent, bg='black')

        image = Image.open("assets/Newspaper.png")
        image = image.resize((25, 25), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)

        self.iconLbl = Label(self, bg='black', image=photo)
        self.iconLbl.image = photo
        self.iconLbl.pack(side=LEFT, anchor=N)

        self.eventName = event_name
        self.eventNameLbl = Label(self, text=self.eventName, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.eventNameLbl.pack(side=LEFT, anchor=N)



class notice(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.config(bg='black')
        self.title = 'Notice'
        self.noticeLbl = Label(self, text = self.title, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.noticeLbl.pack(side=TOP ,anchor=W )

        self.title2 = ' No Notice Found' 
        self.noticeLb2 = Label(self, text = self.title2, font=('Helvetica', small_text_size),wraplength =400, fg="white", bg="black")
        self.noticeLb2.pack(side=TOP ,anchor=W )
        print(self.title2)

        self.get_notice()

        
    def get_notice(self):

        result = firebase.get('/message', None)
        print("result")
        '''
        db = sqlite3.connect('test.db;')
        cursor = db.cursor()
        cursor.execute("create table if not exists noticee(id INTEGER PRIMARY KEY, data TEXT)") 



        cursor.execute("insert into noticee(data) values(?)", (result,))
        db.commit()
        cursor.execute("select * from noticee ORDER BY id DESC LIMIT 1")
        user = cursor.fetchone()
        print("db")
        print(user[1])
        self.d = StringVar()
        db = sqlite3.connect('test.db;')
        cursor = db.cursor()
        cursor.execute("select * from noticee ORDER BY id DESC LIMIT 1")
        user = cursor.fetchone()
        self.d = user[1]


        
        for key, value in result.items():
            message = value
            print (message)
        
            for key , value in d.items():
                message = value
                print(message)
        '''
        self.noticeLb2.destroy()
        print(result)
        self.noticeLb2 = Label(self, text = result, font=('Helvetica', small_text_size),wraplength =400, fg="white", bg="black")
        self.noticeLb2.pack(side=TOP , anchor=S)
        self.noticeLb2.after(2400, self.get_notice)
        #self.after(2500, self.get_notice)

                
      
        
    

'''
                
        #self.noticeContainer.destroy()
        self.d = StringVar()
        db = sqlite3.connect('test.db;')
        cursor = db.cursor()
        cursor.execute("select * from noticee ORDER BY id DESC LIMIT 1")
        user = cursor.fetchone()
        #print(user[1])
        self.d = user[1]
        #print(self.d)
        self.noticeLb2.destroy()
        self.noticeLb2 = Label(self, text = self.d, font=('Helvetica', small_text_size),wraplength =400, fg="white", bg="black")
        self.noticeLb2.pack(side=TOP , anchor=S)
        cursor.close()
        self.after(60000, self.get_notice)
        print('notice')
         
'''        

        #self.get_notice()
        #self.notice_container = Label(self, text=self.d, font=('Helvetica', medium_text_size), fg="white", bg="black")
       # self.notice_container.pack(side=TOP, anchor=W)

     #def get_notice(self):
      #  for widget in self.notice_container.winfo_children():
      #      widget.destroy()
            
        #self.d = StringVar()
       # db = sqlite3.connect('test.db;')
        #cursor = db.cursor()
        #cursor.execute("select * from noticee ORDER BY id DESC LIMIT 1")
        #user = cursor.fetchone()
        #print(user[1])    
        #self.d = user[1]
        #print(self.d)
        #self.notice_display =  Label(self, textvariable = self.d, bg="black", fg="white")
        #self.notice_display.place(x=50, y=50, width=30, height=25)
        #self.after(600000, self.get_notice)


class download(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.config(bg='black')

        global img_list
        img_list = []

        
        self.name = 'no img'
        self.picture_display = Label(self, text=self.name, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.picture_display.pack(side=TOP, anchor=E)

        self.downloading()
        self.image123()   
        
    def downloading(self):
        
        blobs = list(bucket.list_blobs())
        for blob in blobs:
            folder ="/home/pi/smart notice board1/storage/" +blob.name
            if not os.path.exists(folder):
                blob.download_to_filename(folder)
                print("done")
                size = 300,300
                img2 = PIL.Image.open(folder)
                img2.thumbnail(size,PIL.Image.ANTIALIAS)
                img2.save(folder,'JPEG')

            self.after(30000, self.downloading)
         
    def image123(self):
        
        folder = r"/home/pi/smart notice board1/storage/*"
        files = glob.glob(folder)
        for file in files: 
            img_list.append(file)


        
        self.x = 800
        self.y = 800
        self.delay = 5200

        self.pictures = cycle((self.photo_image(image), image) for image in img_list)

        self.picture_display.destroy()

        self.picture_display = Label(self)
        self.picture_display.pack(side=TOP, anchor=E)
        self.show_slides()
        self.picture_display.after(30000, self.image123)
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
        
class FullscreenWindow:

    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='black')
        
        self.topFrame = Frame(self.tk, background = 'black')
        self.bottomFrame = Frame(self.tk, background = 'black')
        self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
        
        self.state = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        # clock ,time,calender
        #self.clock = Clock(self.topFrame)
        #self.clock.pack(side=RIGHT, anchor=E, padx=50, pady=40)
        # weather
        self.weather = Weather(self.topFrame)
        self.weather.pack(side=LEFT, anchor=N, padx=70, pady=5)
        # news
        self.news = News(self.bottomFrame)
        self.news.pack(side=LEFT, anchor=S, padx=90, pady=20)
        #notice
        self.notice = notice(self.topFrame)
        self.notice.pack(side=LEFT ,anchor=N , padx=60, pady=60)
        #image
        self.download = download(self.topFrame)
        self.download.pack(side=RIGHT ,anchor=E , padx=50, pady=40)
        

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

if __name__ == '__main__':

    w = FullscreenWindow()
    w.tk.mainloop()
