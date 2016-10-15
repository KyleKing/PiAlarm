# -*- coding: utf-8 -*-
import time
import subprocess
import config as cg

###########################
# Globals:
###########################

cg.quiet_logging(True)

# Electronic Pin Numbering Globals:
pin_blue = cg.get_pin('GPIO_Pins', 'pin_blue')
pin_red = cg.get_pin('GPIO_Pins', 'pin_red')
pin_green = cg.get_pin('GPIO_Pins', 'pin_green')
# Just an indicator light
pin_led = cg.get_pin('GPIO_Pins', 'pin_led')

steps = 10
# total_run_time = 60
total_run_time = 20
time_step = total_run_time / (6 * steps)  # 3 fades up, 3 down = 6

max_brightness = 0.5

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
    for i in range(steps):
        i = i + 1
        set_PWM(pin, max_brightness * (1 - 1 / (i + 1)))
        time.sleep(time_step)


def fade_down(pin):
    for i in range(steps):
        i = i + 1
        set_PWM(pin, max_brightness / (i + 1))
        time.sleep(time_step)


def all_off():
    cg.send('\nDeactivating SOME PWM pins')
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


# # Use to test the above module:
# fade_RGB_Strip()
