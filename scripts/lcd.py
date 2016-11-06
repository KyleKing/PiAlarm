# !/usr/bin/python

import sys
# import time
import subprocess
import config as cg
import Adafruit_CharLCD as LCD

# Raspberry Pi pin configuration:
lcd_rs = cg.get_pin('LCD_Pins', 'lcd_rs')
lcd_en = cg.get_pin('LCD_Pins', 'lcd_en')
lcd_d4 = cg.get_pin('LCD_Pins', 'lcd_d4')
lcd_d5 = cg.get_pin('LCD_Pins', 'lcd_d5')
lcd_d6 = cg.get_pin('LCD_Pins', 'lcd_d6')
lcd_d7 = cg.get_pin('LCD_Pins', 'lcd_d7')
lcd_red = cg.get_pin('LCD_Pins', 'lcd_red')
lcd_green = cg.get_pin('LCD_Pins', 'lcd_green')
lcd_blue = cg.get_pin('LCD_Pins', 'lcd_blue')

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 32
lcd_rows = 2

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_RGBCharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                              lcd_columns, lcd_rows, lcd_red, lcd_green,
                              lcd_blue)

# TODO: lcd.set_color(1.0, 0.0, 1.0) - Magenta (see more below)
lcd.clear()
lcd.set_color(0, 0, 0)
lcd.message('Initialized')


def set_PWM(pin_num, percent):
    """Run PWM commands through Pi-Blaster"""
    # echo "22=0" > /dev/pi-blaster
    cmd = 'echo "' + str(pin_num) + "=" + str(percent)
    cg.send(cmd + '" > /dev/pi-blaster')
    return subprocess.call(cmd + '" > /dev/pi-blaster', shell=True)


print 'Manually set brightness through pi-blaster'
print 'Note all values are inverse logic (1 - high = off)'
set_PWM(lcd_red, 0.98)
set_PWM(lcd_green, 1.0)
set_PWM(lcd_blue, 0.98)


def full_message(message):
    lcd.clear()
    # # Print a two line message
    # lcd.message('Hello\nworld!')
    lcd.message(message)
    # if len(message) < lcd_columns:
    #     lcd.message(message)
    # else:
    #     lcd.message(message)
    #     for i in range(lcd_columns - len(message)):
    #         time.sleep(0.2)
    #         lcd.move_right()
    #     for i in range(lcd_columns - len(message)):
    #         time.sleep(0.2)
    #         lcd.move_left()


while True:
    line = sys.stdin.readline()
    message = line.rstrip()
    full_message(message)
    print message
    # Force buffer to close and send all data to Node application
    sys.stdout.flush()

# # Manual Tests
# full_message('Very long Message to Test Maximum String Allowed')
# time.sleep(3.0)
# full_message('Really Long Scroll Message')
# time.sleep(3.0)
# full_message('Short Message')


# # message = 'Scroll'
# # lcd.message(message)
# # for i in range(lcd_columns - len(message)):
# #     time.sleep(0.5)
# #     lcd.move_right()
# # for i in range(lcd_columns - len(message)):
# #     time.sleep(0.5)
# #     lcd.move_left()

# # Demo turning backlight off and on.
# lcd.clear()
# lcd.message('Flash backlight\nin 5 seconds...')
# print('Displaying: Flash backlight\nin 5 seconds...')
# time.sleep(5.0)

# # Show some basic colors.
# lcd.set_color(1.0, 0.0, 0.0)
# lcd.clear()
# lcd.message('RED')
# time.sleep(2.0)

# lcd.set_color(0.0, 1.0, 0.0)
# lcd.clear()
# lcd.message('GREEN')
# time.sleep(2.0)

# lcd.set_color(0.0, 0.0, 1.0)
# lcd.clear()
# lcd.message('BLUE')
# time.sleep(2.0)

# lcd.set_color(1.0, 1.0, 0.0)
# lcd.clear()
# lcd.message('YELLOW')
# time.sleep(2.0)

# lcd.set_color(0.0, 1.0, 1.0)
# lcd.clear()
# lcd.message('CYAN')
# time.sleep(2.0)

# lcd.set_color(1.0, 0.0, 1.0)
# lcd.clear()
# lcd.message('MAGENTA')
# time.sleep(2.0)

# lcd.set_color(1.0, 1.0, 1.0)
# lcd.clear()
# lcd.message('WHITE')
# time.sleep(2.0)
