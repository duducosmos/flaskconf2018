#!/usr/bin/env python3

"""
Developed by: Eduardo S. Pereira
version: 0.0.1
e-mail: pereira.somoza@gmail.com
date: 26/05/2018

Copyright 2018 Eduardo S. Pereira

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


import cv2

def facedetection(gray, facemodel="./static/models/haarcascade_frontalface_default.xml"):
    '''
    '''
    face_c = cv2.CascadeClassifier(facemodel)
    retcs = face_c.detectMultiScale(gray, scaleFactor=1.3,
	                                minNeighbors=10, minSize=(75, 75))
    return retcs
