
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile
import cv2
import PIL
from PIL import ImageTk,Image
import time

class App:
    def init(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        my_menu = Menu(self.window)
        self.window.config(menu=my_menu)

        #<-------------------Panel Area------------------------->
        sidebar = Frame(self.window, width=200, bg='grey', height=500, relief='sunken', borderwidth=2)
        sidebar.pack(expand=False, fill='both', side='left', anchor='nw')

        Label(sidebar,text='EXPLORE',bg="grey",fg='white',font=('comicsansmas',19,'bold')).pack(fill='x')

        Mynotebook = ttk.Notebook(window)
        Mynotebook.pack()

        mainarea = Frame(Mynotebook, bg='grey23', width=1500, height=1500)
        mainarea.pack(expand=True, fill='both', side='right')

        def OpenCamera():
            self.vid = MyVideoCapture(self.video_source)
            self.canvas = tkinter.Canvas(mainarea, width =self.vid.width, height = self.vid.height)
            self.canvas.pack(fill='both',expand=1)
            Label(sidebar,text='-->WEB Camera',bg='grey',fg='white',font=('comicsansms',10,'bold')).pack(pady=10,fill='x')
            Mynotebook.add(mainarea,text='web camera')
            self.delay = 15
            self.update()

        def OpenVideo():
            window.filename=tkinter.filedialog.askopenfile(mode ='r', filetypes =[('video file', '*.*')])
            letstring=str(window.filename)
            flag=0
            savestr=''
            for i in range(len(letstring)):
                if letstring[i]=='\'':
                    flag+=1
                    continue
                if flag==1:
                    savestr+=letstring[i]
                if flag==2:
                    break
            print(savestr)
            if savestr != '':
                print(savestr)
            else:
                print('could not find any video')
            self.vid = MyVideoCapture(savestr)
            self.canvas = tkinter.Canvas(mainarea, width = self.vid.width, height = self.vid.height)
            self.canvas.pack()
            Mynotebook.add(mainarea,text=f'{savestr}')
            self.delay = 15
            self.update()

            
        #<----------------------File menu----------------------->
        filemenu = Menu(my_menu,tearoff=False)
        my_menu.add_cascade(label='File',menu=filemenu)
        filemenu.add_command(label='Open Image',command=OpenVideo)
        filemenu.add_command(label='Open Video',command=OpenVideo)
        filemenu.add_command(label='Web Camm',command=OpenCamera)
        filemenu.add_command(label='Exit',command=self.window.quit)
        #<----------------------Edit menu------------------------>
        Editmenu = Menu(my_menu,tearoff=False)
        my_menu.add_cascade(label='Edit',menu=Editmenu)
        Editmenu.add_command(label='Creae text file',command='fileselecter')
        Editmenu.add_command(label='Change Geometry Color',command='prog')
        # #<------------------------EXIT----------------------------->
        my_menu.add_command(label='Exit',command=self.window.quit)


        self.window.mainloop()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray,1.3,4)
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def init(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def del(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")