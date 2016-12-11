# !/usr/bin/python

import sys
import config as cg
import Adafruit_CharLCD as LCD
import Adafruit_GPIO.MCP230xx as MCP  # Only for I2C Config


# FIXME: Trims last word in longer strings...
# Also can't handle longer words that don't have spaces inside (just cut)
# Probably transform this into a class?


cg.quiet_logging(False)

# Define LCD column and row size for 20x4 LCD.
lcd_columns = 20
lcd_rows = 4

# #######################
# Regular COnfig:

# # Raspberry Pi pin configuration:
# # file = "./pins.ini"
# file = "./scripts/pins.ini"
# lcd_rs = cg.get_pin('LCD_Pins', 'lcd_rs', file)
# lcd_en = cg.get_pin('LCD_Pins', 'lcd_en', file)
# lcd_d4 = cg.get_pin('LCD_Pins', 'lcd_d4', file)
# lcd_d5 = cg.get_pin('LCD_Pins', 'lcd_d5', file)
# lcd_d6 = cg.get_pin('LCD_Pins', 'lcd_d6', file)
# lcd_d7 = cg.get_pin('LCD_Pins', 'lcd_d7', file)
# lcd_red = cg.get_pin('LCD_Pins', 'lcd_red', file)
# lcd_green = cg.get_pin('LCD_Pins', 'lcd_green', file)
# lcd_blue = cg.get_pin('LCD_Pins', 'lcd_blue', file)

# # Initialize the LCD using the pins above.
# lcd = LCD.Adafruit_RGBCharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
#                               lcd_d7, lcd_columns, lcd_rows, lcd_red,
#                               lcd_green, lcd_blue)

# #######################
# #######################
# I2C COnfig:

# Define MCP pins connected to the LCD.
lcd_rs = 0
lcd_en = 1
lcd_d4 = 2
lcd_d5 = 3
lcd_d6 = 4
lcd_d7 = 5
lcd_backlight = 0  # Don't assign to any pin b/c over-ridden with PWM pins

gpio = MCP.MCP23008()

# Initialize the LCD using the pins
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight, gpio=gpio)

# #######################


def ext(count, unit=' '):
    """Extend some base string"""
    out = ''
    for i in range(count):
        out = out + unit
    return out


def flip(sections):
    flipped = sections[2]
    sections[2] = sections[1]
    sections[1] = flipped
    return sections


def parse(message):
    messages = message.split(' ')
    counter = 1
    section = ''
    sections = []
    while counter < len(messages):
        chunk = messages[counter - 1]
        if len(section) == 0:
            section = chunk
        else:
            section = section + ' ' + chunk
        next_chunk = messages[counter]
        if (len(next_chunk) + len(section)) >= lcd_columns:
            new_message = section + ext(lcd_columns - len(section))
            sections.append(new_message)
            section = ''
        counter = counter + 1
    sections.append(section + ext(lcd_columns - len(section)))
    return sections


def parse_message(raw):
    """Display a message as expected"""
    message = raw.strip()
    lcd.clear()
    if len(message) <= lcd_columns:
        lcd.message(message)
        return message
    sections = parse(message)
    if len(sections) == 2:
        sections.insert(1, ext(lcd_columns))
    elif len(sections) <= lcd_rows:
        sections = flip(sections)
    else:
        sections = flip(sections)
        warning = '** Too Long ** '
        sections[3] = warning + ext(lcd_columns - len('** Too Long ** '))
        for i in range(len(sections) - 4):
            sections.pop()
        # lcd.message(message)
        # for i in range(lcd_columns - len(message)):
        #     time.sleep(0.2)
        #     lcd.move_right()
        # for i in range(lcd_columns - len(message)):
        #     time.sleep(0.2)
        #     lcd.move_left()

    comp_message = ''
    for section in sections:
        comp_message = comp_message + section
    lcd.message(comp_message)
    # print comp_message
    return comp_message


def set_disp(r, g, b):
    cg.set_PWM(lcd_red, r)
    cg.set_PWM(lcd_green, g)
    cg.set_PWM(lcd_blue, b)


def Initialize():
    # lcd.set_color(0, 0, 0)
    cg.send('Manually set LCD brightness through pi-blaster')
    cg.send(' *Note all values are inverse logic (0 - high, 1 - off)')
    set_disp(0.5, 1.0, 0.5)
    parse_message('Initialized')


Initialize()
while True:
    line = sys.stdin.readline()
    message = line.rstrip()
    # message = "['testing atesting', 'asdf']"
    # message = 'testing atesting btesting ctesting v'
    if 'turn lcd screen for alarm clock' in message:
        if 'on' in message:
            set_disp(0.4, 0.7, 0.4)
            cg.send('Turned display on')
        elif 'off' in message:
            set_disp(1.0, 1.0, 1.0)
            cg.send('Turned display off')
    else:
        try:
            sections = eval(message)
            if len(sections) == 2:
                sections.insert(1, ext(lcd_columns))
            elif len(sections) > 2:
                flip(sections)
            comp = ''
            for section in sections:
                comp = comp + section + ext(lcd_columns - len(section))
            # cg.send('Received pre-parsed message: ' + comp)
        except:
            comp = parse_message(message)
            # cg.send('Auto-parsed message: ' + str(comp))
        lcd.clear()
        lcd.message(comp)
    # Force buffer to close and send all data to Node application
    sys.stdout.flush()


# # # Manual Tests
# # full_message('Very long Message to Test Maximum String Allowed')
# # time.sleep(3.0)
# # full_message('Really Long Scroll Message')
# # time.sleep(3.0)
# # full_message('Short Message')


# # # message = 'Scroll'
# # # lcd.message(message)
# # # for i in range(lcd_columns - len(message)):
# # #     time.sleep(0.5)
# # #     lcd.move_right()
# # # for i in range(lcd_columns - len(message)):
# # #     time.sleep(0.5)
# # #     lcd.move_left()

# # # Demo turning backlight off and on.
# # lcd.clear()
# # lcd.message('Flash backlight\nin 5 seconds...')
# # print('Displaying: Flash backlight\nin 5 seconds...')
# # time.sleep(5.0)

# # # Show some basic colors.
# # lcd.set_color(1.0, 0.0, 0.0)
# # lcd.clear()
# # lcd.message('RED')
# # time.sleep(2.0)

# # lcd.set_color(0.0, 1.0, 0.0)
# # lcd.clear()
# # lcd.message('GREEN')
# # time.sleep(2.0)

# # lcd.set_color(0.0, 0.0, 1.0)
# # lcd.clear()
# # lcd.message('BLUE')
# # time.sleep(2.0)

# # lcd.set_color(1.0, 1.0, 0.0)
# # lcd.clear()
# # lcd.message('YELLOW')
# # time.sleep(2.0)

# # lcd.set_color(0.0, 1.0, 1.0)
# # lcd.clear()
# # lcd.message('CYAN')
# # time.sleep(2.0)

# # lcd.set_color(1.0, 0.0, 1.0)
# # lcd.clear()
# # lcd.message('MAGENTA')
# # time.sleep(2.0)

# # lcd.set_color(1.0, 1.0, 1.0)
# # lcd.clear()
# # lcd.message('WHITE')
# # time.sleep(2.0)
