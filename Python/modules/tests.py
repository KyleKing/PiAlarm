"""Run tests on Python modules."""

import os
from time import sleep

import all_off
import config as cg
import fade
import lcd
import weather
from context import IO


#
# Utilities
#


def ask(question):
    """Prompt user for input then abort if failed."""
    response = raw_input('\n ? {} (Y/N)'.format(question))
    if 'n' in response.strip().lower():
        raise Exception('User replied No, aborting')


def test_passed(correct, output):
    """Automate some of manual testing."""
    if correct == output:
        return True
    elif type(output) is not bool and correct in output:
        return True
    raise ValueError('Failed test > E: {} vs. A: {}'.format(correct, output))


def gen_button_cb(pin_num):
    """For testing the callback function."""
    if IO.input(pin_num):
        print 'Triggered on a rising edge from pin: {}'.format(pin_num)
        cg.send('Triggered on a rising edge from pin: {}'.format(pin_num))
    else:
        print 'Triggered on a falling edge from pin: {}'.format(pin_num)
        cg.send('Triggered on a falling edge from pin: {}'.format(pin_num))


#
# Actual Tests
#


def t_hw():
    """Hello World."""
    print 'Hey! This module is working!'


def t_weather():
    """Output the commute-weather format."""
    print weather.hourly(quiet=False)


def test_off_btn():
    """Test the OFF button for the alarm."""
    print 'Checking that the alarm off button works'
    off_button = cg.get_pin('Input_Pins', 'off_button')
    IO.setwarnings(False)
    IO.setmode(IO.BCM)
    IO.setup(off_button, IO.IN)
    IO.add_event_detect(off_button, IO.BOTH, callback=gen_button_cb)
    sleep(5)

    print 'Checking that Pi-Blaster is booted'
    os.system('sudo python ./bootPiBlaster.py')
    print '** Getting started! Turning everything off **'
    all_off.deactivate()
    print ''


def toggle_status():
    """Test exit/enter status."""
    # Test the script called by the Node Application:
    print 'User home/away status currently is: {}'.format(cg.check_status())
    os.system('python alarm_status.py exit')
    pass_exit = test_passed(False, cg.check_status())
    print 'Set status to Away: {}'.format(pass_exit)
    ask('Is the away LED on?')

    os.system('python alarm_status.py enter')
    pass_enter = test_passed(True, cg.check_status())
    print 'Set status to Present: {}'.format(pass_enter)


def test_hardware():
    """Check each electrical component and check with operator."""
    print 'Fading the RGB Strip'
    fade.fade_RGB_Strip()
    ask('Did the RGB strip fade?')

    print 'Starting the 7-Segment Clock'
    os.system('python clock.py someargthat_preventsBGrun')
    ask('Does clock display the current time?')

    print 'Initializing the LCD display'
    lcd.Initialize()
    ask('Does the character display have some text?')


def button_tests():
    """Check buttons."""
    led_state = 1
    away_led = cg.get_pin('Alarm_Status', 'away_led')
    onoff_led = cg.get_pin('Reserved', 'onoff_led')

    def test_off_led(tmp):
        global led_state
        print 'test_off_led', led_state
        cg.set_PWM(away_led, led_state)
        led_state = 1 if led_state == 0 else 0

    def test_nf_led(tmp):
        global led_state
        print 'test_nf_led', led_state
        cg.set_PWM(onoff_led, led_state)
        led_state = 1 if led_state == 0 else 0

    IO.setwarnings(False)
    IO.setmode(IO.BCM)

    off_button = cg.get_pin('Input_Pins', 'off_button')
    IO.setup(off_button, IO.IN)
    IO.add_event_detect(off_button, IO.RISING, callback=test_off_led, bouncetime=300)
    print 'Did the OFF button work? (Press Key)'
    raw_input()
    IO.remove_event_detect(off_button)

    onoff_button = cg.get_pin('Reserved', 'onoff_button')
    IO.setup(onoff_button, IO.IN)
    IO.add_event_detect(onoff_button, IO.RISING, callback=test_nf_led, bouncetime=300)
    print 'Did the ON/OFF button work? (Press Key)'
    raw_input()
    IO.remove_event_detect(onoff_button)
