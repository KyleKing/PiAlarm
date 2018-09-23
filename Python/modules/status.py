"""Manage user's Home/Away status."""

import sys

import config as cg

# FYI: For a synchronous status query, call this file with an arg of:
#    exit, enter, false, or true respectively

quiet = False
cg.quiet_logging(quiet)


def update_status(running):
    """Update status in INI file."""
    # cg.send('Setting alarm status to: {}'.format(running))
    cg.write_ini('Alarm_Status', 'running', running)


def set_led_state():
    """Set the LED to ON for Away."""
    away_led = cg.get_pin('Alarm_Status', 'away_led')
    if cg.check_status():
        cg.send('Present', force=True)
        cg.set_pwm(away_led, 0, quiet)
    else:
        cg.send('Away', force=True)
        cg.set_pwm(away_led, 1, quiet)


def run(arg):
    """Parse arguments."""
    if 'exit' in arg or 'leave' in arg or 'false' in arg:
        update_status('false')
    elif 'enter' in arg or 'true' in arg:
        update_status('true')
    else:
        cg.send('Error: unknown arg = {}'.format(arg))
    set_led_state()


if __name__ == '__main__':
    # Quiet logging, so the only output is "forced"
    cg.quiet_logging(True)

    # Parse STDIN:
    if len(sys.argv) > 1:
        arg = cg.parse_argv(sys)
        run(arg)
    else:
        cg.send('No state change, only updating LED')
        set_led_state()
