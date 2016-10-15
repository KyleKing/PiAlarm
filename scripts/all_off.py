# -*- coding: utf-8 -*-
import sys
import subprocess
import RPi.GPIO as GPIO
import config as cg


###########################
# Globals:
###########################


alarm_on = True
cg.quiet_logging(False)

# Standard pins: --gpio 4,17,18,27,21,22,23,24,25
# New pins: --gpio 4,17,18,27,21,22,23,24,25

# Electronic Pin Numbering Globals:
# pin_button = 20  # prev: 20
pin_button = cg.get_pin('Input_Pins', 'pin_button')
# pin_buzzer = 16  # prev: 18
pin_buzzer = cg.get_pin('GPIO_Pins', 'pin_buzzer')
# pin_shaker = 21  # prev: 23
pin_shaker = cg.get_pin('GPIO_Pins', 'pin_shaker')
# pin_blue = 5  # prev: 21
pin_blue = cg.get_pin('GPIO_Pins', 'pin_blue')
# pin_red = 6  # prev: 27
pin_red = cg.get_pin('GPIO_Pins', 'pin_red')
# pin_green = 13  # prev: 22
pin_green = cg.get_pin('GPIO_Pins', 'pin_green')

# Just an indicator light
# pin_led = 19  # prev: 17
pin_led = cg.get_pin('GPIO_Pins', 'pin_led')

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
