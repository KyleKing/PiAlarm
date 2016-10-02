# -*- coding: utf-8 -*-
import time
import subprocess
import config as cg

###########################
# Globals:
###########################

debug = False
# debug = True
cg.quiet_logging(debug)

# Electronic Pin Numbering Globals:
pin_blue = 21
pin_red = 27
pin_green = 22

###########################
# Functions and Stuff
###########################


def set_PWM(pin_num, percent):
    """Run PWM commands through Pi-Blaster"""
    # echo "22=0" > /dev/pi-blaster
    cmd = 'echo "' + str(pin_num) + "=" + str(percent)
    cg.send(cmd + '" > /dev/pi-blaster')
    subprocess.call(cmd + '" > /dev/pi-blaster', shell=True)


def fade_up(pin):
    for i in range(10):
        i = i + 1
        set_PWM(pin, 0.1 - 0.1 / (i + 1))
        time.sleep(0.1)


def fade_down(pin):
    for i in range(10):
        i = i + 1
        set_PWM(pin, 0.1 / (i + 1))
        time.sleep(0.1)


def all_off():
    cg.send('\nDeactivating all PWM pins')
    set_PWM(pin_red, 0)
    set_PWM(pin_blue, 0)
    set_PWM(pin_green, 0)


def fade_RGB_Strip():
    all_off()

    set_PWM(pin_red, 0.1)

    fade_up(pin_green)
    fade_down(pin_red)
    fade_up(pin_blue)
    fade_down(pin_green)
    fade_up(pin_red)
    fade_down(pin_blue)

    all_off()
