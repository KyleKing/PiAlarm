"""Fade LED Strip."""

from time import sleep

from . import config as cg

# cg.quiet_logging(False)
cg.quiet_logging(True)

# Electronic Pin Numbering Globals:
pin_blue = cg.get_pin('RGB_Strip', 'pin_blue')
pin_red = cg.get_pin('RGB_Strip', 'pin_red')
pin_green = cg.get_pin('RGB_Strip', 'pin_green')

max_brightness = 1.0
steps = 30
total_run_time = 60
time_step = total_run_time / (6 * steps)  # 3 fades up, 3 down = 6


def fade_up(pin):
    """Fade brightness in the positive direction."""
    for i in range(steps):
        cg.set_pwm(pin, max_brightness * (1 - (1 / (i + 2))))
        sleep(time_step)


def fade_down(pin):
    """Fade brightness in the negative direction."""
    for i in range(steps):
        cg.set_pwm(pin, max_brightness / (i + 2))
        sleep(time_step)


def all_off():
    """Turn off LEDs."""
    cg.send('\nDeactivating SOME PWM pins')
    cg.set_pwm(pin_red, 0)
    cg.set_pwm(pin_blue, 0)
    cg.set_pwm(pin_green, 0)


def all_on(max_brightness=1):
    """Set LEDs to max brightness."""
    cg.send('\nActivating all LED Strip pins')
    cg.set_pwm(pin_red, max_brightness)
    cg.set_pwm(pin_blue, max_brightness)
    cg.set_pwm(pin_green, max_brightness)


def fade_rgb_strip():
    """Fade the LED strip through a full RGB sequence."""
    all_off()

    cg.set_pwm(pin_red, 0.1)

    fade_up(pin_green)
    fade_down(pin_red)
    fade_up(pin_blue)
    fade_down(pin_green)
    fade_up(pin_red)
    fade_down(pin_blue)

    all_off()


if __name__ == '__main__':
    # Test the above methods:
    fade_rgb_strip()
    input('Did Fade work? (Press Key)')

    cg.set_pwm(pin_red, 0.5)
    input('Currently Red? (Press Key)')
    cg.set_pwm(pin_green, 0.5)
    input('Currently Green? (Press Key)')
    cg.set_pwm(pin_blue, 0.5)
    input('Currently Blue? (Press Key)')
