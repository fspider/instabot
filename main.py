from walker import WalkerThread
import tkinter as tk
from tkinter import *
from tkinter import ttk
import time
from PIL import Image, ImageTk
import logging
from threading import Thread
from logger import ConsoleUi
import signal

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

        bt_w = 100
        bt_h =30

        self.btStart = Button(self, text = "Start", command = self.btStart_clicked)
        self.btStop = Button(self, text = "Stop", command = self.btStop_clicked)
        self.btSetting = Button(self, text = "Setting", command = self.btStop_clicked)

        # Control Buttons
        self.btStart.place(x=20, y = 150, w=bt_w, h=bt_h)
        self.btStop.place(x=20, y = 190, w=bt_w, h=bt_h)
        self.btSetting.place(x=20, y = 230, w=bt_w, h=bt_h)

        self.console_frame = ttk.Labelframe(self, text="Console")
        self.console_frame.place(x=140, y = 120, w=430, h=420)

        logging.basicConfig(
            filename='log.log',
            level=logging.DEBUG, 
            format='%(asctime)s - %(levelname)s - %(message)s') 
        self.logger = logging.getLogger()

        self.console = ConsoleUi(self.console_frame, self.logger)
        self.console.scrolled_text.place(x=4, y = 4, w=420, h=380)

        self.walkerThread = WalkerThread(self.logger)

        self.master.protocol('WM_DELETE_WINDOW', self.quit)
        self.master.bind('<Control-q>', self.quit)
        signal.signal(signal.SIGINT, self.quit)

    def btStart_clicked(self):
        self.btStart.config(state='disabled')
        self.logger.info('InstaBot Started!')
        self.walkerThread.start()
    
    def btStop_clicked(self):
        self.walkerThread.stop()
        self.btStart.config(state = 'normal')

    def exit(self):
        self.master.destroy()

if __name__ == '__main__':
    MainFrm().mainloop()

