# -*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO

from modules import config as cg
from modules import fade


###########################
# Globals:
###########################

alarm_on = True
cg.quiet_logging(False)

# Electronic Pin Numbering Globals:
pin_button = cg.get_pin('Input_Pins', 'pin_button')
pin_buzzer = cg.get_pin('GPIO_Pins', 'pin_buzzer')
pin_shaker = cg.get_pin('GPIO_Pins', 'pin_shaker')
pin_blue = cg.get_pin('GPIO_Pins', 'pin_blue')
pin_red = cg.get_pin('GPIO_Pins', 'pin_red')
pin_green = cg.get_pin('GPIO_Pins', 'pin_green')

# alarm_stage_time = [0, 4, 8, 12 + 3]
alarm_stage_time = [0, 100, 80, 60]
step_size = 0.2

# Settings for fade_led_strip()
max_brightness = 0.6
fade_stage = 0
fade_stages = [pin_green, pin_red, pin_blue,
               pin_green, pin_red, pin_blue]
time_total = alarm_stage_time[3] / len(fade_stages)


###########################
# Functions and Stuff
###########################


def alarm_deactivate(pin_num):
    """Button callback on rising edge"""
    global alarm_on
    val = GPIO.input(pin_num)
    cg.send('Alarm Deactivate Script called with: {}'.format(val))
    if val:
        cg.send('Deactivating Alarm')
        alarm_on = False


def gen_button_cb(pin_num):
    """For testing the cb function"""
    if GPIO.input(pin_num):
        cg.send("Triggered on a rising edge from pin: " + str(pin_num))
    else:
        cg.send("Triggered on a falling edge from pin: " + str(pin_num))


def all_off():
    cg.send('\nDeactivating all PWM pins')
    cg.set_PWM(pin_shaker, 1)
    cg.set_PWM(pin_buzzer, 0)
    cg.set_PWM(pin_red, 0)
    cg.set_PWM(pin_blue, 0)
    cg.set_PWM(pin_green, 0)


def beep(counter):
    """Cycle through different low frequencies"""
    if counter % 2 == 0:
        cg.set_PWM(pin_buzzer, 0.2)
    elif counter % 2 == 1:
        cg.set_PWM(pin_buzzer, 0.0)


def fade_led_strip(counter):
    """Cycle the LED Strip through various colors"""
    global fade_stage
    time_step = (counter % time_total) + 1.0

    # Increment the LED value
    if fade_stage % 2 == 0:
        value = 1 - (1 / time_step)
    # Decrement the LED value
    elif fade_stage % 2 == 1:
        value = 1 / time_step

    # Update the Alarm Electronics
    if fade_stage < len(fade_stages):
        # cg.set_PWM(pin_buzzer, ((counter % 2) + 1.0) / 4)
        cg.set_PWM(fade_stages[fade_stage], max_brightness * value)
        if time_step == time_total:
            fade_stage += 1
    else:
        # cg.set_PWM(pin_buzzer, 0.5)
        fade.all_on(max_brightness)


###########################
# Alarm logic!
###########################


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_button, GPIO.IN)
GPIO.add_event_detect(pin_button, GPIO.RISING, callback=alarm_deactivate,
                      bouncetime=300)

user_home = cg.check_status()
if user_home:
    cg.ifttt('PiAlarm_SendText', {'value1': '** PiAlarm Started! **'})
    stage = 1
    stage3_rep_counter = 0

    while stage < 4 and stage3_rep_counter < 3 and user_home:
        all_off()
        cg.send('\nStarting Stage: {}'.format(stage) + ' for ' +
                str(alarm_stage_time[stage]) + ' seconds')

        current_time = 0
        # Stage 1 - Green LED Strip for 1 minute
        if stage == 1 and alarm_on:
            cg.send('Configuring Stage 1')
            cg.set_PWM(pin_green, 0.2)
            cg.set_PWM(pin_red, 0.2)
            cb = False
        # Stage 2 - Purple LED Strip and Buzzer
        if stage == 2 and alarm_on:
            cg.send('Configuring Stage 2')
            cg.set_PWM(pin_blue, 0.5)
            cg.set_PWM(pin_red, 0.5)
            # cg.set_PWM(pin_buzzer, 0.1)
            cb = beep
        # Stage 3 - LED Strip, Bed Shaker, and Buzzer
        if stage == 3 and alarm_on:
            cg.send('Configuring Stage 3')
            cg.set_PWM(pin_shaker, 0)
            cg.set_PWM(pin_buzzer, 0.5)
            cb = fade_led_strip

        # Run alarm and check for button interrupt:
        while alarm_on and current_time < alarm_stage_time[stage]:
            time.sleep(step_size)
            current_time += step_size
            if cb:
                cb(current_time)
        cg.send('Completed Step #{0}'.format(stage))

        # Prep for the next loop:
        if stage == 3 and alarm_on:
            all_off()
            cg.send('\nLooping back through Stage 3')
            time.sleep(5)
            fade_stage = 0
            stage3_rep_counter += 1
        else:
            stage += 1
        current_time = 0
        user_home = cg.check_status()

    cg.send("\nAlarm Cycles Finished\n")
    cg.ifttt('PiAlarm_SendText', {'value1': 'PiAlarm Completed'})

    # Cleanup tasks:
    all_off()
    GPIO.remove_event_detect(pin_button)
    GPIO.cleanup()

    # release_PWM(pin_shaker)
    # etc...
    # # Then stop pi-blaster for good measure:
    # stopPiB = "sudo kill $(ps aux | grep [b]laster | awk '{print $2}')"
    # subprocess.call(stopPiB, shell=True)

else:
    cg.ifttt('PiAlarm_SendText', {'value1': 'User away, no PiAlarm'})
