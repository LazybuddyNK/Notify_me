import time
import tkinter as tk
from plyer import notification
from tkinter import *
import tkinter.ttk
import datetime
from threading import Timer
from notify_run import Notify 
import pyqrcode
import os

class App(tk.Frame):                        # Copied from stackoverflow:-https://stackoverflow.com/questions/57034118/time-picker-for-tkinter
    def __init__(self, parent):
        super().__init__(parent)
        self.hourstr=tk.StringVar(self,'10')
        self.hour = tk.Spinbox(self,from_=0,to=23,wrap=True,textvariable=self.hourstr,width=2,state="readonly")
        self.minstr=tk.StringVar(self,'30')
        self.minstr.trace("w",self.trace_var)
        self.last_value = ""
        self.min = tk.Spinbox(self,from_=0,to=59,wrap=True,textvariable=self.minstr,width=2,state="readonly")
        self.hour.grid()
        self.min.grid(row=0,column=1)

    def trace_var(self,*args):
        if self.last_value == "59" and self.minstr.get() == "0":
            self.hourstr.set(int(self.hourstr.get())+1 if self.hourstr.get() !="23" else 0)
        self.last_value = self.minstr.get()


def alert(title, msg, sec):
    # now = time.localtime()
    
    # print(app.hour.get(), app.minstr.get())
    
    # new = datetime.datetime.now() + datetime.timedelta(seconds=sec)
    # t = new.strftime("%H:%M:%S")
    
    notification.notify(
        title = title,
        message = msg,
        timeout = sec
    )
    # time.sleep(sec)
    # notification.notify(
    #     title = title,
    #     message = msg,
    #     timeout = sec
    # )

# alert('hey', 'msg', 5)

def ph_alert(msg):
    notify = Notify() 
    notify.send(msg) 

def create():
    title = title_m.get()
    msg = msg_m.get()
    sec = sec_m.get()

    hr = app.hour.get()
    min = app.minstr.get()

    now = datetime.datetime.now()
    time = datetime.datetime.strptime('{0}:{1}'.format(hr,min),'%H:%M').time()
    time = datetime.datetime.combine(datetime.date.today(), time)
    diff = (time - now).total_seconds()

    print(title, msg, sec)
    print(diff)
    # if title!=None and msg!=None:
    alert('Notifi_me', 'Your Notification will be shown at {}:{}.'.format(hr, min), sec)
    timer = Timer(diff, alert, [title, msg, sec])
    timer1 = Timer(diff, ph_alert, [msg])
    # Timer(sec, ph_alert(msg))
    timer.start()
    timer1.start()
    # else:
    #     print('Please provide title and msg')

flag = 0

def load():

    global flag
    if flag == 0:

        with open('data.txt', 'r') as f:
            data = f.read().split('\n')

            for i,j in enumerate(data):
                # Seperator
                if(i>=4):
                    # tk.ttk.Separator(root, orient=VERTICAL).grid(column=2,row=i+4,rowspan=1,sticky='ns')
                    tk.ttk.Separator(root, orient=VERTICAL).pack()

                t = ''
                for a,k in enumerate(j.split('|')):
                    if a==0:
                        t += k+'\n\n'
                    else:
                        t += k+'\n'
                
                if t != '\n\n':
                    btn = tk.Button(second_frame,text=t,relief='ridge',width=50,wraplength=300,borderwidth=5,background='#345',foreground='white',activebackground='firebrick3',activeforeground='white')
                    btn.pack(expand=1,fill=Y,pady=2) # grid(row=i+1,column=3,padx=20)
                    # btn.config(command=lambda b=btn: delete_tag(b))     # [b.bind("<Triple-1>", delete_tag(b))]

                    btn.bind("<Triple-1>", lambda evt, b=btn: delete_tag(evt,b))
                    print(i, j)
                    flag = 1
    
    else:
        with open('data.txt') as f:
            for line in f:
                pass
            last_line = line
            t = ''
            for a,k in enumerate(last_line.split('|')):
                if a==0:
                    t += k+'\n\n'
                else:
                    t += k+'\n'
            
            if t != '\n\n':
                btn = tk.Button(second_frame,text=t,relief='ridge',width=50,wraplength=300,borderwidth=5,background='#345',foreground='white',activebackground='firebrick3',activeforeground='white')
                btn.pack(expand=1,fill=Y,pady=2) # grid(row=i+1,column=3,padx=20)
                # btn.config(command=lambda b=btn: delete_tag(b))     # [b.bind("<Triple-1>", delete_tag(b))]
                btn.bind("<Triple-1>", lambda evt, b=btn: delete_tag(evt,b))

                print(last_line)


