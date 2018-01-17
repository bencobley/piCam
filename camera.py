#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import os
import datetime

print('Raspberry Pi Flash Test ')
print('Copyright Ben Cobley 2018')

GPIO.setmode(GPIO.BCM)

GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.OUT)  # Flash LED 
GPIO.output(21, GPIO.LOW)
GPIO.setup(18, GPIO.OUT)  # Button LED 
GPIO.output(18, GPIO.HIGH)

flash_on = True
flash_button_count = 0
flash_prev_pressed = False
shutter_prev_pressed = False
camera_pause = "500"

def button_blink(n, flash_delay):
    for repeats in range(n):
        GPIO.output(18, GPIO.LOW)
        time.sleep(flash_delay)
        GPIO.output(18, GPIO.HIGH)
        time.sleep(flash_delay)


def button_LED_on():
    GPIO.output(18, GPIO.HIGH)


def button_LED_off():
    GPIO.output(18, GPIO.LOW)

    
def switch_flash_on():
    if flash_on:
        GPIO.output(21, GPIO.HIGH)
    

def switch_flash_off():
    GPIO.output(21, GPIO.LOW)
    
    
def get_filename():
    now = datetime.datetime.now()
    time_string = now.strftime("%m%d_%H%M%S")
    file_name = "CC_" + time_string + ".jpg"
    return file_name

button_blink(2, 0.25)

try:
    while True:
        shutter_button = GPIO.input(15)
        flash_button = GPIO.input(24)
        button_LED_on()
        
        if shutter_button == False:
            if shutter_prev_pressed == False:
                button_LED_off()
                switch_flash_on()
                image_name = get_filename()
                print(image_name)
                command = "sudo raspistill -o " + image_name + " -q 100 -t " + camera_pause
                os.system(command)
                time.sleep(1)
                switch_flash_off()
                button_LED_on()
            shutter_prev_pressed = True

        elif flash_button == False:
            if flash_prev_pressed == True and flash_button_count >=8:
                os.system("sudo shutdown -h now")
                button_blink(60, 0.5)
            else:
                flash_prev_pressed = True
            flash_button_count += 1
            time.sleep(0.2)
            
        elif flash_prev_pressed == True: #and flash button not pressed by definition
            if flash_on:
                flash_on = False
                button_blink(1, 0.5)
            else:
                flash_on = True
                button_blink(2, 0.25)
            flash_button_count = 0
            flash_prev_pressed = False

        else:
            flash_button_count = 0
            flash_prev_pressed = False
            shutter_prev_pressed = False
        time.sleep(0.2)

except KeyboardInterrupt:
    GPIO.output(21, GPIO.LOW)
    GPIO.output(18, GPIO.LOW)
    GPIO.cleanup()
    quit()

