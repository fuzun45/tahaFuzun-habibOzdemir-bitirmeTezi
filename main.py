from tkinter import Tk, Label, Button,filedialog,Scale
from pydicom import dcmread
from pydicom.data import get_testdata_file
import os
import tkinter as tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 
import cv2
import numpy as np
from skimage import exposure,morphology
from scipy import ndimage

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("DICOM VIEWER")

        self.master.attributes("-zoomed",True)
        self.label = Label(master, text="Aşağıdan dosya listesini seçiniz")
        self.label.pack()

        self.greet_button = Button(master, text="Choose Folder", command=self.askDirectoryPath)
        self.greet_button.pack()

        self.scale = Scale(master, from_=0, to =312, command = self.slider , orient =tk.HORIZONTAL)
        self.scale.pack()

        self.label1 = Label(master, text="")
        self.label1.pack()
        self.plot_button = Button(master, text="Plot", command=self.plot)
        self.plot_button.pack()

        
        #self.clear_button = Button(master, text="Clear", command=self.clear)
        #self.clear_button.pack()

        self.counter =0

    def askDirectoryPath(self):
    
        self.folderPath = filedialog.askdirectory()
    


    def slider(self,val):
        
        self.val = val
        print(self.val)
        return self.val

    def readDicom(self):

        arr = sorted(os.listdir(self.folderPath))
    
        val = self.slider(self.scale).get()
        
        return dcmread(self.folderPath + "/" + arr[val])

    

    def plot(self): 

        if self.counter >0:
            self.canvas.get_tk_widget().pack_forget()
        
        # the figure that will contain the plot 
        self.fig = plt.figure(figsize=(15,15),dpi=1000)

        
    
        # list of squares 
        
        self.img_org = self.readDicom().pixel_array
        # adding the subplot 
        self.plot1 = self.fig.add_subplot(241)
        #self.plot1.set_xlabel("deneme", fontsize=12)
        # plotting the graph 

        self.plot1.set_title("Input Image",fontdict={"fontsize":2},y=.8)
        self.plot1.imshow(self.img_org, cmap= "gray") 

        self.plot1.axes.xaxis.set_visible(False)
        self.plot1.axes.yaxis.set_visible(False)
        # creating the Tkinter canvas 
        

        self.plot2 = self.fig.add_subplot(242)
        self.plot2.set_title("Hounsfield Unit Histogram",fontdict={"fontsize":2},y=.8)
        self.plot2.hist(self.img_org.flatten(), color='c' ,bins=80 )
        
        
        self.plot2.axes.xaxis.set_visible(False)
        self.plot2.axes.yaxis.set_visible(False)
        
        
        # Gaussian Filter

       
        self.plot3 = self.fig.add_subplot(245)
        

        
        self.img = cv2.blur(self.img_org,(8,8))
        #plt.suptitle("Implementation of Gaussian Filter",y=.9 ,size=16)

        #self.plot3.imshow(img,cmap="gray"),plt.title('Original')
        #self.plot3.xticks([]), self.plot3.yticks([])

        self.plot3.set_title("Gaussian Blur",fontdict={"fontsize":2},y=.8)
        self.plot3.imshow(self.img,cmap="gray")
        #self.plot4.xticks([]), self.plot4.yticks([])

        self.plot3.axes.xaxis.set_visible(False)
        self.plot3.axes.yaxis.set_visible(False)
        

        # Thresholding

        from skimage.filters import threshold_mean
        
        


        self.plot4 = self.fig.add_subplot(246)

        
        self.retval, self.img = cv2.threshold(self.img, 232, 255, cv2.THRESH_BINARY)
        self.plot4.set_title("Thresholding",fontdict={"fontsize":2},y=.8)
        self.plot4.imshow(self.img,cmap="gray")

        self.plot4.axes.xaxis.set_visible(False)
        self.plot4.axes.yaxis.set_visible(False)
        


        self.kernel = np.ones((16,16),np.uint8)
        self.erosion = cv2.morphologyEx(self.img, cv2.MORPH_OPEN, self.kernel)
        self.plot5 = self.fig.add_subplot(122)
        #self.plot6 = self.ax[0,2]
        #self.img = exposure.equalize_adapthist(self.masked_image)
        self.plot5.set_title("Output Image",fontdict={"fontsize":2},y=.92)
        self.plot5.imshow(self.erosion , cmap="gray")


        self.plot5.axes.xaxis.set_visible(False)
        self.plot5.axes.yaxis.set_visible(False)


        #self.plot6.axes.xaxis.set_visible(False)
        #self.plot6.axes.yaxis.set_visible(False)

        # containing the Matplotlib figure 
        self.canvas = FigureCanvasTkAgg(self.fig, 
                                master = root)   
        self.canvas.draw() 
        
    
        # placing the canvas on the Tkinter window 
        self.canvas.get_tk_widget().pack() 
    
        self.fig.canvas.flush_events()

        self.counter +=1





root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()