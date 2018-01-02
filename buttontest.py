#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import os
import datetime

print('Raspberry Pi Button Test ')
print('Copyright Ben Cobley 2018')

GPIO.setmode(GPIO.BCM)

GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.OUT)  # Button LED 
GPIO.output(21, GPIO.LOW)
GPIO.setup(18, GPIO.OUT)  # Flash LED 
GPIO.output(18, GPIO.HIGH)

flash_on = True
flash_button_count = 0
prev_pressed = False

print('Initialisation success')

try:
    print('True loop started')
    while True:
        shutter_button = GPIO.input(15)
        flash_button = GPIO.input(24)
        
        if shutter_button == False:
            print('Taking picture')
            time.sleep(0.8)
            flash_button_count = 0

        elif flash_button == False:
            print('yes')
            flash_button_count += 1
            if prev_pressed is True and flash_button_count >=8:
                print('Initiating shutdown')
            else:
                prev_pressed = True
            time.sleep(0.2)
            
        elif prev_pressed is True: #and flash button not pressed
            print('Switching flash')
            time.sleep(0.2)
            flash_button_count = 0
            prev_pressed = False

        else:
            flash_button_count = 0
            prev_pressed = False
        time.sleep(0.2)

except KeyboardInterrupt:
    GPIO.output(21, GPIO.LOW)
    GPIO.output(18, GPIO.LOW)
    GPIO.cleanup()
    quit()
