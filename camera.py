#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import os
import datetime

print('Raspberry Pi Cardboard Camera ')
print('Copyright Ben Cobley 2018')

GPIO.setmode(GPIO.BCM)

GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, GPIO.LOW)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.HIGH)

shutter_button = GPIO.input(15)
flash_button = GPIO.input(23)

flash_on = True
flash_button_count = 0
prev_pressed = False

camera_pause = "500"


def button_flash(n, flash_delay):
    for repeats in range(n):
        GPIO.output(21, GPIO.LOW)
        time.sleep(flash_delay)
        GPIO.output(21, GPIO.HIGH)
        time.sleep(flash_delay)


def button_on():
    GPIO.output(21, GPIO.HIGH)


def button_off():
    GPIO.output(21, GPIO.LOW)


def get_filename():
    now = datetime.datetime.now()
    time_string = now.strftime("%Y-%m-%d_%H:%M:%S")
    print("Request received" + time_string)
    file_name = "photo-" + time_string + ".jpg"
    return file_name


print('Initialisation success')
button_flash(5, 0.25)

try:
    while True:
        print('True loop started')
        button_on()

        if shutter_button is False:
            print('Taking picture')
            button_off()
            if flash_on:
                GPIO.output(21, GPIO.HIGH)
            image_name = get_filename()
            command = "sudo raspistill -o " + image_name + " -q 100 -t " + camera_pause
            os.system(command)
            GPIO.output(21, GPIO.LOW)
            flash_button_count = 0

        elif flash_button is False:
            flash_button_count += 1
            if prev_pressed is True and flash_button_count >= 12:
                print('Initiating shutdown')
                os.system("sudo shutdown -h now")
                button_flash(60, 0.5)
            elif prev_pressed is False:
                print('Switching flash')
                if flash_on:
                    flash_on = False
                    button_flash(1, 0.5)
                else:
                    flash_on = True
                    button_flash(2, 0.25)
            else:
                prev_pressed = True

        else:
            flash_button_count = 0
            prev_pressed = False
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.output(21, GPIO.LOW)
    GPIO.output(18, GPIO.LOW)
    GPIO.cleanup()
    quit()


