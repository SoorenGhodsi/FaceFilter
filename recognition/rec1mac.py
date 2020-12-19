import cv2
import numpy as np 
from matplotlib import pyplot as plt

#path to classifiers
# path = '/Users/Sooren/opt/anaconda3/envs/learn-env/share/opencv4/haarcascades/'

#get image classifiers
face_cascade = cv2.CascadeClassifier('haarcascade-xmls/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade-xmls/haarcascade_eye.xml')

#read image
img = cv2.imread('assets/people.jpg') 
if img is None:
    print("Check file path")

#convert to gray
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#detect faces
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

#for each face
for (x,y,w,h) in faces:
    #draw rectangle around face
    img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    #select face as region of interest 
    roi_g = gray[y:y+h,x:x+h]
    roi_c = img[y:y+h,x:x+h]
    #within region of interest find eyes
    eyes = eye_cascade.detectMultiScale(roi_g)
    #for each eye
    for (ex,ey,ew,eh) in eyes:
        #draw retangle around eye
        cv2.rectangle(roi_c, (ex,ey),(ex+ew,ey+eh),(0,255,0),2)
 
cv2.imshow('img', img) #shows image
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)
