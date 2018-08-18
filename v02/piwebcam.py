#!/usr/bin/env python3
"""
picam: Face Detection Using webcam on Raspberry pi 
with python-opencv

;-------------------------------------------------------------------------------
; Developed by: Eduardo S. Pereira
; version: 0.0.1
; e-mail: pereira.somoza@gmail.com
; date: 26/05/2018
;
; Copyright 2018 Eduardo S. Pereira
;
; Licensed under the Apache License, Version 2.0 (the "License");
; you may not use this file except in compliance with the License.
; You may obtain a copy of the License at
;
; http://www.apache.org/licenses/LICENSE-2.0
;
; Unless required by applicable law or agreed to in writing, software
; distributed under the License is distributed on an "AS IS" BASIS,
; WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
; See the License for the specific language governing permissions and
; limitations under the License.
;-------------------------------------------------------------------------------
"""

import cv2
from threading import Thread 

class PiWebcam(Thread):
    '''
    Capture webcam images using Python-Opencv.
    The webcam can run as thread.

    '''
    def __init__(self, width=None, height=None, 
                 window_name="webcam", show_window=False):

        Thread.__init__(self)

        self._cam = cv2.VideoCapture(0)

        if (self._cam.isOpened() == False): 
            print("Unable to read camera feed")
                
        

        if width is not None:
            self._cam.set(3, width)
            self.width = width
        else:
            self.width = int(self._cam.get(3))

        if height is not None:
            self._cam.set(4, height)
            self.height = height
        else:
            self.height = int(self._cam.get(4))

        self._image = None
        self._raw_image = None
        self._ret = None
        self._stopCam = False
        self._cam_window = None
        self._window_name = window_name
        self._showwindow = show_window

        self._rectangles = []
        self._lines = []
        self._countours = []
    
    def set_width(self, width):
        self.width = width
        self._cam.set(3, self.width)

    def set_height(self, height):
        self.height = height
        self._cam.set(4, self.height)

    def get_width(self):
        return self.width
        
    def get_height(self):
        return self.height

    def set_showwindow(self, show):
            self._showwindow = show
        
    def cam_window(self):
        if self._cam_window is None:
            self._cam_window = cv2.namedWindow(self._window_name, 
                                                cv2.WINDOW_AUTOSIZE)
            if self._image is not None:
                cv2.imshow(self._window_name, self._image)

        #Tecla esc para sair
        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            self.start_stop()
            

    def run(self):
        while True:	
            	

            self._ret, self._image = self._cam.read()
            if self._image is not None:
                self._raw_image = self._image.copy()
            else:
                self._raw_image = None
            self._draw_rects()
            self._draw_countors()

            for line in self._lines:
                for i in range(len(line) - 1):
                    
                    if len(line) > 1:
                        p0, p1 = None, None
                        try:
                            p0, p1 = line[i], line[i + 1]
                        except:
                            pass
                        if p0 is not None:
                            self._draw_line(p0, p1) 
                     

            if self._showwindow is True:	
                self.cam_window()
            
            if self._stopCam is True:
                break

    def _draw_countors(self):
        if self._image is not None:
            cv2.drawContours(self._image, self._countours, -1, (0,255,0), 3)

    def draw_countors(self, countours):
        self._countours = countours

    def _draw_rects(self):
        if self._image is not None:
            for (x, y, w, h, rgb, linewidth) in self._rectangles:
                cv2.rectangle(self._image, (x, y), (x + w, y + h),
                              rgb, linewidth)

    def _draw_line(self, point0, point1, rbg=(255,0,0), thickness=5):
        if self._image is not None:            
            cv2.line(self._image ,point0, point1,rbg,thickness)

    def draw_line(self, lines):
        self._lines = lines
        
            

    def draw_rectangles(self, rectangles):
        """
        Draw a list of rectangles.
        Input rectangles:
            List of Rectangles. 
            The rectangle element is of type
            (x,y,width, height, rgb, linewidth)
        """
        self._rectangles = rectangles
                
    def is_running(self):
        return not self._stopCam
                
    def start_stop(self):
        self._stopCam = True if self._stopCam is False else False
        
    def get_image(self):
        return self._raw_image
        
    def get_gray(self):
        if self._image is not None:
            return cv2.cvtColor(self._raw_image, cv2.COLOR_BGR2GRAY)
            
        
    def set_image(self, image):
        self._image = image
  
