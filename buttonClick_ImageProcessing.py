# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 10:52:21 2023

@author: biswa
"""

import os
import copy
import pandas as pd
import pyautogui
from pynput.mouse import Listener
from pynput.keyboard import Key,Controller
import keyboard  # using module keyboard
from threading import Thread
import time    
import cv2
import numpy as np
import pytesseract
# adds image processing capabilities
from PIL import Image  

counter=0
dim=None
coordinates=[]
individual_coordinates=[]
screenDirectory={}
import win32api
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
dirname="C:\\Users\\biswa\\OneDrive\\Desktop\\images"
dirname_csv="C:\\Users\\biswa\\OneDrive\\Desktop"


#cv2.namedWindow("Window_name", cv2.WINDOW_NORMAL)
#cv2.setWindowProperty("Window_name", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


win32api.MessageBox(0, 'Open Images in Full screen', 'Alert',0x00000000)

#img = Image.open(dirname+'\\'+"screen.png")

# img.show()
while True:  # making a loop
    try:  # used try so that if user pressed other than the given key error will not be shown
        
        if keyboard.is_pressed('esc'):  # if key 'q' is pressed 
                w,h=pyautogui.size()
                dim=(w,h)
                print("Screen Size:",w,h)
                break  # finishing the loop
        if keyboard.is_pressed('c'):
            x,y=pyautogui.position()
            #print(x,y) 
            counter+=1
            individual_coordinates.extend([x,y])
            #print("Counter",counter)
            if counter%2==0:
                
                x1 = individual_coordinates[0]
                y1 = individual_coordinates[1]
                x2 = individual_coordinates[2]
                y2 = individual_coordinates[3]
                
                width = abs(x1 - x2)
                height = abs(y1 - y2)
                width = x2
                height = y2
                #area = height * width
                #perimeter = 2 * (height + width)
                coordinates.append([individual_coordinates[0],individual_coordinates[1],width,height])
                individual_coordinates.clear()
                
                counter=0
            time.sleep(.25)
        elif keyboard.is_pressed('r'):
            counter=0
            #print(coordinates)
            individual_coordinates.clear()
            coordinates=coordinates[0:-1]
            #print(coordinates)
            time.sleep(.25)
            #print("======================================")
    except:
        break
print(coordinates)

per=25
#coordinates=[[1251, 589, 1481, 648],[869, 823, 1103, 884],[1395, 825, 1625, 861]]
offset=0#30
addition=0#25
height=0#10 
# opening an image from the source path
#img = Image.open(r'C:\Users\biswa\Downloads\screen.png')     
for file in os.listdir(dirname):
    name=file.split(".")
    name="".join(name[:-1])
    img=cv2.imread(dirname+'\\'+file,cv2.IMREAD_UNCHANGED) 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #print(img.shape)  
    #img = cv2.resize(img, (1896,img.shape[1]), interpolation = cv2.INTER_AREA)
    imgmask=np.zeros_like(img)  
    
    # path where the tesseract module is installed
    
    
    temp=[]
    for ind,data in enumerate(coordinates):
        #cv2.rectangle(img,(offset+data[0],data[1]),(data[0]+offset+data[2]+addition,data[1]+data[3]+height),(255,0,0))
        cv2.rectangle(img,(data[0],data[1]),(data[2],data[3]),(255,0,0),2)
        
        imgmask=cv2.addWeighted(imgmask,0.99,img,0.1,0)
        imgcrop = img[data[1]:data[3],data[0]:data[2]]
        #cv2.imshow(str(ind),imgcrop)
        
        temp.append((data,pytesseract.image_to_string(imgcrop).strip()))
    screenDirectory[name]=temp
                   

#cv2.waitKey(0)
print(screenDirectory)
'''
keys = screenDirectory.keys()
testdata_final = ''
testdata_screens = ''
data_final = ''

for  key in screenDirectory:

    for data in screenDirectory[key]:
        if testdata_final =='':
            testdata_final=key

            data_final=data[1]

        else:
            testdata_final=testdata_final+","+key
            data_final=data_final+","+data[1]



print("Data Final:",data_final)
print("Testdata final:",testdata_final)
if not (len(keys)== 2 and keys[0] == 0  and keys[1] == 1):
    testdata_final = testdata_final + "\n";
    testdata_final = testdata_final + data_final + "\n"
print(testdata_final)
'''
testdata_final = pd.DataFrame.from_dict(screenDirectory)
testdata_final.to_csv('./data/data_to_transport.csv',index=False)