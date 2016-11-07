# -*- coding: utf-8 -*-
import sys
import config as cg

cg.quiet_logging(False)

# Parse STDIN
arg = str(sys.argv[1]).lower()
if 'true' or 'false' in arg:
    cg.send('Setting alarm status to: ' + arg)
    cg.write_ini('Alarm_Status', 'running', arg)

# Check status of user and update an LED:
a_status = cg.get_pin('Alarm_Status', 'running', "./scripts/pins.ini", True)
a_led = cg.get_pin('Alarm_Status', 'led')
if 'true' in a_status:
    cg.set_PWM(a_led, 0)
elif 'false' in a_status:
    cg.set_PWM(a_led, 1)

sys.exit()
