import config as cg

cg.quiet_logging(False)

# Electronic Pin Numbering Globals:
pin_buzzer = cg.get_pin('Haptics', 'pin_buzzer')
pin_shaker = cg.get_pin('Haptics', 'pin_shaker')
pin_blue = cg.get_pin('RGB_Strip', 'pin_blue')
pin_red = cg.get_pin('RGB_Strip', 'pin_red')
pin_green = cg.get_pin('RGB_Strip', 'pin_green')
# # TODO
# pin_blue2 = cg.get_pin('RGB_Strip', 'pin_blue2')
# pin_red2 = cg.get_pin('RGB_Strip', 'pin_red2')
# pin_green2 = cg.get_pin('RGB_Strip', 'pin_green2')


def all_off():
    cg.send('\nDeactivating all PWM pins')
    cg.set_PWM(pin_buzzer, 0)
    cg.set_PWM(pin_shaker, 0)
    cg.set_PWM(pin_red, 0)
    cg.set_PWM(pin_blue, 0)
    cg.set_PWM(pin_green, 0)
    # # TODO
    # cg.set_PWM(pin_red2, 0)
    # cg.set_PWM(pin_blue2, 0)
    # cg.set_PWM(pin_green2, 0)
    cg.send("\nFinished turning all pins to off state (all_off)\n")


if __name__ == "__main__":
    all_off()
