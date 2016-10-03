# !/usr/bin/python

import sys
# import time
import Adafruit_CharLCD as LCD

# Raspberry Pi pin configuration (adjusted for soldered perf board):
# Pin Name = Actual Pin Number # LCD Pin (#/16)-Expected Pin Number
lcd_rs = 24  # 4-27
lcd_en = 25  # 6-22
lcd_d4 = 12  # 11-25
lcd_d5 = 13  # 12-24
lcd_d6 = 16  # 13-23
lcd_d7 = 19  # 14-18
lcd_backlight = 26  # 16-4 (FIXME: currently grounded, but could be to 21?)
# # Only for RGB display:
# lcd_red   = 19  # 16-4
# lcd_green = 17 # 17-17
# lcd_blue  = 7  # 18-7 (Pin 7 is CE1)

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)


def full_message(message):
    lcd.clear()
    if len(message) < lcd_columns:
        # Normal Method
        lcd.message(message)
        # print(message)
    elif len(message) <= 2 * lcd_columns:
        # Split into two rows
        first_line = message[:lcd_columns]
        second_line = message[lcd_columns:]
        lcd.message(first_line + "\n" + second_line)
    # FIXME # This is a mess...
    # elif len(message) > 2 * lcd_columns:
    #     lcd.message(message)
    #     # print(message)
    #     for i in range(len(message) - lcd_columns):
    #         time.sleep(0.5)
    #         lcd.move_left()
    #     for i in range(len(message) - lcd_columns):
    #         time.sleep(0.5)
    #         lcd.move_right()
    #     return True
    else:
        lcd.message(message)
        # print(message)
        return False
    return True


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
