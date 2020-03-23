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
from configparser import ConfigParser

class MainFrm(Frame):
    def __init__(self):

        tk.Frame.__init__(self)
        self.pack(fill=BOTH, expand=1)
        self.master.title("InstaBot")
        self.master.geometry("600x600+50+100")

        load = Image.open('banner.png')
        render = ImageTk.PhotoImage(load)
        imgBanner = Label(self, image=render)
        imgBanner.image = render
        imgBanner.place(x=0, y=0, w=600, h=100)
        self.position = None
        self.config_filename = 'config.ini'
        self.config = ConfigParser()
        self.config.read(self.config_filename)

        bt_w = 100
        bt_h =30

        lb_w = 100
        lb_h = 18

        self.btStart = Button(self, text = "Start", command = self.btStart_clicked)
        self.btStop = Button(self, text = "Stop", command = self.btStop_clicked)
        self.btSetting = Button(self, text = "Region", command = self.btSetting_clicked)

        self.doUnfollowing = IntVar()
        self.ckUnfollowing = Checkbutton(self, text="unfollowing", variable=self.doUnfollowing, anchor = 'w')
        self.doLikes = IntVar()
        self.ckLikes = Checkbutton(self, text="Likes", variable=self.doLikes, anchor = 'w')

        self.lbCycle = Label(self, text="Cycle (hour)")
        self.enCycleSt = Entry(self, justify='center')
        self.lbCycleMd = Label(self, text="~")
        self.enCycleEd = Entry(self, justify='center')

        self.lbFollows = Label(self, text="Follows/Cycle")
        self.enFollowsSt = Entry(self, justify='center')
        self.lbFollowsMd = Label(self, text="~")
        self.enFollowsEd = Entry(self, justify='center')

        self.lbSearchDelay = Label(self, text="Search Delay")
        self.enSearchDelaySt = Entry(self, justify='center')
        self.lbSearchDelayMd = Label(self, text="~")
        self.enSearchDelayEd = Entry(self, justify='center')

        self.lbLikesDelay = Label(self, text="Likes Delay")
        self.enLikesDelaySt = Entry(self, justify='center')
        self.lbLikesDelayMd = Label(self, text="~")
        self.enLikesDelayEd = Entry(self, justify='center')

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

        self.btFollowPause = Button(self, text = "Pause", command = self.bt_follow_pause_clicked)
        self.btFollowResume = Button(self, text = "Resume", command = self.bt_follow_resume_clicked)

        # Control Buttons
        self.btStart.place(x=20, y = 120, w=bt_w, h=bt_h)
        self.btStop.place(x=20, y = 160, w=bt_w, h=bt_h)
        self.btSetting.place(x=20, y = 200, w=bt_w, h=bt_h)
        self.ckUnfollowing.place(x=20, y=230, w=bt_w, h=bt_h)
        self.ckLikes.place(x=20, y=250, w=bt_w, h=bt_h)

        self.btFollowPause.place(x=20, y=555, w=50, h=bt_h)
        self.btFollowResume.place(x=70, y=555, w=50, h=bt_h)

        self.lbCycle.place(x=20, y = 270, w=lb_w, h=lb_h)
        self.enCycleSt.place(x=20, y = 290, w=40, h=lb_h)
        self.lbCycleMd.place(x=65, y = 290, w=10, h=lb_h)
        self.enCycleEd.place(x=80, y = 290, w=40, h=lb_h)

        self.lbFollows.place(x=20, y = 310, w=lb_w, h=lb_h)
        self.enFollowsSt.place(x=20, y = 330, w=40, h=lb_h)
        self.lbFollowsMd.place(x=65, y = 330, w=10, h=lb_h)
        self.enFollowsEd.place(x=80, y = 330, w=40, h=lb_h)

        self.lbSearchDelay.place(x=20, y = 350, w=lb_w, h=lb_h)
        self.enSearchDelaySt.place(x=20, y = 370, w=40, h=lb_h)
        self.lbSearchDelayMd.place(x=65, y = 370, w=10, h=lb_h)
        self.enSearchDelayEd.place(x=80, y = 370, w=40, h=lb_h)

        self.lbLikesDelay.place(x=20, y = 390, w=lb_w, h=lb_h)
        self.enLikesDelaySt.place(x=20, y = 410, w=40, h=lb_h)
        self.lbLikesDelayMd.place(x=65, y = 410, w=10, h=lb_h)
        self.enLikesDelayEd.place(x=80, y = 410, w=40, h=lb_h)

        self.lbFollower.place(x=20, y = 435, w=lb_w, h=lb_h)
        self.enFollower.place(x=20, y = 455, w=lb_w, h=lb_h)
        self.lbFollowerList.place(x=20, y = 475, w=lb_w, h=lb_h)
        self.enFollowerList.place(x=20, y = 495, w=lb_w, h=lb_h)

        self.lbSearchMethod.place(x=20, y = 515, w=lb_w, h=lb_h)
        self.cbSearchMethod.place(x=20, y = 535, w=lb_w, h=lb_h)

        self.enCycleSt.insert(END, '0.1')
        self.enCycleEd.insert(END, '0.2')
        self.enFollowsSt.insert(END, '2')
        self.enFollowsEd.insert(END, '5')
        self.enSearchDelaySt.insert(END, '12')
        self.enSearchDelayEd.insert(END, '16')
        self.enLikesDelaySt.insert(END, '10')
        self.enLikesDelayEd.insert(END, '20')
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
            self.walkerThread = WalkerThread(self.logger, self)
            self.btStart.config(state='disabled')
            self.walkerThread.start()
        else:
            tk.messagebox.showinfo('Confirm Search Page Status', 'Also please check if previous search item was closed')

    def btStop_clicked(self):
        self.walkerThread.stop()
        print(self.walkerThread.is_alive())
        # self.walkerThread.join()
        # self.btStart.config(state = 'normal')
        # print(self.walkerThread.is_alive())
    def btSetting_clicked(self):
        tk.messagebox.showinfo('Select Instagram Range', 'Please move and resize to fit instagram app window')

        x1 = int(self.config.get('main', 'win_x1'))
        y1 = int(self.config.get('main', 'win_y1'))
        x2 = int(self.config.get('main', 'win_x2'))
        y2 = int(self.config.get('main', 'win_y2'))

        self.regionWin = Toplevel(self)
        self.regionWin.configure(background='#ff0000')
        self.regionWin.geometry(str(x2-x1)+"x" + str(y2-y1) + "+" + str(x1-8) + "+" + str(y1-31))
        self.regionWin.attributes('-alpha', 0.5)
        self.regionWin.wm_attributes('-topmost', True)

        self.btOkay = Button(self.regionWin, text = "O K", command = self.btOk_clicked)
        self.btOkay.place(x=50, y=50, w=80, h=30)

    def btOk_clicked(self):
        lv_x = self.regionWin.winfo_rootx()
        lv_y = self.regionWin.winfo_rooty()
        lv_w = self.regionWin.winfo_width()
        lv_h = self.regionWin.winfo_height()
        print(lv_x, lv_y, lv_w, lv_h)
        self.regionWin.destroy()
        self.position = [lv_x, lv_y, lv_x+lv_w, lv_y+lv_h]

        self.config.set('main', 'win_x1', str(self.position[0]))
        self.config.set('main', 'win_y1', str(self.position[1]))
        self.config.set('main', 'win_x2', str(self.position[2]))
        self.config.set('main', 'win_y2', str(self.position[3]))
        with open(self.config_filename, 'w') as f:
            self.config.write(f)

        return self.position
    
    def bt_follow_pause_clicked(self):
        try:
            self.walkerThread._isPausedFollowing.set()
            self.logger.info('---Following Paused---')
        except Exception as e:
            print(e)
            pass
    
    def bt_follow_resume_clicked(self):
        try:
            self.walkerThread.walker.moveHome()
            self.walkerThread._isPausedFollowing.clear()
            self.logger.info('---Following Resumed---')
        except Exception as e:
            print(e)
            pass

    def setStatus(self, value):
        self.lbStatus['text'] = value

    def exit(self, args=0):
        self.master.destroy()
        sys.exit()

if __name__ == '__main__':
    # print (os.getcwd())
    MainFrm().mainloop()

