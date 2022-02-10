import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image,ImageTk
import cv2
import pickle as pc
import playsound
import os

knn_model = pc.load(open('knn_pickle_final','rb'))

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
from numpy.lib.function_base import angle, average
from skimage.feature import greycomatrix, greycoprops
import math
from scipy import stats

win = tk.Tk()
win.geometry("600x600+200+30")
win.resizable(False, False)
win.configure(bg ='#AB82FF')
w = 400
h = 300

color = "#9F79EE"
frame_1 = Frame(win,width = 600,height =320,bg = color).place(x=0,y=0)
frame_2 = Frame(win,width = 600,height =320,bg = color).place(x=0,y=350)
#Load an image in the script
img= (Image.open("cem.png"))
img_mulai= (Image.open("mulai.png"))
resized_image_mulai= img_mulai.resize((100,60), Image.ANTIALIAS)
mulai_btn= ImageTk.PhotoImage(resized_image_mulai)

#Resize the Image using resize method
resized_image= img.resize((100,60), Image.ANTIALIAS)
camera_btn= ImageTk.PhotoImage(resized_image)

v = Label(frame_1, width=w, height=h)
v.place(x=10, y=10)
cap = cv2.VideoCapture(0)


def Save(im):
    # file = filedialog.asksaveasfilename(filetypes=[("PNG", ".png")])
    img = im.copy()
    imgs_test=[]

    img = cv2.resize(img, (500, 500))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (15, 15), 0)
    cany = cv2.Canny(blurred, 0, 100)

    b, g, r = cv2.split(img)
    rgba = [b,g,r,cany]

    dst = cv2.merge(rgba, 4)

    contours, hierarchy = cv2.findContours(cany, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    select = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(select)

    png = dst[y:y+h, x:x+w]

    png_gray = cv2.cvtColor(png, cv2.COLOR_BGR2GRAY)
    ret, mg = cv2.threshold(png_gray, 60, 255, cv2.THRESH_BINARY_INV)


    # fitur metric
    height1=img.shape[0]
    width1=img.shape[1]
    height2=png.shape[0]
    width2=png.shape[1]

    blurred = cv2.GaussianBlur(gray, (15, 15), 0)
    edge = cv2.Canny(blurred, 0, 100)

    k=0
    keliling = 0
    while k < height1:
        j=0
        while j < width1:
            if edge[k][j] == 255:
                keliling += 1
            j += 1
        k += 1

    k = 0
    luas = 0
    while k < height2:
        j = 0
        while j < width2:
            if mg[k][j] == 0:
                luas += 1
            j += 1
        k += 1

    metric = (4*math.pi*luas)/(keliling*keliling)
    shape_props = [metric]
    for item in shape_props:
        imgs_test.append(item)

    # fitur warna

    R = png[:, :, 0]
    G = png[:, :, 1]
    B = png[:, :, 2]

    mean_r = np.mean(R)
    mean_g = np.mean(G)
    mean_b = np.mean(B)

    color_props = [mean_r,mean_g, mean_b]

    for item in color_props:
        imgs_test.append(item)

    k_pred = knn_model.predict([imgs_test])

    pred_fin = str(k_pred)
    newstr = pred_fin.replace("['","")
    newstr = newstr.replace("']","")
    # label = Label(win,text = newstr,width=43,bg='#9F79EE')
    # label.place(x=0,y=355)

    if newstr=="pir":
        playsound.playsound('F:/Kampus/Workshop Citra dan Cerdas/ProjekCitra/Suara Buah/Pir.mp3')
        label = Label(win,text = "Buah Pir",width=43,bg='#9F79EE')
        label.place(x=0,y=355)
        foto_apel=Image.open('F:/Kampus/Workshop Citra dan Cerdas/ProjekCitra/Gambar Buah/pir.png')
        resized_image= foto_apel.resize((150,150), Image.ANTIALIAS)
        poto= ImageTk.PhotoImage(resized_image)
        win.lab=Label(image=poto,text="white").place(x=400, y=370) 
        win.lab.pack()

    elif newstr=="apel":
        label = Label(win,text = "Buah Apel",width=43,bg='#9F79EE')
        label.place(x=0,y=355)
        playsound.playsound('F:/Kampus/Workshop Citra dan Cerdas/ProjekCitra/Suara Buah/Apel.mp3')
        foto_apel=Image.open('F:/Kampus/Workshop Citra dan Cerdas/ProjekCitra/Gambar Buah/apel.png')
        resized_image= foto_apel.resize((150,150), Image.ANTIALIAS)
        poto= ImageTk.PhotoImage(resized_image)
        win.lab=Label(image=poto,text="white").place(x=400, y=370) 
        win.lab.pack()
        
    elif newstr=="pisang":
        label = Label(win,text = "Buah Pisang",width=43,bg='#9F79EE')
        label.place(x=0,y=355)
        playsound.playsound('F:/Kampus/Workshop Citra dan Cerdas/ProjekCitra/Suara Buah/Pisang.mp3')
        foto_apel=Image.open('F:/Kampus/Workshop Citra dan Cerdas/ProjekCitra/Gambar Buah/pisang.png')
        resized_image= foto_apel.resize((150,150), Image.ANTIALIAS)
        poto= ImageTk.PhotoImage(resized_image)
        win.lab=Label(image=poto,text="white").place(x=400, y=370) 
        win.lab.pack()

    elif newstr=="lemon":
        label = Label(win,text = "Buah Lemon",width=43,bg='#9F79EE')
        label.place(x=0,y=355)
        playsound.playsound('F:/Kampus/Workshop Citra dan Cerdas/ProjekCitra/Suara Buah/Lemon.mp3')
        foto_apel=Image.open('F:/Kampus/Workshop Citra dan Cerdas/ProjekCitra/Gambar Buah/lemon.png')
        resized_image= foto_apel.resize((150,150), Image.ANTIALIAS)
        poto= ImageTk.PhotoImage(resized_image)
        win.lab=Label(image=poto,text="white").place(x=400, y=370) 
        win.lab.pack()

    elif newstr=="jeruk":
        label = Label(win,text = "Buah Jeruk",width=43,bg='#9F79EE')
        label.place(x=0,y=355)
        playsound.playsound('F:/Kampus/Workshop Citra dan Cerdas/ProjekCitra/Suara Buah/Jeruk.mp3')
        foto_apel=Image.open('F:/Kampus/Workshop Citra dan Cerdas/ProjekCitra/Gambar Buah/jeruk.png')
        resized_image= foto_apel.resize((150,150), Image.ANTIALIAS)
        poto= ImageTk.PhotoImage(resized_image)
        win.lab=Label(image=poto,text="white").place(x=400, y=370) 
        win.lab.pack()

    elif newstr=="mangga":
        label = Label(win,text = "Buah Mangga",width=43,bg='#9F79EE')
        label.place(x=0,y=355)
        playsound.playsound('F:/Kampus/Workshop Citra dan Cerdas/ProjekCitra/Suara Buah/Mangga.mp3')
        foto_apel=Image.open('F:/Kampus/Workshop Citra dan Cerdas/ProjekCitra/Gambar Buah/mangga.png')
        resized_image= foto_apel.resize((150,150), Image.ANTIALIAS)
        poto= ImageTk.PhotoImage(resized_image)
        win.lab=Label(image=poto,text="white").place(x=400, y=370) 
        win.lab.pack()

    else:
        print("buah tidak terdeteksi")
    # image.save(file+'.png')
    # print(newstr)

def take_copy(im):
    la = Label(frame_2, width=w-100, height=h-100)
    la.place(x=10, y=380)
    copy = im.copy()
    copy = cv2.resize(copy, (w-100, h-100))
    rgb = cv2.cvtColor(copy, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(copy)
    imgtk = ImageTk.PhotoImage(image)
    la.configure(image=imgtk)
    la.image = imgtk
    save = Button(win,image= mulai_btn,command=lambda : Save(rgb))
    save.place(x=425,y=530)



def select_img():
    global rgb
    _, img = cap.read()
    img = cv2.resize(img, (w, h))
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(rgb)
    imgtk = ImageTk.PhotoImage(image)
    v.configure(image=imgtk)
    v.image = imgtk
    v.after(10, select_img)

def upload_file():
    global img
    f_types = [('Jpg Files', '*.jpg')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    img = ImageTk.PhotoImage(file=filename)
    b2 =tk.Button(win,image=img) # using Button 
    b2.grid(row=3,column=1)
    
select_img()
snap = Button(win, image=camera_btn, command=lambda: take_copy(rgb))
snap.place(x=450, y=150)


browse_image = Button(frame_1,text="Browse Image",bg='#AB82FF',command=lambda:upload_file())
browse_image.place(x=0,y=323)

win.mainloop()