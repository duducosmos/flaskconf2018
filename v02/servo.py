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

import time

import pigpio

class Servo(object):
    def __init__(self, servo):
        self.servo = servo
        self.MIN_PWD = 500
        self.MAX_PWD = 2500
        self.pi = pigpio.pi()
        
    def _angles(self, angle):
        a = (self.MAX_PWD - self.MIN_PWD) / 180.0
        y = a * angle + self.MIN_PWD
        return int(y)
    
    def move_angle(self, angle):
        pw = self._angles(angle)
        self.pi.set_servo_pulsewidth(self.servo, pw)

    def stop(self):
        self.pi.stop()