# -*- coding: utf-8 -*-
import sys
import config as cg

# FYI
# For a synchronous status query, call this file with an arg of:
#    exit, enter, false, or true respectively

quiet = False
cg.quiet_logging(quiet)


def update_status(running):
    # cg.send('Setting alarm status to: {}'.format(running))
    cg.write_ini('Alarm_Status', 'running', running)


def set_LED_state():
    away_led = cg.get_pin('Alarm_Status', 'away_led')
    if cg.check_status():
        cg.send('Present', force=True)
        cg.set_PWM(away_led, 0, quiet)
    else:
        cg.send('Away', force=True)
        cg.set_PWM(away_led, 1, quiet)


def run(arg):
    if 'exit' in arg or 'false' in arg:
        update_status('false')
    elif 'enter' in arg or 'true' in arg:
        update_status('true')
    set_LED_state()


if __name__ == "__main__":
    # Quiet logging, so the only output is "forced"
    cg.quiet_logging(True)
    # Parse STDIN:
    if len(sys.argv) > 1:
        arg = cg.parse_argv(sys)
        run(arg)
    else:
        cg.send('No state change, only updating LED')
        set_LED_state()
