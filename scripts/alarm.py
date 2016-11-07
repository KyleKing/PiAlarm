# -*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO
import config as cg
# import fade

###########################
# Globals:
###########################

alarm_on = True
debug = False
cg.quiet_logging(debug)

# Electronic Pin Numbering Globals:
pin_button = cg.get_pin('Input_Pins', 'pin_button')
pin_buzzer = cg.get_pin('GPIO_Pins', 'pin_buzzer')
pin_shaker = cg.get_pin('GPIO_Pins', 'pin_shaker')
pin_blue = cg.get_pin('GPIO_Pins', 'pin_blue')
pin_red = cg.get_pin('GPIO_Pins', 'pin_red')
pin_green = cg.get_pin('GPIO_Pins', 'pin_green')

# Just an indicator light
# pin_led = cg.get_pin('GPIO_Pins', 'pin_led')

###########################
# Functions and Stuff
###########################


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
    cg.set_PWM(pin_shaker, 1)
    cg.set_PWM(pin_buzzer, 0)
    # cg.set_PWM(pin_led, 0)
    cg.set_PWM(pin_red, 0)
    cg.set_PWM(pin_blue, 0)
    cg.set_PWM(pin_green, 0)


def check_status():
    """Returns True, if alarm is to continue running, else is False"""
    stat = cg.get_pin('Alarm_Status', 'running', "./scripts/pins.ini", True)
    return 'true' in stat.lower()


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

if debug:
    alarm_stage_time = [0, 10, 10, 10]
else:
    alarm_stage_time = [0, 90, 180, 60]
    cg.ifttt('PiAlarm_StartAlarm')

for stage in [1, 2, 3]:
    all_off()
    cg.send('\nStarting Stage: ' + str(stage) + ' for ' +
            str(alarm_stage_time[stage]) + ' seconds')

    current_time = 0
    if alarm_on:
        # Stage 1 - Blue LED for 1 minute
        if stage == 1:
            cg.send('Configuring Stage 1')
            cg.set_PWM(pin_green, 0.2)
            cg.set_PWM(pin_red, 0.2)
            # cg.set_PWM(pin_led, 1)
        # Stage 2 - Purple LED and Bed Shaker for 2 minutes
        if stage == 2:
            cg.send('Configuring Stage 2')
            cg.set_PWM(pin_blue, 0.5)
            cg.set_PWM(pin_red, 0.5)
            cg.set_PWM(pin_buzzer, 0.1)
            # cg.set_PWM(pin_led, 0.2)
        # Stage 3 - FADE LED Strip, Bed Shaker, and Buzzer for 5 minutes
        if stage == 3:
            cg.send('Configuring Stage 3')
            # THIS IS THE PROBLEM:
            # fade.fade_RGB_Strip()
            cg.set_PWM(pin_blue, 0.5)
            cg.set_PWM(pin_red, 0.5)
            cg.set_PWM(pin_shaker, 0)
            cg.set_PWM(pin_buzzer, 0.5)
            # cg.set_PWM(pin_led, 1)

        # Run alarm and check for button interrupt:
        while (alarm_on and current_time < alarm_stage_time[stage] and
               check_status()):
            current_time += 1
            time.sleep(1)

        # Prep for the next loop:
        if stage == 3 & alarm_on:
            cg.send('Looping back through Stage 3')
            all_off()
            time.sleep(10)
        current_time = 0
    cg.log_to_web_app(stage)

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
    #         cg.set_PWM(pin_shaker, shaker_val)

# Cleanup GPIO Pins:
all_off()
GPIO.remove_event_detect(pin_button)

cg.send("\nAlarm Cycles Finished\n")

# release_PWM(pin_shaker)
# release_PWM(pin_buzzer)
# release_PWM(pin_button)
# # release_PWM(pin_led)
# release_PWM(pin_blue)
# release_PWM(pin_red)
# release_PWM(pin_green)

GPIO.cleanup()

# # Then stop pi-blaster for good measure:
# stopPiB = "sudo kill $(ps aux | grep [b]laster | awk '{print $2}')"
# subprocess.call(stopPiB, shell=True)
