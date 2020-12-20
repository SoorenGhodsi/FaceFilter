import cv2
import math
import numpy as np 
from scipy import ndimage
import time

# path = '/Users/YOUR/PATH/HERE/share/opencv4/haarcascades/'

#get facial classifiers
face_cascade = cv2.CascadeClassifier('haarcascade-xmls/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade-xmls/haarcascade_eye.xml')

#read images
fltr = cv2.imread('assets/heart.png')

#get shape of fltr
original_fltr_h,original_fltr_w,fltr_channels = fltr.shape

#convert to gray
fltr_gray = cv2.cvtColor(fltr, cv2.COLOR_BGR2GRAY)

#create mask and inverse mask of fltr
ret, original_mask = cv2.threshold(fltr_gray, 10, 255, cv2.THRESH_BINARY_INV)
original_mask_inv = cv2.bitwise_not(original_mask)

#read video
cap = cv2.VideoCapture(0)
ret, img = cap.read()
img_h, img_w = img.shape[:2]

while True:   #continue to run until user breaks loop
    
    #read each frame of video and convert to gray
    ret, img = cap.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    #find faces in image using classifier
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    
    #for every face found:
    for (x,y,w,h) in faces:
        #retangle for testing purposes
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

    
        #select face as region of interest 
        roi_g = gray[y:y+h,x:x+h]
        roi_c = img[y:y+h,x:x+h]
        #within region of interest find eyes
        eyes = eye_cascade.detectMultiScale(roi_g)
        #for each eye
        eye_y = []
        for (ex,ey,ew,eh) in eyes:
            #draw retangle around eye
            eye_y.append(ey)
            cv2.rectangle(roi_c, (ex,ey),(ex+ew,ey+eh),(0,255,0),2)    

        '''
        #sort eye y-values
        eye_y = sorted(eye_y)
    
        #rotate filter if eyes are not in a straight line
        if len(eye_y) >= 2:
            diff = (eye_y[0] - eye_y[1])
        
            if len(eye_y) == 3:
                if abs(eye_y[1] - eye_y[0]) < abs(eye_y[2] - eye_y[1]):
                    diff = eye_y[1] - eye_y[0]
                else:
                    diff = eye_y[2] - eye_y[1]
            
            angle = math.degrees(math.atan(diff / int(0.5 * w)))
        
            #rotate filter, mask, and inverse mask by degrees
            fltr2 = ndimage.rotate(fltr, angle)
            original_mask2 = ndimage.rotate(original_mask, angle)
            original_mask_inv2 = ndimage.rotate(original_mask_inv, angle)
        '''
        fltr2 = fltr
        #convert mask to gray
        fltr2_gray = cv2.cvtColor(fltr2, cv2.COLOR_BGR2GRAY)
    
        #recreate mask and inverse mask for rotated filter
        ret, original_mask2 = cv2.threshold(fltr2_gray, 10, 255, cv2.THRESH_BINARY_INV)
        original_mask_inv2 = cv2.bitwise_not(original_mask2)    
            
            
        #coordinates of face region
        face_w = w
        face_h = h
        face_x1 = x
        face_x2 = face_x1 + face_w
        face_y1 = y
        face_y2 = face_y1 + face_h

        #fltr size in relation to face by scaling
        fltr_width = int(1.25 * face_w)
        fltr_height = int(fltr_width * original_fltr_h / original_fltr_w)
        
        #setting location of coordinates of fltr
        fltr_x1 = face_x2 - int(face_w/2) - int(fltr_width/2)
        fltr_x2 = fltr_x1 + fltr_width
        fltr_y1 = face_y1 - int(face_h/2.5)
        fltr_y2 = fltr_y1 + fltr_height 

        #check to see if out of frame
        if fltr_x1 < 0:
            fltr_x1 = 0
        if fltr_y1 < 0:
            fltr_y1 = 0
        if fltr_x2 > img_w:
            fltr_x2 = img_w
        if fltr_y2 > img_h:
            fltr_y2 = img_h

        #Account for any out of frame changes
        fltr_width = fltr_x2 - fltr_x1
        fltr_height = fltr_y2 - fltr_y1

        #resize fltr to fit on face
        fltr2 = cv2.resize(fltr2, (fltr_width,fltr_height), interpolation = cv2.INTER_AREA)
        mask = cv2.resize(original_mask2, (fltr_width,fltr_height), interpolation = cv2.INTER_AREA)
        mask_inv = cv2.resize(original_mask_inv2, (fltr_width,fltr_height), interpolation = cv2.INTER_AREA)

        #take ROI for fltr from background that is equal to size of fltr image
        roi = img[fltr_y1:fltr_y2, fltr_x1:fltr_x2]

        #original image in background (bg) where fltr is not
        roi_bg = cv2.bitwise_and(roi,roi,mask = mask)
        roi_fg = cv2.bitwise_and(fltr2,fltr2,mask=mask_inv)
        dst = cv2.add(roi_bg,roi_fg)

        #put back in original image
        img[fltr_y1:fltr_y2, fltr_x1:fltr_x2] = dst

        time.sleep(.07)

        break
        
    #display image
    cv2.imshow('img',img) 

    #if user pressed 'q' break
    if cv2.waitKey(1) == ord('q'): # 
        break;

cap.release() #turn off camera 
cv2.destroyAllWindows() #close all windows
