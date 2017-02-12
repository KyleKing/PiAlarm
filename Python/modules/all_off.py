import config as cg

cg.quiet_logging(False)

# Electronic Pin Numbering Globals:
pin_buzzer = cg.get_pin('Haptics', 'pin_buzzer')
pin_shaker = cg.get_pin('Haptics', 'pin_shaker')
pin_blue = cg.get_pin('RGB_Strip', 'pin_blue')
pin_red = cg.get_pin('RGB_Strip', 'pin_red')
pin_green = cg.get_pin('RGB_Strip', 'pin_green')


def run():
    cg.send('\nDeactivating all PWM pins')
    cg.set_PWM(pin_buzzer, 0)
    cg.set_PWM(pin_shaker, 0)
    cg.set_PWM(pin_red, 0)
    cg.set_PWM(pin_blue, 0)
    cg.set_PWM(pin_green, 0)
    cg.send("\nSet all pins to off state [all_off.run()]\n")


if __name__ == "__main__":
    run()
