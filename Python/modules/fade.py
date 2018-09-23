from time import sleep

import config as cg

###########################
# Globals:
###########################

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


###########################
# Functions and Stuff
###########################


def fade_up(pin):
    for i in range(steps):
        cg.set_PWM(pin, max_brightness * (1 - (1 / (i + 2))))
        sleep(time_step)


def fade_down(pin):
    for i in range(steps):
        cg.set_PWM(pin, max_brightness / (i + 2))
        sleep(time_step)


def all_off():
    cg.send('\nDeactivating SOME PWM pins')
    cg.set_PWM(pin_red, 0)
    cg.set_PWM(pin_blue, 0)
    cg.set_PWM(pin_green, 0)


def all_on(max_brightness=1):
    cg.send('\nActivating all LED Strip pins')
    cg.set_PWM(pin_red, max_brightness)
    cg.set_PWM(pin_blue, max_brightness)
    cg.set_PWM(pin_green, max_brightness)


def fade_RGB_Strip():
    all_off()

    cg.set_PWM(pin_red, 0.1)

    fade_up(pin_green)
    fade_down(pin_red)
    fade_up(pin_blue)
    fade_down(pin_green)
    fade_up(pin_red)
    fade_down(pin_blue)

    all_off()


if __name__ == '__main__':
    # Test the above module:
    fade_RGB_Strip()
    print "Did Fade work? (Press Key)"

    cg.set_PWM(pin_red, 0.5)
    print "Currently Red? (Press Key)"
    cg.set_PWM(pin_green, 0.5)
    print "Currently Green? (Press Key)"
    cg.set_PWM(pin_blue, 0.5)
    print "Currently Blue? (Press Key)"
