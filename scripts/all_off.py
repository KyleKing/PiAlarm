# -*- coding: utf-8 -*-
import sys
import subprocess
import RPi.GPIO as GPIO

###########################
# Globals:
###########################

# Electronic Pin Numbering Globals:
pin_shaker = 23
pin_buzzer = 18
pin_led = 17


###########################
# Functions and Stuff
###########################


def set_PWM(pin_num, percent):
    """Run PWM commands through Pi-Blaster"""
    cmd = "echo " + str(pin_num) + "=" + str(percent)
    status = subprocess.call(cmd + " > /dev/pi-blaster", shell=True)
    print "Called: " + cmd + " > /dev/pi-blaster"
    return status


def all_off():
    print set_PWM(pin_shaker, 0)
    print set_PWM(pin_buzzer, 0)
    print set_PWM(pin_led, 0)

###########################
# Alarm logic!
###########################


GPIO.setmode(GPIO.BCM)
all_off()

print "\nFinished turning all pins to off state (all_off)\n"
sys.stdout.flush()
