import os
import json
# import requests

import lcd
from modules import fade
from modules import all_off
from modules import config as cg


def ask(question):
    """Prompt user for input then abort if failed"""
    response = raw_input('\n ? {} (Y/N)'.format(question))
    if 'n' in response.strip().lower():
        raise Exception("User replied No, aborting")


def test_passed(correct, output):
    """Automate some of manual testing"""
    if (correct == output) or (correct in output):
        return True
    raise ValueError('Failed test > E: {} vs. A: {}'.format(correct, output))


if __name__ == '__main__':

    print '** Getting started! Turning everything off **'
    all_off.all_off()
    print 'Booting Pi-Blaster'
    os.system('sudo python ./bootPiBlaster.py')
    print ''

    #####################
    # Test exit/enter capabilities
    #####################

    with open('../secret.json') as secrets_file:
        secrets = json.load(secrets_file)
        key = secrets["maker"]
        ip = secrets["ip"]

    # Test the script called by the Node Application:
    print "User home/away status currently is: {}".format(cg.check_status())
    os.system('python alarm_status.py exit')
    pass_exit = test_passed(True, cg.check_status())
    print "Set status to Away: {}".format(pass_exit)
    ask('Is the away LED on?')

    os.system('python alarm_status.py enter')
    pass_enter = test_passed(True, cg.check_status())
    print "Set status to Present: {}".format(pass_enter)

    #####################
    # Test the hardware:
    #####################

    print 'Fading the RGB Strip'
    fade.fade_RGB_Strip()
    ask('Did the RGB strip fade?')

    print 'Starting the 7-Segment Clock'
    os.system('python clock.py someargthat_preventsBGrun')
    ask('Does clock display the current time?')

    print 'Initializing the LCD display'
    lcd.Initialize()
    ask('Does the character display have some text?')

    #####################
    # Final Tests:
    #####################

    ask('Ready to start full alarm?')
    os.system('python alarm.py someargthat_allowsforshortsequence')
