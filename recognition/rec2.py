'''
Adds filters on images with multiple people
'''

import cv2
import math
import numpy as np 
from scipy import ndimage

#get facial classifiers
face_cascade = cv2.CascadeClassifier('haarcascade-xmls/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade-xmls/haarcascade_eye.xml')

#read images
img = cv2.imread('assets/people1.jpg')
fltr = cv2.imread('assets/goggles.png')

#get shape of filter
original_fltr_h,original_fltr_w,fltr_channels = fltr.shape

#get shape of img
img_h,img_w,img_channels = img.shape

#convert to gray
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
fltr_gray = cv2.cvtColor(fltr, cv2.COLOR_BGR2GRAY)

#create mask and inverse mask of filter
#use THRESH_BINARY_INV with transparent background
#use THRESH_BINARY with white background
ret, original_mask = cv2.threshold(fltr_gray, 10, 255, cv2.THRESH_BINARY_INV)
original_mask_inv = cv2.bitwise_not(original_mask)

#find faces in image using classifier
faces = face_cascade.detectMultiScale(img_gray, 1.3, 5)

for (x,y,w,h) in faces:
    #retangle for testing purposes
    # img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    
    #declare new filter, mask, and inverse mask
    fltr2 = fltr
    original_mask2 = original_mask
    original_mask_inv2 = original_mask_inv

    #select face as region of interest 
    roi_lg = img_gray[y:y+int(0.7*h),x:x+int(0.5*h)]
    roi_lc = img[y:y+int(0.7*h),x:x+int(0.5*h)]
    #within region of interest find eyes
    eyesl = eye_cascade.detectMultiScale(roi_lg)
    
    #make empty list
    eye_x = [0, 0]
    eye_y = [0, 0]
    
    #take the first eye's x and y values
    if len(eyesl) > 0:
        eye_x[0] = eyesl[0][0]
        eye_y[0] = eyesl[0][1]
        
    '''
    #for each eye
    for (ex,ey,ew,eh) in eyesl:
        #draw retangle around eye
        cv2.rectangle(roi_lc, (ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    '''
    
    #select face as region of interest 
    roi_rg = img_gray[y:y+int(0.7*h),x+int(0.5*h):x+h]
    roi_rc = img[y:y+int(0.7*h),x+int(0.5*h):x+h]
    #within region of interest find eyes
    eyesr = eye_cascade.detectMultiScale(roi_rg)
    
    #take the first eye's x and y values
    if len(eyesr) > 0:
        eye_x[1] = eyesr[0][0]
        eye_y[1] = eyesr[0][1]
        
    '''
    #for each eye
    for (ex,ey,ew,eh) in eyesr:
        #draw retangle around eye
        cv2.rectangle(roi_rc, (ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    '''
    
    #rotate filter if eyes are not in a straight line
    if len(eyesr) > 0 and len(eyesl) > 0:
        #find the angle between the eyes
        diff = eye_y[0] - eye_y[1]
        if diff < 0:
            angle = -1* math.degrees(math.atan((math.sqrt(abs(diff)) * 1) / (abs(eye_x[1] - eye_x[0]) * 2)))
        else:
            angle = math.degrees(math.atan((math.sqrt(diff) * 1) / (abs(eye_x[1] - eye_x[0]) * 2)))
        
        #rotate filter, mask, and inverse mask by degrees
        fltr2 = ndimage.rotate(fltr, angle)
        original_mask2 = ndimage.rotate(original_mask, angle)
        original_mask_inv2 = ndimage.rotate(original_mask_inv, angle)
    
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

    #filter size in relation to face by scaling
    fltr_width = int(1.25 * face_w)
    fltr_height = int(fltr_width * original_fltr_h / original_fltr_w)
    
    #setting location of coordinates of filter
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

    #account for any out of frame changes
    fltr_width = fltr_x2 - fltr_x1
    fltr_height = fltr_y2 - fltr_y1

    #resize filter to fit on face
    fltr2 = cv2.resize(fltr2, (fltr_width,fltr_height), interpolation = cv2.INTER_AREA)
    mask = cv2.resize(original_mask2, (fltr_width,fltr_height), interpolation = cv2.INTER_AREA)
    mask_inv = cv2.resize(original_mask_inv2, (fltr_width,fltr_height), interpolation = cv2.INTER_AREA)
    
    #take ROI for filter from background that is equal to size of filter image
    roi = img[fltr_y1:fltr_y2, fltr_x1:fltr_x2]

    #original image in background (bg) where filter is not present
    roi_bg = cv2.bitwise_and(roi,roi,mask = mask)
    roi_fg = cv2.bitwise_and(fltr2,fltr2,mask=mask_inv)
    dst = cv2.add(roi_bg,roi_fg)

    #put back in original image
    img[fltr_y1:fltr_y2, fltr_x1:fltr_x2] = dst

cv2.imshow('Face Filter',img) #display image
cv2.waitKey(0) #wait until key is pressed to proceed
cv2.destroyAllWindows() #close all windows
