from instapy_cli import client
from os import listdir
from os.path import isfile, join
import time
from tkinter import *
import tkinter as tk
from tkinter import filedialog
import threading
from PIL import ImageTk,Image
from tkinter.ttk import Progressbar

window = Tk()
window.geometry("500x400")
window.title("IMPU | 1.1")

def choose():
    global filename
    filename = filedialog.askdirectory()
    print(filename)
    global onlyfiles
    onlyfiles = [f for f in listdir
             (filename) if isfile(join(filename, f))]
    global length_onlyfiles
    length_onlyfiles = len(onlyfiles)
    print(length_onlyfiles)
    e.delete(0,END)
    e.insert(0,filename)
global gaythanos
gaythanos = ("")
def upload():
    quantity = 0
    username = e_login.get()
    password = e_password.get()
    progress=Progressbar(window,orient=HORIZONTAL,length=100,
                         mode='determinate')
    progress["maximum"] = length_onlyfiles
    progress.place(y=190,x=197)
    with client(username, password) as cli:
        while quantity < length_onlyfiles:
            file_da_caricare = (filename +"/"+ onlyfiles[quantity])
            info_file1 = str(quantity+1)
            info_quantity = str(length_onlyfiles)
            info_file2 = ("["+info_file1+"/"+info_quantity+"] "+file_da_caricare)
            print(info_file2)
            time.sleep(1)
            cli.upload(file_da_caricare)
            quantity += 1
            global gaythanos
            bo2 = str(quantity+1)
            gaythanos = ("Uploading... "+"["+bo2+"/"+info_quantity+"] ")
            progress['value']=quantity
def start_submit_thread(event):
    global submit_thread
    submit_thread = threading.Thread(target=upload)
    submit_thread.daemon = True
    submit_thread.start()
    window.after(20, check_submit_thread)
def progress(currentValue):
    progressbar["value"]=currentValue
def check_submit_thread():
    file_label.config(text=gaythanos)
    if submit_thread.is_alive():
        window.after(20, check_submit_thread)
    else:
        file_label.config(text="Upload Complete")

def stop_upload_thread():
    if submit_thread.is_alive():
       submit_thread.stop()
       print("Thread stopped")
       stop_Button.delete()
    else:
       print("something occured")     

file_label=Label(window,text="")
file_label.place(y=170,x=167)

def on_entry_click(event):
    if e_login.get() == 'Login...':
       e_login.delete(0, "end")
       e_login.insert(0, '') 
       e_login.config(fg = 'black')
def on_focusout(event):
    if e_login.get() == '':
        e_login.insert(0, 'Login...')
        e_login.config(fg = 'grey')       
e_login = Entry(window,width=20)
e_login.pack()
e_login.insert(0, 'Login...')
e_login.bind('<FocusIn>', on_entry_click)
e_login.bind('<FocusOut>', on_focusout)
e_login.config(fg = 'grey')

def on_entry_click(event):
    if e_password.get() == 'Password...':
       e_password.delete(0, "end")
       e_password.insert(0, '') 
       e_password.config(fg = 'black',show= '*')
def on_focusout(event):
    if e_password.get() == '':
        e_password.insert(0, 'Password...')
        e_password.config(fg = 'grey',show= '')
e_password = Entry(window,width=20)
e_password.pack()
e_password.insert(0, 'Password...')
e_password.bind('<FocusIn>', on_entry_click)
e_password.bind('<FocusOut>', on_focusout)
e_password.config(fg = 'grey')

def show_password():
    show_password_get = check_password_var.get()
    if show_password_get == True:
        e_password.config(show='')
    if show_password_get == False:
        e_password.config(show='*')
        
check_password_var = tk.BooleanVar()    
check_password = Checkbutton(window, text="show", var=check_password_var,
                             command=show_password)
check_password.place(y=17,x=335)

e = Entry(window,width=20)
e.place(y = 100, x =167)
Button(window, text="choose folder", command=choose).place(y=98, x=335)
Button(window, text="Upload",
        command=lambda:start_submit_thread(None)).place(y=130,x=210)
window.mainloop()
