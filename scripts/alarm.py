# -*- coding: utf-8 -*-
import sys
import time
import subprocess
import RPi.GPIO as GPIO
import config as cg
import fade

###########################
# Globals:
###########################

alarm_on = True
debug = False
# debug = True
cg.quiet_logging(True)
# cg.quiet_logging(debug)

# Pi-Blaster Pins
# --gpio 4,17,18,27,21,22,23,24,25

# Electronic Pin Numbering Globals:
pin_shaker = 23
pin_buzzer = 18
pin_button = 20
pin_blue = 21
pin_red = 27
pin_green = 22

# Just an indicator light
pin_led = 17

###########################
# Functions and Stuff
###########################


def log_to_web_app(counter):
    """Prep a string to send to the controlling node application"""
    log_str = 'Completed Step #{0}'
    print log_str.format(counter)
    sys.stdout.flush()


def set_PWM(pin_num, percent):
    """Run PWM commands through Pi-Blaster"""
    # echo "22=0" > /dev/pi-blaster
    cmd = 'echo "' + str(pin_num) + "=" + str(percent)
    cg.send(cmd + '" > /dev/pi-blaster')
    return subprocess.call(cmd + '" > /dev/pi-blaster', shell=True)


def release_PWM(pin_num):
    """Run PWM commands through Pi-Blaster"""
    # echo "release 22" > /dev/pi-blaster
    cmd = 'echo "release ' + str(pin_num)
    cg.send(cmd + '" > /dev/pi-blaster')
    return subprocess.call(cmd + '" > /dev/pi-blaster', shell=True)


def alarm_deactivate(pin_num):
    """Button callback on rising edge"""
    global alarm_on
    print '\nAlarm Deactivate Script called with: ' + str(GPIO.input(pin_num))
    if GPIO.input(pin_num):
        cg.send('Deactivating Alarm')
        alarm_on = False


def gen_button_cb(pin_num):
    """Button callback on rising edge:
       ex: GPIO.add_event_detect(pin_button, GPIO.BOTH,
                                 callback=gen_button_cb)"""
    if GPIO.input(pin_num):
        cg.send("Triggered on a rising edge from pin: " + str(pin_num))
    else:
        cg.send("Triggered on a falling edge from pin: " + str(pin_num))


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

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_button, GPIO.IN)
GPIO.add_event_detect(pin_button, GPIO.RISING, callback=alarm_deactivate,
                      bouncetime=300)
# Implemented hardware bouncetime with 0.1uf capacitor, so use this instead:
# GPIO.add_event_detect(pin_button, GPIO.RISING, callback=alarm_deactivate)


for stage in [1, 2, 3]:
    all_off()
    if debug:
        alarm_stage_time = [0, 10, 10, 10]
    else:
        alarm_stage_time = [0, 90, 180, 500]
    cg.send('\nStarting Stage: ' + str(stage) + ' for ' +
            str(alarm_stage_time[stage]) + ' seconds')

    current_time = 0
    if alarm_on:
        # Stage 1 - Blue LED for 1 minute
        if stage == 1:
            cg.send('Configuring Stage 1')
            set_PWM(pin_green, 0.2)
            set_PWM(pin_red, 0.2)
            set_PWM(pin_led, 1)
        # Stage 2 - Purple LED and Bed Shaker for 2 minutes
        if stage == 2:
            cg.send('Configuring Stage 2')
            set_PWM(pin_blue, 0.5)
            set_PWM(pin_red, 0.5)
            set_PWM(pin_buzzer, 0.1)
            set_PWM(pin_led, 0.2)
        # Stage 3 - FADE LED Strip, Bed Shaker, and Buzzer for 5 minutes
        if stage == 3:
            cg.send('Configuring Stage 3')
            fade.fade_RGB_Strip()
            set_PWM(pin_shaker, 0)
            set_PWM(pin_buzzer, 0.5)
            set_PWM(pin_led, 1)
        # Stage 4 - WELL FADE EVERYTHING?
        if stage == 4:
            fade.fade_RGB_Strip()

        while alarm_on and current_time < alarm_stage_time[stage]:
            current_time += 1
            time.sleep(1)
        current_time = 0

    # if shaker_val >= 0:
    #     # Determine Shaker Status:
    #     if (cur_time % (shaker_interval * 2)) <= shaker_interval:
    #         cg.send('+ * (Alarm = ' + str(cur_time) +
    #                 ') shaker modulo: ' +
    #                 str(cur_time % (shaker_interval * 2)))
    #         shaker_val = 1
    #     else:
    #         shaker_val = 0
    #     if shaker_val != lasts[0]:
    #         cg.send('+   (Alarm = ' + str(cur_time) +
    #                 ') Turning Shaker to: ' +
    #                 str(shaker_val))
    #         set_PWM(pin_shaker, shaker_val)

# Cleanup GPIO Pins:
all_off()
GPIO.remove_event_detect(pin_button)

cg.send("\nAlarm Cycles Finished\n")

# release_PWM(pin_shaker)
# release_PWM(pin_buzzer)
# release_PWM(pin_button)
# release_PWM(pin_led)
# release_PWM(pin_blue)
# release_PWM(pin_red)
# release_PWM(pin_green)

GPIO.cleanup()

# # Then stop pi-blaster for good measure:
# stopPiB = "sudo kill $(ps aux | grep [b]laster | awk '{print $2}')"
# subprocess.call(stopPiB, shell=True)
