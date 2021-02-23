#!/usr/bin/env python
# coding: utf-8


import cv2
import tensorflow as tf
import numpy as np


face_cascade = cv2.CascadeClassifier('face_mod.xml')
final_model=tf.keras.models.load_model("Aug_Model")



def image(path):
    img = cv2.imread(path)
    faces = face_cascade.detectMultiScale(img, 1.3,5)
    for (x,y,w,h) in faces:
        print("X : ",x)
        print("y" ,y)
        print("width",w)
        print("height",h)
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi = img[y:y+h, x:x+w]
        resized = cv2.resize(roi,(48,48))    
    resized = resized[:,:,1]
    resized = resized.reshape(1,48,48,1)
    emotion=np.argmax(final_model.predict(resized))
    return emotion  





