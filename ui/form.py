from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os

class p_chioce(LabelFrame):
    def __init__(self,master,**kwargs):
        super().__init__(master,text="Select images",**kwargs)
        ttk.Label(self,text='Select a picture on your computer to get the text    ',foreground="red").grid(row=0,column=0,columnspan=3,sticky=(W))
        ttk.Button(self,text="Browse",command=self.find_file).grid(row=0,column=3,padx=5,pady=5,sticky=(E))
    def find_file(self):
        default_dir=os.path.join(os.path.expanduser("~"), 'Desktop')
        self.filename = filedialog.askopenfilename(title='打开文件', filetypes=[('JPEG','*.jpg;*.jpeg;*.jpe;*.jfif'),('PNG','*.png'),('All Files','*')],initialdir=(os.path.expanduser(default_dir)))
        self.event_generate('<<LoadImage>>')


class p_cut(LabelFrame):
    def __init__(self,master,**kwargs):
        super().__init__(master,text="screenshot",**kwargs,)
        
        self.image=PhotoImage(file='ui/key.png')
        ttk.Label(self,text="Click to get a screenshot  ",foreground="red").grid(column=0,row=0,sticky=(W))
        Button(self,image=self.image,command=self.screenshot_sign,height=20,width=30).grid(column=1,row=0,padx=5,pady=5,sticky=(E))

    def screenshot_sign(self):
        self.event_generate('<<ScreenShot>>')