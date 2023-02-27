# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 15:46:54 2023

@author: biswa
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 20:16:41 2022

@author: 028906744
"""
import cv2
import numpy as np
import pytesseract
# adds image processing capabilities
from PIL import Image    
  
per=25
roi=[[1251, 589, 1481, 648],[869, 823, 1103, 884],[1391, 825, 1625, 881]]
offset=0#30
addition=0#25
height=0#10
# opening an image from the source path
#img = Image.open(r'C:\Users\biswa\Downloads\screen.png')     
  
img=cv2.imread(r'C:\Users\biswa\Downloads\screen.png')   
imgmask=np.zeros_like(img)  

# path where the tesseract module is installed
pytesseract.pytesseract.tesseract_cmd ='C:\Program Files\Tesseract-OCR/tesseract.exe' 


for data in roi:
    #cv2.rectangle(img,(offset+data[0],data[1]),(data[0]+offset+data[2]+addition,data[1]+data[3]+height),(255,0,0))
    cv2.rectangle(img,(data[0],data[1]),(data[2],data[3]),(255,0,0),2)
    
    #img=cv2.addWeighted(img,0.99,imgmask,0.1,0)

#img=cv2.resize(img,)                   
cv2.imshow("screen",img)
cv2.waitKey(0)