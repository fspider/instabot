from walker import WalkerThread
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
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

        lb_w = 100
        lb_h = 18

        self.btStart = Button(self, text = "Start", command = self.btStart_clicked)
        self.btStop = Button(self, text = "Stop", command = self.btStop_clicked)
        # self.btSetting = Button(self, text = "Setting", command = self.btStop_clicked)
        self.doUnfollowing = IntVar()
        self.ckUnfollowing = Checkbutton(self, text="unfollowing", variable=self.doUnfollowing)
        self.lbCycle = Label(self, text="Cycle (hour)")
        self.enCycle = Entry(self, justify='center')
        self.lbFollows = Label(self, text="Follows/Cycle")
        self.enFollows = Entry(self, justify='center')
        self.lbSearchDelay = Label(self, text="Search Delay")
        self.enSearchDelaySt = Entry(self, justify='center')
        self.lbSearchDelayMd = Label(self, text="~")
        self.enSearchDelayEd = Entry(self, justify='center')

        self.lbFollower = Label(self, text="Follower")
        self.enFollower = Entry(self, justify='center')
        self.lbFollowerList = Label(self, text="Follower list file")
        self.enFollowerList = Entry(self, justify='center')
        self.lbSearchMethod = Label(self, text="Search Method")
        self.cbSearchMethod = ttk.Combobox(self, values=[
                                        "Through",
                                        "Direct" ,
                                        # "Random"
                                        ], justify='center')
        self.lbStatus = Label(self, text="Status is displayed here", anchor=W)

        # Control Buttons
        self.btStart.place(x=20, y = 150, w=bt_w, h=bt_h)
        self.btStop.place(x=20, y = 190, w=bt_w, h=bt_h)
        # self.btSetting.place(x=20, y = 230, w=bt_w, h=bt_h)
        self.ckUnfollowing.place(x=20, y=240, w=bt_w, h=bt_h)
        self.lbCycle.place(x=20, y = 270, w=lb_w, h=lb_h)
        self.enCycle.place(x=20, y = 290, w=lb_w, h=lb_h)
        self.lbFollows.place(x=20, y = 310, w=lb_w, h=lb_h)
        self.enFollows.place(x=20, y = 330, w=lb_w, h=lb_h)
        self.lbSearchDelay.place(x=20, y = 350, w=lb_w, h=lb_h)
        self.enSearchDelaySt.place(x=20, y = 370, w=40, h=lb_h)
        self.lbSearchDelayMd.place(x=65, y = 370, w=10, h=lb_h)
        self.enSearchDelayEd.place(x=80, y = 370, w=40, h=lb_h)

        self.lbFollower.place(x=20, y = 395, w=lb_w, h=lb_h)
        self.enFollower.place(x=20, y = 415, w=lb_w, h=lb_h)
        self.lbFollowerList.place(x=20, y = 435, w=lb_w, h=lb_h)
        self.enFollowerList.place(x=20, y = 455, w=lb_w, h=lb_h)

        self.lbSearchMethod.place(x=20, y = 475, w=lb_w, h=lb_h)
        self.cbSearchMethod.place(x=20, y = 495, w=lb_w, h=lb_h)

        self.enCycle.insert(END, '0.1')
        self.enFollows.insert(END, '2')
        self.enSearchDelaySt.insert(END, '12')
        self.enSearchDelayEd.insert(END, '16')
        self.enFollower.insert(END, 'garyvee')
        self.enFollowerList.insert(END, 'garyvee.txt')
        self.cbSearchMethod.current(1)

        self.console_frame = ttk.Labelframe(self, text="Console")
        self.console_frame.place(x=140, y = 120, w=430, h=420)
        self.lbStatus.place(x=140, y = 570, w=400, h=20)

        logging.basicConfig(
            filename='log.log',
            level=logging.DEBUG, 
            format='%(asctime)s - %(levelname)s - %(message)s') 
        self.logger = logging.getLogger()

        self.console = ConsoleUi(self.console_frame, self.logger)
        self.console.scrolled_text.place(x=4, y = 4, w=420, h=380)

        self.master.protocol('WM_DELETE_WINDOW', self.exit)
        self.master.bind('<Control-q>', self.exit)
        signal.signal(signal.SIGINT, self.exit)

    def btStart_clicked(self):
        MsgBox = tk.messagebox.askquestion('Confirm Page Status', 'Did you check if it is on main page now',
                                           icon='warning')
        if MsgBox == 'yes':
            self.btStart.config(state='disabled')
            self.walkerThread = WalkerThread(self.logger, self)
            self.walkerThread.start()
        else:
            tk.messagebox.showinfo('Confirm Search Page Status', 'Also please check if previous search item was closed')

    def btStop_clicked(self):
        self.walkerThread.stop()
        print(self.walkerThread.is_alive())
        # self.walkerThread.join()
        # self.btStart.config(state = 'normal')
        # print(self.walkerThread.is_alive())

    def setStatus(self, value):
        self.lbStatus['text'] = value

    def exit(self, args=0):
        self.master.destroy()
        sys.exit()

if __name__ == '__main__':
    # print (os.getcwd())
    MainFrm().mainloop()

