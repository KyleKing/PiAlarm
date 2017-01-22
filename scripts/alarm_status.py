# -*- coding: utf-8 -*-
import sys
from modules import config as cg

quiet = False
cg.quiet_logging(quiet)


def update_status(running):
    # cg.send('Setting alarm status to: {}'.format(running))
    cg.write_ini('Alarm_Status', 'running', running)


# Parse STDIN
if len(sys.argv) > 1:
    arg = str(sys.argv[1]).strip().lower()
    if 'exit' in arg or 'false' in arg:
        update_status('false')
    elif 'enter' in arg or 'true' in arg:
        update_status('true')

away_led = cg.get_pin('Alarm_Status', 'away_led')
if cg.check_status():
    cg.send('Present', force=True)
    cg.set_PWM(away_led, 0, quiet)
else:
    cg.send('Away', force=True)
    cg.set_PWM(away_led, 1, quiet)

sys.exit()
