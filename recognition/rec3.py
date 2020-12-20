import cv2
import numpy as np 

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
        #img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

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
        fltr = cv2.resize(fltr, (fltr_width,fltr_height), interpolation = cv2.INTER_AREA)
        mask = cv2.resize(original_mask, (fltr_width,fltr_height), interpolation = cv2.INTER_AREA)
        mask_inv = cv2.resize(original_mask_inv, (fltr_width,fltr_height), interpolation = cv2.INTER_AREA)

        #take ROI for fltr from background that is equal to size of fltr image
        roi = img[fltr_y1:fltr_y2, fltr_x1:fltr_x2]

        #original image in background (bg) where fltr is not
        roi_bg = cv2.bitwise_and(roi,roi,mask = mask)
        roi_fg = cv2.bitwise_and(fltr,fltr,mask=mask_inv)
        dst = cv2.add(roi_bg,roi_fg)

        #put back in original image
        img[fltr_y1:fltr_y2, fltr_x1:fltr_x2] = dst

        break
        
    #display image
    cv2.imshow('img',img) 

    #if user pressed 'q' break
    if cv2.waitKey(0) == ord('q'): # 
        break;

cap.release() #turn off camera 
cv2.destroyAllWindows() #close all windows
