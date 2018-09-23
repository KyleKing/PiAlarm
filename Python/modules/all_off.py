"""Deactivate all pins."""

import config as cg

cg.quiet_logging(False)


def deactivate():
    """Deactivate the pins."""
    cg.send('\nStart: Deactivating all PWM pins')
    cg.set_PWM(cg.get_pin('Haptics', 'pin_buzzer'), 0)
    cg.set_PWM(cg.get_pin('Haptics', 'pin_shaker'), 0)
    for pin_color in ['red', 'blue', 'green']:
        cg.set_PWM(cg.get_pin('RGB_Strip', 'pin_{}'.format(pin_color)), 0)
    cg.send('\nEnd: Set all pins to off state [all_off.deactivate()]\n')


if __name__ == '__main__':
    deactivate()
