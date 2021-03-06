"""Alarm Script."""

import sys
import time

from . import config as cg
from . import all_off, fade, lcd
from .context import IO

# FIXME: Re-implement as a thread with an interrupt Exception

###########################
# Configuration:
###########################

# Electronic Pin Numbering Globals:
off_button = cg.get_pin('Input_Pins', 'off_button')
pin_buzzer = cg.get_pin('Haptics', 'pin_buzzer')
pin_shaker = cg.get_pin('Haptics', 'pin_shaker')
pin_blue = cg.get_pin('RGB_Strip', 'pin_blue')
pin_red = cg.get_pin('RGB_Strip', 'pin_red')
pin_green = cg.get_pin('RGB_Strip', 'pin_green')
# # TODO: Add second LED Strip
# pin_blue2 = cg.get_pin('RGB_Strip', 'pin_blue2')
# pin_red2 = cg.get_pin('RGB_Strip', 'pin_red2')
# pin_green2 = cg.get_pin('RGB_Strip', 'pin_green2')

# Allow shorter run time for testing with ANY argument
if len(sys.argv) > 1:
    # arg = cg.parse_argv(sys)
    alarm_stage_time = [0, 5, 10, 15]
else:
    alarm_stage_time = [30, 180, 80, 60]

step_size = 0.2
alarm_on = True
_running = False
cg.quiet_logging(False)

# Settings for fade_led_strip()
max_brightness = 0.6
last_beep, fade_stage = 0, 0
fade_stages = [pin_green, pin_red, pin_blue,
               pin_green, pin_red, pin_blue]
a_s_t = alarm_stage_time[3]
l_f_s = len(fade_stages)
if a_s_t < l_f_s:
    raise ValueError('a_s_t({}) not > len({})'.format(a_s_t, l_f_s))
time_total = a_s_t / l_f_s


###########################
# Functions and Stuff
###########################


def alarm_deactivate(pin_num):
    """Button callback on rising edge."""
    global alarm_on
    if IO.input(pin_num):
        cg.send('Deactivating Alarm on {}'.format(IO.input(pin_num)))
        alarm_on = False


def gen_button_cb(pin_num):
    """For testing the callback function."""
    if IO.input(pin_num):
        cg.send('Triggered on a rising edge from pin: {}'.format(pin_num))
    else:
        cg.send('Triggered on a falling edge from pin: {}'.format(pin_num))


def beep(counter):
    """Cycle through different low frequencies."""
    global last_beep
    if counter % 2 <= 1 and last_beep == 0:
        cg.set_pwm(pin_buzzer, 0.2)
        last_beep = 0.2
    elif counter % 2 > 1 and last_beep == 0.2:
        cg.set_pwm(pin_buzzer, 0.0)
        last_beep = 0


def fade_led_strip(counter):
    """Cycle the LED Strip through various colors."""
    global fade_stage
    if time_total < 0.1:
        time_step = 1
    else:
        time_step = (counter % time_total) + 1.0

    # Increment the LED value
    if fade_stage % 2 == 0:
        value = 1 - (1 / time_step)
    # Decrement the LED value
    elif fade_stage % 2 == 1:
        value = 1 / time_step

    # Update the Alarm Electronics
    if fade_stage < len(fade_stages):
        # cg.set_pwm(pin_buzzer, ((counter % 2) + 1.0) / 4)
        cg.set_pwm(fade_stages[fade_stage], max_brightness * value)
        if time_step == time_total:
            fade_stage += 1
    else:
        # cg.set_pwm(pin_buzzer, 0.5)
        fade.all_on(max_brightness)


###########################
# Alarm logic!
###########################


def stop():
    """Halt execution."""
    global _running
    _running = False
    cg.send('\nAlarm Cycles Finished\n')
    cg.ifttt('PiAlarm_SendText', {'value1': 'PiAlarm Completed'})

    # Cleanup tasks:
    all_off.deactivate()
    IO.remove_event_detect(off_button)
    #
    # IO.cleanup()  # Removed to avoid interference with clock
    #
    # release_pwm(pin_shaker)
    # etc...
    # # Then stop pi-blaster for good measure:
    # stopPiB = "sudo kill $(ps aux | grep [b]laster | awk '{print $2}')"
    # subprocess.call(stopPiB, shell=True)


def start(user_home):
    """Start alarm sequence."""
    global fade_stage, _running, alarm_on
    _running = True
    stage, stage3_rep_counter = 1, 0

    cg.send('Set IO mode and event detection')
    IO.setwarnings(False)
    IO.setmode(IO.BCM)
    IO.setup(off_button, IO.IN)
    IO.add_event_detect(off_button, IO.RISING, callback=alarm_deactivate, bouncetime=300)

    while stage < 4 and stage3_rep_counter < 3 and user_home:
        all_off.deactivate()
        cg.send('\nStarting Stage: {}'.format(stage) +
                ' for {} seconds'.format(alarm_stage_time[stage]))

        current_time = 0
        # Stage 1 - Green LED Strip for 1 minute
        if stage == 1 and alarm_on:
            cg.send('Configuring Stage 1')
            cg.set_pwm(pin_green, 0.2)
            cg.set_pwm(pin_red, 0.2)
            cb = False
        # Stage 2 - Purple LED Strip and Buzzer
        if stage == 2 and alarm_on:
            cg.send('Configuring Stage 2')
            cg.set_pwm(pin_blue, 0.5)
            cg.set_pwm(pin_red, 0.5)
            cg.set_pwm(pin_buzzer, 0.1)
            cb = beep
        # Stage 3 - LED Strip, Bed Shaker, and Buzzer
        if stage == 3 and alarm_on:
            cg.send('Configuring Stage 3')
            cg.set_pwm(pin_shaker, 1)
            cg.set_pwm(pin_buzzer, 0.5)
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
            all_off.deactivate()
            cg.send('\nLooping back through Stage 3')
            time.sleep(7)
            fade_stage = 0
            stage3_rep_counter += 1
        else:
            stage += 1
        current_time = 0
        user_home = cg.check_status()
        cg.send('Checking home (= {}) before next loop'.format(user_home))
    stop()


def run():
    """Check state and start alarm if ready."""
    global _running, alarm_on
    user_home = cg.check_status()
    alarm_on = True
    if _running:
        _err = 'ERROR: ALARM IS ALREADY RUNNING!'
        cg.send(_err)
        cg.ifttt('PiAlarm_SendText', {'value1': _err})
    elif user_home:
        lcd.brightness('alt')
        cg.ifttt('PiAlarm_SendText', {'value1': '** PiAlarm Started! **'})
        time.sleep(alarm_stage_time[0])  # let text alert go out
        start(cg.check_status())
    else:
        cg.ifttt('PiAlarm_SendText', {'value1': 'User away, no PiAlarm'})


if __name__ == '__main__':
    run()