# .replace('{','').replace('}','')

def write():
    title = title_m.get()
    msg = msg_m.get()
    sec = sec_m.get()
    # if title!=None and msg!=None:
    with open('data.txt', 'a') as writer:
        text = '\n'+title+'|'+msg+'|'+str(sec)
        writer.write(text)
    # else:
    #     print('Please provide title and msg')

def create_qr():
    s=entvar.get()
    url=pyqrcode.create(s)
    url.png("myqr.png",scale=8)
    os.system("myqr.png")


def delete_tag(event, b):
    t = b.cget('text')
    text = t.replace('\n\n', '|').replace('\n','|')         # turning it back to same text as in data.txt

    # code to delete a particular
    # data from a file
    # open file in read mode
    with open("data.txt", "r") as f:
        
        # read data line by line
        data = f.readlines()
        
    # open file in write mode
    with open("data.txt", "w") as f:
        
        for line in data :
            
            # condition for data to be deleted
            if line.strip("\n")+'|' != text :
                f.write(line)
                # print(line.strip("\n")+'-->'+text)

    b.destroy()
    # print("3 click")
    # print(b.cget('text'))


# create()
root =Tk()
root.title("Notify_me")
root.geometry("750x400")
# root['bg'] = 'cyan'


# ---------------Scrollable feature-----------------
main_frame = tkinter.ttk.Frame(root)
main_frame.pack(fill=BOTH, expand=1)

my_canvas = tk.Canvas(main_frame)
my_canvas.pack(fill=BOTH, expand=1, side=LEFT)

my_scrollbar = tkinter.ttk.Scrollbar(main_frame, orient="vertical", command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

my_canvas.configure(yscrollcommand=my_scrollbar.set)

# scrollable_frame = tkinter.ttk.Frame(my_canvas)

my_canvas.bind(
    "<Configure>",
    lambda e: my_canvas.configure(
        scrollregion=my_canvas.bbox("all")
    )
)
# canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
# canvas.configure(yscrollcommand=scrollbar.set)
second_frame = tkinter.ttk.Frame(my_canvas)

my_canvas.create_window((0,0), window=second_frame, anchor="nw")

def MouseWheelHandler(event):
    global count

    def delta(event):
        if event.num == 5 or event.delta < 0:
            return -1 
        return 1 

    count += delta(event)
    print(count)

count = 0
my_canvas.bind("<MouseWheel>",MouseWheelHandler)
my_canvas.bind("<Button-4>",MouseWheelHandler)
my_canvas.bind("<Button-5>",MouseWheelHandler)
# self.canvas = Canvas(...)
# root.bind_all("<MouseWheel>", on_mousewheel)

# def on_mousewheel(event):
#     root.yview_scroll(-1*(event.delta/120), "units")
# ---------------------Scroll-----------------------


Label(root,text="Enter Title for ur alert:").place(x=400,y=5)
title_m=StringVar()
Entry(root,textvariable=title_m).place(x=600,y=5)

Label(root,text="Enter msg for ur alert:").place(x=400,y=55)
msg_m=StringVar()
Entry(root,textvariable=msg_m).place(x=600,y=55)

Label(root,text="Enter the duration of notification:").place(x=400,y=105)
sec_m=IntVar()
Entry(root,textvariable=sec_m).place(x=600,y=105)

Label(root,text="When do you want your notification:").place(x=400,y=155)
# sec_m=IntVar()
app = App(root)
app.place(x=600,y=155)

Button(root,text="create",command=lambda: [create(), write(), load()]).place(x=400,y=205)

Label(root,text="Click here to generate qr for login.").place(x=400,y=305)
entvar=StringVar()
Entry(root,textvariable=entvar).place(x=600,y=305)
Button(root,text="Genrate QR",command=create_qr).place(x=600,y=355)
# to-do list
tk.ttk.Separator(root, orient=VERTICAL).place(x=400,y=0)
Label(root,text="Your works to be Done-->").place(x=100,y=5)
load()

# --------Delete command ------------
# tags_display_box.bind("<Triple-1>", delete_tag)

mainloop()
