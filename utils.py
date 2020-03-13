from tkinter import *
import tkinter as tk

class RegionFrm(Frame):
    def __init__(self):
        tk.Frame.__init__(self)

        self.pack(fill=BOTH, expand=1)
        self.configure(background='#ff0000')
        self.master.geometry("300x600+500+100")

        self.master.attributes('-alpha', 0.3)
        self.master.wm_attributes('-topmost', True)

        self.btOkay = Button(self, text = "O K", command = self.btOk_clicked)
        self.btOkay.place(x=50, y=50, w=80, h=30)


    def btOk_clicked(self):
        lv_x = self.winfo_rootx()
        lv_y = self.winfo_rooty()
        lv_w = self.winfo_width()
        lv_h = self.winfo_height()
        print(lv_x, lv_y)
        self.destroy()

if __name__ == '__main__':
    RegionFrm().mainloop()