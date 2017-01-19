# !/usr/bin/python

import sys
import Adafruit_CharLCD as LCD
import Adafruit_GPIO.MCP230xx as MCP
import datetime

from modules import config as cg


# FIXME: Trims last word in longer strings...
# TODO: Can't handle longer words that don't have spaces inside (just cut)

cg.quiet_logging(False)

# Define LCD column and row size for 20x4 LCD.
lcd_columns = 20
lcd_rows = 4

# Raspberry Pi pin configuration:
lcd_rs = 6
lcd_en = 7
lcd_d4 = 3
lcd_d5 = 2
lcd_d6 = 1
lcd_d7 = 0
lcd_backlight = 4  # Disconnected -PWM are used instead
lcd_red = cg.get_pin('LCD_I2C_Pins', 'lcd_red')
lcd_green = cg.get_pin('LCD_I2C_Pins', 'lcd_green')
lcd_blue = cg.get_pin('LCD_I2C_Pins', 'lcd_blue')

gpio = MCP.MCP23008()
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight, gpio=gpio)

# Set brightness to something reasonable based on time of day
now = datetime.datetime.now()
default_b = (0.4, 0.4, 0.4)
dimmed_b = (0.7, 0.7, 0.7)
brightness = default_b if now.hour < 6 or now.hour > 9 else dimmed_b


def ext(count, unit=' '):
    """Extend a string by a number of string units"""
    out = ''
    for i in range(count):
        out += unit
    return out


def flip(segments):
    """Flip order of the middle two values of a list"""
    flipped = segments[2]
    segments[2] = segments[1]
    segments[1] = flipped
    return segments


def parse(message):
    """Sort words into correctly sized lists"""
    messages = message.split(' ')
    counter = 0
    segment = ''
    segments = []
    while counter < len(messages):
        counter += 1
        l_s = len(segment)
        chunk = messages[counter - 1]
        segment = chunk if l_s == 0 else '{} {}'.format(segment, chunk)
        if (len(messages[counter]) + l_s) >= lcd_columns:
            # Save string segment and reset for next loop
            segments.append(segment + ext(lcd_columns - l_s))
            segment = ''
    # Append final segment:
    segments.append(segment + ext(lcd_columns - l_s))
    return segments


def parse_message(raw):
    """Modify a message to display coherently on the LCD"""
    lcd.clear()
    message = raw.strip()
    if len(message) <= lcd_columns:
        lcd.message(message)
        return message

    segments = parse(message)
    if len(segments) == 2:
        segments.insert(1, ext(lcd_columns))  # extra blank row for LCD order
    elif len(segments) <= lcd_rows:
        segments = flip(segments)
    else:
        segments = flip(segments)
        warning = '** Too Long ** '  # alert user of length error
        segments[3] = warning + ext(lcd_columns - len('** Too Long ** '))
        for i in range(len(segments) - 4):
            segments.pop()

    full_msg = ''
    for segment in segments:
        full_msg += segment
    # print full_msg
    lcd.message(full_msg)
    return full_msg


def set_disp(r, g, b):
    """Control the R,G,B color of LCD"""
    cg.set_PWM(lcd_red, r)
    cg.set_PWM(lcd_green, g)
    cg.set_PWM(lcd_blue, b)


def Initialize():
    """Set color & initial value to display"""
    cg.send('Manually set LCD brightness through pi-blaster')
    cg.send(' *Note all values are inverse logic (0 - high, 1 - off)')
    set_disp(brightness)
    parse_message('Initialized')


if __name__ == "__main__":
    Initialize()
    while True:
        line = sys.stdin.readline()
        message = line.rstrip()

        if 'turn lcd screen for alarm clock' in message:
            if 'on' in message:
                set_disp(0.4, 0.7, 0.4)
                cg.send('Turned display on')
            elif 'off' in message:
                set_disp(1.0, 1.0, 1.0)
                cg.send('Turned display off')
        else:
            try:
                # Accept a message already in a list (i.e. ['1','2'])
                segments = eval(message)
                if len(segments) == 2:
                    segments.insert(1, ext(lcd_columns))
                elif len(segments) > 2:
                    flip(segments)
                comp = ''
                for segment in segments:
                    comp += segment + ext(lcd_columns - len(segment))
                # cg.send('Received pre-parsed message: ' + comp)
            except:
                # Otherwise parse whatever string was sent
                comp = parse_message(message)
                # cg.send('Auto-parsed message: {}'.format(comp))
            lcd.clear()
            lcd.message(comp)
        # Force buffer to close and send all data to Node application
        sys.stdout.flush()
