# -*- coding: utf-8 -*-
import sys
import subprocess
import RPi.GPIO as GPIO
import time
# import config as cg


###########################
# Accept STDIN
###########################


# # simple JSON echo scripts

# line = ' '
# while line:
#     # Parse STDIN
#     line = sys.stdin.readline().strip().lower()

# for line in sys.stdin:
#     # print line[:-1]
#     log_to_web_app(line[:-1])

# TODO: Could be set with stdin in later version:
stages = [1, 2, 3, 4]


###########################
# Globals:
###########################


# For debugging purposes:
conv_min = 60
time_step = 1

# Electronic Pin Numbering Globals:
pin_shaker = 23
pin_buzzer = 18
pin_led = 17
pin_button = 24

# Other:
alarm_on = True
alarm_time = 0
next_stage_delay = 0
shaker_interval = 2
buzzer_freq = 0
led_color = 0
shaker_val = 0
buzzer_val = 0


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
    cmd = "echo " + str(pin_num) + "=" + str(percent)
    status = subprocess.call(cmd + " > /dev/pi-blaster", shell=True)
    return status

    # echo 23=1 > /dev/pi-blaster
    # echo 23=0 > /dev/pi-blaster


def alarm_deactivate(pin_num):
    """Button callback on rising edge"""
    global pin_button, pin_shaker, pin_led, alarm_on
    if GPIO.input(pin_num):
        print 'Deactivating Alarm'
        sys.stdout.flush()
        alarm_on = False
        set_PWM(pin_shaker, 0)
        set_PWM(pin_buzzer, 0)
        set_PWM(pin_led, 0)


def gen_button_cb(pin_num):
    """Button callback on rising edge:
       ex: GPIO.add_event_detect(pin_button, GPIO.BOTH,
                                 callback=gen_button_cb)"""
    if GPIO.input(pin_num):
        print "Triggered on a rising edge from pin: " + str(pin_num)
        sys.stdout.flush()
    else:
        print "Triggered on a falling edge from pin: " + str(pin_num)
        sys.stdout.flush()


def all_off():
    global led_color, shaker_val, buzzer_val
    if shaker_val > 0:
        shaker_val = 0
    if buzzer_val > 0:
        buzzer_val = 0
    set_PWM(pin_shaker, 0)
    set_PWM(pin_buzzer, 0)
    set_PWM(pin_led, 0)


def set_globals(*argv):
    global alarm_time, shaker_interval, buzzer_freq
    global led_color, next_stage_delay, shaker_val
    global buzzer_val
    alarm_time = argv[0]
    next_stage_delay = argv[1]
    shaker_interval = argv[2]
    buzzer_freq = argv[3]
    led_color = argv[4]
    shaker_val = argv[5]
    buzzer_val = argv[6]


###########################
# Alarm logic!
###########################

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_button, GPIO.IN)
GPIO.add_event_detect(pin_button, GPIO.RISING, callback=alarm_deactivate)
# Implemented hardware bouncetime with 0.1uf capacitor, so use ^
# GPIO.add_event_detect(pin_button, GPIO.RISING, callback=alarm_deactivate,
#                       bouncetime=300)

for stage in stages:
    print '\nStarting Stage: ' + str(stage)
    sys.stdout.flush()

    # # Testing Settings:
    # set_globals(1, 1.5, 3, 0.5, 1, 1, 0.8)

    if stage == 1:
        # set_globals(2, 3, -1, -1, 1, -1, -1)
        set_globals(1.5, 2, -1, -1, 1, -1, -1)
    elif stage == 2:
        # set_globals(1, 2, 10, 0.2, 0.2, -1, 1)
        set_globals(1.5, 2, 10, 0.2, 0.2, -1, 1)
    elif stage == 3:
        # set_globals(1, 2, 4, 0.5, 0.7, 1, 1)
        set_globals(1.5, 2, 4, 0.5, 0.7, 1, 1)
    elif stage == 4:
        # set_globals(5, 6, 1, 0.7, 1, 1, 1)
        set_globals(1.5, 2, 1, 0.7, 1, 1, 1)

    # # FIXME: WILL NOT FIX: TODO: What condition to keep alarm going?
    # alarm_on = True
    # Actually finish alarm:
    # sys.exit()

    # Loop-specific variables:
    all_off()
    start = time.clock()
    lasts = [0, 0, 0]
    cur_time = 0

    if alarm_on is False:
        print "Alarm is in off state and stage: " + str(stage) + " is skipped"
        sys.stdout.flush()

    while cur_time < alarm_time * conv_min and alarm_on:
        if shaker_val >= 0:
            # Determine Shaker Status:
            if (cur_time % (shaker_interval * 2)) <= shaker_interval:
                print '+ * (Alarm = ' + str(cur_time) + ') shaker modulo: ' + \
                    str(cur_time % (shaker_interval * 2))
                sys.stdout.flush()
                shaker_val = 1
            else:
                shaker_val = 0
            if shaker_val != lasts[0]:
                print '+   (Alarm = ' + str(cur_time) + \
                    ') Turning Shaker to: ' + \
                    str(shaker_val)
                sys.stdout.flush()
                set_PWM(pin_shaker, shaker_val)

        # Set Buzzer on alternating cycle (on time step):
        if buzzer_val >= 0 and (cur_time % 5) == 0:
            # print '* (Alarm = ' + str(cur_time) + \
            #     ') Checking last buzzer status'
            if buzzer_val == 0:
                print '> * (Alarm = ' + str(cur_time) + ') Turning Buzzer on!'
                sys.stdout.flush()
                buzzer_val = buzzer_freq
                set_PWM(pin_buzzer, buzzer_freq)
            else:
                print '>   (Alarm = ' + str(cur_time) + ') Turning Buzzer off!'
                sys.stdout.flush()
                buzzer_val = 0
                set_PWM(pin_buzzer, 0)

        # Set LED Strip a certain color:
        if led_color != lasts[2]:
            print '() (Alarm = ' + str(cur_time) + ') Turning Led to: ' + \
                str(led_color)
            sys.stdout.flush()
            set_PWM(pin_led, led_color)

        # Prep for next loop:
        # print 'Alarm = ' + str(cur_time)
        sys.stdout.flush()
        time.sleep(time_step)
        lasts = [shaker_val, buzzer_val, led_color]
        cur_time = cur_time + time_step

    # Turn all off and wait for next alarm to begin:
    all_off()
    net_sleep = (next_stage_delay * conv_min) - (time.clock() - start)
    print 'Sleeping for ' + str(round(net_sleep)) + \
        ' seconds before stage: ' + str(stage + 1) + \
        ' (' + str(next_stage_delay) + ' min)'
    sys.stdout.flush()
    time.sleep(net_sleep)

# Cleanup GPIO Pins:
all_off()
GPIO.remove_event_detect(pin_button)

print "\nAlarm Cycles Finished\n"
sys.stdout.flush()

# !! NOTE: $echo "release 23" > /dev/pi-blaster
GPIO.cleanup()
