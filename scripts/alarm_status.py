# -*- coding: utf-8 -*-
import sys
import config as cg

cg.quiet_logging(False)

# Parse STDIN
if len(sys.argv) > 1:
    arg = str(sys.argv[1]).lower()
else:
    arg = 'update_LED_only'

# except:
#     message = 'No arg sent to alarm_status.py'
#     cg.ifttt('PiAlarm_SendText', {'value1': message})
#     raise Exception(message)

if 'true' in arg or 'false' in arg:
    cg.send('Setting alarm status to: ' + arg)
    cg.write_ini('Alarm_Status', 'running', arg)
else:
    cg.send(cg.check_status())
    # cg.send('Current status is: ' + cg.check_status())

# Check status of user and update an LED:
a_led = cg.get_pin('Alarm_Status', 'led')
if cg.check_status():
    cg.set_PWM(a_led, 0)
else:
    cg.set_PWM(a_led, 1)

sys.exit()
