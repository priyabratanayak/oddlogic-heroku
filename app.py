# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 16:52:52 2023

@author: biswa
"""

import os

import copy
import pandas as pd
import keyboard  # using module keyboard
import time

import numpy as np
import pytesseract
# adds image processing capabilities
from PIL import Image  
import math
from flask import Flask, jsonify, request, render_template
import shutil
import os
#--------On Local System
#pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

# ----------------pytesseract on Heroku (deployment ONLY)
pytesseract.pytesseract.tesseract_cmd = "/app/.apt/usr/bin/tesseract"

dirname="./images"
dirname_csv="./"


app=Flask(__name__)

               
@app.route('/')
def hello_world():
    return 'Hello !!!'

#@app.route('/move/<coordinates>')
#def move(coordinates):  
@app.route('/move/',methods = ['GET','POST'])
def move():
    import pyautogui
    adjustment_x=0#60
    adjustment_y=0#20
    coordinate_json=request.get_json()
    coord=coordinate_json['title']
    testdata=coordinate_json['testdata']
    tag=coordinate_json['tag']
    width=int(coord[2])-int(coord[0])
    height=int(coord[3])-int(coord[1])
    pyautogui.moveTo(int(adjustment_x+coord[0]+math.floor(width/2)), adjustment_y+int(coord[1]+math.floor(height/2)),duration=0.1)
    
    if tag.strip().lower()=='data':
       
        pyautogui.click();
        pyautogui.click();
        pyautogui.hotkey('ctrl','a')
        pyautogui.typewrite(testdata)
  
    message = {'coordinates':coord}
    return jsonify(message)
@app.route('/save/<screen>')
def save(screen):
    import win32api
    import pyautogui
    win32api.MessageBox(0, 'Go to the Application', 'Alert',0x00001000)
    time.sleep(0.5)
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save("./screen/"+screen+'.png')    
    return ""
@app.route('/copy/')
def copy(): 
    # path to source directory
    src_dir = 'C:/Users/biswa/OneDrive/Desktop/images/'
     
    # path to destination directory
    dest_dir = './screen/'
     
    # getting all the files in the source directory
    files = os.listdir(src_dir)
     
    for fname in files:
     
        # copying the files to the
        # destination directory
        shutil.copy2(os.path.join(src_dir,fname), dest_dir)
      
    return ""
#@app.route('/run/<screen>')
@app.route('/run/',methods = ['GET','POST'])
def run(): 
    screen=request.get_json()
    screen=screen['title']
    df = pd.read_csv('./data/data_to_transport.csv')
    screen_data=df[screen].tolist()
    
   # win32api.MessageBox(0, 'Go to the Application and Click Ok.', 'Alert',0x00001000)
    coord_list=[]
    testdata_list=[]
    tag=[]
    for data in screen_data:
        data=data.replace("(","")
        data=data.replace(")","")
        data=eval(data)
        cord=data[0]
        testdata=data[1]
        tag_ind=data[2]
        #win32api.MessageBox(0, tag, 'Alert',0x00001000)
        value=data[1]
        #win32api.MessageBox(0, str(cord[0])+":"+str(((cord[2]-cord[0])/2)), 'Alert',0x00001000)
        x=abs(int(cord[0]+int((cord[2]-cord[0])/2)))
        y=abs(int(cord[1]+int((cord[3]-cord[1])/2)))
        coord_list.append([x,y])
        testdata_list.append(testdata)
        tag.append(tag_ind)
        #win32api.MessageBox(0, str(x)+":"+str(y), 'Alert',0x00001000)
        #pyautogui.moveTo(x, y)
        
    message = {'coordinates':coord_list,'testdata':testdata_list,'tag':tag}
    return jsonify(message)
@app.route('/fetch/',methods = ['GET'])
def fetch(): 
    
    df = pd.read_csv('./data/data_to_transport.csv')
    df=df.fillna("")
        
    message = {'screendata':df.to_dict('dict')}
    return jsonify(message)  
@app.route('/capture')
def capture():
    import win32api
    import pyautogui
    counter=0
    dim=None
    coordinates=[]
    individual_coordinates=[]
    screenDirectory={}
    testdata=[]

    #cv2.namedWindow("Window_name", cv2.WINDOW_NORMAL)
    #cv2.setWindowProperty("Window_name", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


    win32api.MessageBox(0, 'Open Images in Full screen', 'Alert',0x00001000)

    #img = Image.open(dirname+'\\'+"screen.png")

    # img.show()
    
    while True:  # making a loop
        try:  # used try so that if user pressed other than the given key error will not be shown
            
            if keyboard.is_pressed('esc'):  # if key 'q' is pressed 
                    w,h=pyautogui.size()
                    dim=(w,h)
                    
                    break  # finishing the loop
            #press r to capture element coordinates without the test data
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
                    testdata.append("tag")
                    counter=0
                time.sleep(.25)
            #press r to capture element coordinates along with test data
            if keyboard.is_pressed('d'):
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
                    testdata.append("data")
                    counter=0
                time.sleep(.25)
            # press r to update the element captured
            elif keyboard.is_pressed('r'):
                counter=0
                #print(coordinates)
                individual_coordinates.clear()
                coordinates=coordinates[0:-1]
                testdata=testdata[0:-1]
                #print(coordinates)
                time.sleep(.25)
                #print("======================================")
        except:
            break
    #print(coordinates)
    
    #win32api.MessageBox(0, ",".join(testdata), 'Alert',0x00001000)
    per=25
    #coordinates=[[1251, 589, 1481, 648],[869, 823, 1103, 884],[1395, 825, 1625, 861]]
    offset=0#30
    addition=0#25
    height=0#10 
    # opening an image from the source path
    #img = Image.open(r'C:\Users\biswa\Downloads\screen.png')     
    for file in os.listdir(dirname):
        import cv2
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
            
            temp.append((data,pytesseract.image_to_string(imgcrop).strip(),testdata[ind]))
        screenDirectory[name]=temp
                       

    #cv2.waitKey(0)
    
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
if __name__=="__main__":
    app.run()
