from walker import Walker
import tkinter as tk
from tkinter import *
from tkinter import ttk
import time
from PIL import Image, ImageTk
import tkinter.scrolledtext as ScrolledText
import logging
import threading

class TextHandler(logging.Handler):
    """This class allows you to log to a Tkinter Text or ScrolledText widget"""
    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        msg = self.format(record)
        # print(msg)
        def append():
            self.text.configure(state='normal')
            self.text.insert(tk.END, msg + '\n')
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(tk.END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)

class MainFrm(Frame):
    def __init__(self):

        tk.Frame.__init__(self)
        self.pack(fill=BOTH, expand=1)
        self.master.title("InstaBot")
        self.master.geometry("600x600+10+20")

        load = Image.open('banner.png')
        render = ImageTk.PhotoImage(load)
        imgBanner = Label(self, image=render)
        imgBanner.image = render
        imgBanner.place(x=0, y=0, w=600, h=100)

        bt_w = 120
        bt_h =30

        self.btStart = Button(self, text = "Start", command = self.btStart_clicked)
        self.btStop = Button(self, text = "Stop", command = self.btStop_clicked)
        self.btSetting = Button(self, text = "Setting", command = self.btStop_clicked)

        # Control Buttons
        self.btStart.place(x=20, y = 150, w=bt_w, h=bt_h)
        self.btStop.place(x=20, y = 190, w=bt_w, h=bt_h)
        self.btSetting.place(x=20, y = 230, w=bt_w, h=bt_h)

        # List Name
        self.lbFollow = Label(self, text='New Followings')
        self.lbFollow.place(x=150, y = 120, w=bt_w, h=bt_h)

        # List Box
        # self.liFollow = Listbox(self)
        # self.liFollow.place(x=160, y = 150, w=300, h=420)

        self.log = ScrolledText.ScrolledText(self, state='disabled')
        self.log.configure(font='TkFixedFont')
        self.log.place(x=160, y = 150, w=300, h=420)

        self.text_handler = TextHandler(self.log)

        logging.basicConfig(filename='log.log',
            level=logging.DEBUG, 
            format='%(asctime)s - %(levelname)s - %(message)s') 

        self.logger = logging.getLogger()
        self.logger.addHandler(self.text_handler)
        self.walker = Walker(self.logger)

    def btStart_clicked(self):
        self.logger.info('InstaBot Started!')
        self.walker.start()
        self.logger.info('InstaBot Ended!')
    
    def btStop_clicked(self):
        pass


if __name__ == '__main__':
    MainFrm().mainloop()

