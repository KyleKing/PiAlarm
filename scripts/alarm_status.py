# -*- coding: utf-8 -*-
import sys
from modules import config as cg

quiet = False
cg.quiet_logging(quiet)

# Parse STDIN
if len(sys.argv) > 1:
    arg = str(sys.argv[1]).lower()
    if 'quiet' in arg:
        quiet = True
    if 'true' in arg or 'false' in arg:
        cg.send('Setting alarm status to: ' + arg)
        cg.write_ini('Alarm_Status', 'running', arg)

away_led = cg.get_pin('Alarm_Status', 'away_led')
if cg.check_status():
    cg.send('Present')
    cg.set_PWM(away_led, 0, quiet)
else:
    cg.send('Away')
    cg.set_PWM(away_led, 1, quiet)

sys.exit()
