from tkinter import *
import tkinter as tk
from ui.form import p_chioce,p_cut
from PIL import ImageGrab,Image,ImageTk
from image_deal import read_image
import win32api,win32gui,win32print,win32con        #pip install pywin32

class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


class ImageDeal(Tk,Singleton):
    def __init__(self):
        super().__init__()
        self.title('Recognize words of image V2.0')
        # self.resizable(False,False)
        # self.geometry('640x480')
        self.event_bind()
        image=ImageTk.PhotoImage(Image.open('1.ico'))
        self.iconphoto(False,image)    
        # self.iconphoto(False,PhotoImage(file='ico.png')) #加载图标放后面（加载有一定时间？），避免出现默认界面
        self.columnconfigure(0,weight=1)        #调整缩放后的界面布局
        self.rowconfigure(2,weight=1)
        self.rowconfigure(4,weight=1)

        self.sp_frame=p_chioce(self)
        self.sp_frame.grid(row=0,column=0,padx=5,pady=5,sticky=(N,W,E))

        self.cp_frame=p_cut(self)
        self.cp_frame.grid(row=1,column=0,padx=5,sticky=(N,W,E))

        self.cvm=Canvas(self,bg='white')
        #do :set size of canvas
        self.cvm.grid(row=2,column=0,padx=5,pady=5,sticky=(N,W,E,S))

        self.bt=Button(self,text='recognize',fg="blue",command=self.recognize)
        self.bt.grid(row=3,column=0,padx=200,pady=5,sticky=(N,E,S))

        self.wd=Text(self)
        self.wd.grid(row=4,column=0,padx=5,pady=5,sticky=(N,W,E,S))

    def event_bind(self):
        self.bind('<<ScreenShot>>', self.screenshot)
        self.bind('<<LoadImage>>',self.loadimage)
        # self.bind('<Motion>',self.coord)

    def coord(self,event):
        print(event.x,event.y)

    def screenshot(self,event):
        self.state('icon')
        self.f1=Toplevel(self)
        self.f1.wm_attributes("-alpha",0.6)
        self.f1.overrideredirect(True)
        ws=self.f1.winfo_screenwidth()
        hs=self.f1.winfo_screenheight()
        s=str(ws)+"x"+str(hs)
        self.f1.geometry(s)
        self.f1.wm_attributes('-transparentcolor',"gray")
        Button(self.f1,text='关闭',command=self.closeToplevel,bg="blue").pack(side='right')
        self.cv=Canvas(self.f1)
        self.cv.pack(fill='both',expand=1)          #使Canvas实例自动充满Toplevel窗体
        self.cv.bind("<ButtonPress-1>",self.StartMove)  #绑定鼠标左键按下事件，为在Toplevel窗体上拖动鼠标画矩形做准备
        self.cv.bind("<ButtonRelease-1>",self.StopMove) #绑定鼠标左键松开事件
        self.cv.bind("<B1-Motion>", self.OnMotion)   #绑定鼠标左键被按下时移动鼠标事件

    def loadimage(self,event):
        self.cvm.delete('P')
        self.filepath=self.sp_frame.filename
        self.image=self.imageSizable(Image.open(self.filepath))
        self.img=ImageTk.PhotoImage(self.image)
        self.cvm.create_image(0,0,image=self.img,tags=('P'),anchor=('nw'))   #将img在主窗口显示,img必须是全局变量,不能丢失

    def get_real_resolution(self):
        """获取真实的分辨率"""
        hDC = win32gui.GetDC(0)
        wide = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
        high = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
        return {"wide": wide, "high": high}

    def get_screen_size(self):
        """获取缩放后的分辨率"""
        wide = win32api.GetSystemMetrics(0)
        high = win32api.GetSystemMetrics(1)
        return {"wide": wide, "high": high}

    def get_scaling(self):
        '''获取屏幕的缩放比例'''
        real_resolution = self.get_real_resolution()
        screen_size = self.get_screen_size()
        proportion = round(real_resolution['wide'] / screen_size['wide'], 2)
        return proportion


    def closeToplevel(self):
        self.f1.destroy()
        self.state('normal')

    def imageSizable(self,image=None):
        x,y=image.size[0],image.size[1]
        if(x<500)and(y<250):
            return image
        if(x/500<y/250):
            pro=y/250
        else:
            pro=x/500
        x=x/pro
        y=y/pro
        return image.resize((int(x),int(y)),Image.LANCZOS)

    def StartMove(self,event):
        self.first_x,self.first_y = event.x,event.y       #拖动鼠标画矩形其左上角坐标必须记住，保持不变
        self.cv.create_rectangle(self.first_x,self.first_y,event.x+1,event.y+1,fill='gray', outline='gray',tags=('L')) #左上角坐标，右下角坐标，填充颜色，边框颜色
        
    def StopMove(self,event):
        if abs(self.first_x-event.x)<10 or abs(self.first_y-event.y)<10:      #如截取的图像太小无意义，可能是误操作
            self.cv.delete('L')                                          #删除这个误操作所画矩形
            return
        x=self.f1.winfo_rootx()+self.first_x      #x=Toplevel窗体在屏幕坐标系中的x坐标+所画透明矩形左上角x坐标
        y=self.f1.winfo_rooty()+self.first_y
        x1=x+abs(self.first_x-event.x)       #abs(first_x-event.x)是所画透明矩形的宽
        y1=y+abs(self.first_y-event.y)       #abs(first_y-event.y)是所画透明矩形的高
        proportion=self.get_scaling()
        self.image=ImageGrab.grab((x*proportion,y*proportion,x1*proportion,y1*proportion))   #截取屏幕透明矩形内图像。因PIL的问题(以真实分辨率进行截图)，必须将显示设置里的缩放比例调成100%，这里通过计算缩放后的坐标截图的方式解决
        self.image_deal=self.imageSizable(self.image)
        self.img = ImageTk.PhotoImage(image=self.image_deal)              #将image1转换为canvas能显示的格式
        self.cvm.delete('P')                                #删除上一个截取图像
        self.cvm.create_image(0,0,image=self.img,tags=('P'),anchor=('nw'))   #将img在主窗口显示,img必须是全局变量,不能丢失
        self.f1.destroy()                    #关闭Toplevel窗体
        self.state('normal')            #使主窗体正常显示    

    def OnMotion(self,event):
        self.cv.coords('L',self.first_x,self.first_y,event.x,event.y)  #移动透明矩形到新位置,左上角坐标不变,右下角为新位置
    
    def recognize(self):
        self.image.save('test1.jpg')
        try:
            Recogn_image=read_image()
            word_list=Recogn_image.do_ai(Recogn_image.get_file_content(r'test1.jpg'))
            for word in word_list:
                self.wd.insert("end",word)
                self.wd.insert("end",'\n')
        except Exception as e:
            print(e)
        pass


if __name__=="__main__":
    tool=ImageDeal()
    tool.mainloop()

  