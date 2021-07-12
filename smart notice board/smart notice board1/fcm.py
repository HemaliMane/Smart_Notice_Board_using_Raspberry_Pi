from Tkinter import *
from firebase import firebase
import json
import pyrebase




top = Tk()

d={}
firebase = firebase.FirebaseApplication('https://notice-64ce2.firebaseio.com/', None)



def publish():
    notice = E1.get()
    print(notice)

    #json = '{'"Message"': +notice }'
    #result = firebase.post("/notice-64ce2/notice/", json )
    result = firebase.patch('/', {'message': notice })


    
    


def upload():
    config = {
      "apiKey": "AIzaSyAoQvyYfduGeNmlCOh1VWiAw_5mG5tJPss",
      "authDomain": "notice-64ce2.firebaseapp.com",
      "databaseURL": 'https://notice-64ce2/storage.firebaseio.com/',
      "storageBucket": "notice-64ce2.appspot.com"
    }
    firebase = pyrebase.initialize_app(config)
    
    image = E2.get()
    #filename = "D:\python projects\smart_notice_board\aaaa.jpg"
    file1 = open(image, 'rb')


    storage = firebase.storage()
    storage.child(image).put(file1)
    print('done')
        
    
L1 = Label(top, text = 'Enter the notice:')
L1.grid(row=1,column=1)
E1 = Entry(top, bd =5)
E1.grid(row=1, column=2)

b1 = Button(top, text='Publish', command=publish)
b1.grid(row=2, column=1)


L2 = Label(top, text ='Upload Image')
L2.grid(row = 3 ,column = 1)
E2 = Entry(top,bd=5)
E2.grid(row=3, column=2)

b2 = Button(top, text='Upload',command =upload)
b2.grid(row=4, column=1)


top.mainloop()
