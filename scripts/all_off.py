# -*- coding: utf-8 -*-
import sys
import subprocess
import RPi.GPIO as GPIO
import config as cg


###########################
# Globals:
###########################


alarm_on = True
cg.quiet_logging(True)

# Electronic Pin Numbering Globals:
pin_shaker = 23
pin_buzzer = 18
pin_button = 24
pin_blue = 21
pin_red = 27
pin_green = 22

# Just an indicator light
pin_led = 17


###########################
# Functions and Stuff
###########################


def set_PWM(pin_num, percent):
    """Run PWM commands through Pi-Blaster"""
    # echo "22=0" > /dev/pi-blaster
    cmd = 'echo "' + str(pin_num) + "=" + str(percent)
    cg.send(cmd + '" > /dev/pi-blaster')
    return subprocess.call(cmd + '" > /dev/pi-blaster', shell=True)


def all_off():
    cg.send('\nDeactivating all PWM pins')
    set_PWM(pin_shaker, 1)
    set_PWM(pin_buzzer, 0)
    set_PWM(pin_led, 0)
    set_PWM(pin_red, 0)
    set_PWM(pin_blue, 0)
    set_PWM(pin_green, 0)


###########################
# Alarm logic!
###########################


GPIO.setmode(GPIO.BCM)
all_off()

print "\nFinished turning all pins to off state (all_off)\n"
sys.stdout.flush()
