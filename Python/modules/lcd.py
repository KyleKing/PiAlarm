# !/usr/bin/python
import datetime
import schedule
from time import sleep
import re

import config as cg
import weather

if cg.is_pi():
    import Adafruit_CharLCD as LCD
    import Adafruit_GPIO.MCP230xx as MCP

# FIXME: Trims last word in longer strings...
# TODO: Can't handle longer words that don't have spaces inside (just cut)

cg.quiet_logging(False)

# Define LCD column and row size for 20x4 LCD
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

if cg.is_pi():
    gpio = MCP.MCP23008()
    lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                               lcd_columns, lcd_rows, lcd_backlight, gpio=gpio)

# Set brightness to something reasonable based on time of day
now = datetime.datetime.now()
# default_b = (0.5, 0.0, 1.0)
default_b = (1.0, 0.0, 1.0)
off_b = (1.0, 1.0, 1.0)
# dimmed_b = (0.7, 1.0, 0.7)
dimmed_b = (0.0, 1.0, 1.0)
brightness = dimmed_b if now.hour < 6 or now.hour > 21 else default_b


class char_disp():
    _started = False
    _running = True

    def __init__(self):
        self.Initialize()

    def Initialize(self):
        """Set color & initial value to display"""
        cg.send('Manually set LCD brightness through pi-blaster')
        cg.send(' *Note all values are inverse logic (0 - high, 1 - off)')
        self.set_disp(*brightness)
        self.custom_msg('Initialized')

    def set_disp(self, r, g, b):
        """Control the R,G,B color of LCD"""
        if cg.is_pi():
            cg.set_PWM(lcd_red, r)
            cg.set_PWM(lcd_green, g)
            cg.set_PWM(lcd_blue, b)

    def custom_msg(self, raw):
        """External call to update the display with a custom message"""
        try:
            # Check if given a list (or a text string to eval as a list)
            if type(raw) is list:
                sections = raw
            else:
                sections = eval(raw)
            if len(sections) == 2:
                sections.insert(1, self.ext(lcd_columns))
            elif len(sections) > 2:
                sections = self.flip(sections)
            comp = ''
            for section in sections:
                if type(section) is list:
                    section = section[0]
                comp = comp + section + self.ext(lcd_columns - len(section))
            self.update_disp(comp)
        except:
            comp = self.parse_message(raw)
            cg.send('Auto-parsed message: {}'.format(comp))

    def update_disp(self, msg):
        if cg.is_pi():
            lcd.clear()
            lcd.message(msg)
        else:
            cg.send('LCD would display: `{}`'.format(msg))

    #
    # Utility Functions
    #

    def ext(self, count, unit=' '):
        """Extend a string by a number of string units"""
        out = ''
        for i in range(count):
            out += unit
        return out

    def flip(self, segments):
        """Flip order of the middle two values of a list"""
        flipped = segments[2]
        segments[2] = segments[1]
        segments[1] = flipped
        return segments

    def parse(self, message):
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
                segments.append(segment + self.ext(lcd_columns - l_s))
                segment = ''
        # Append final segment:
        segments.append(segment + self.ext(lcd_columns - l_s))
        return segments

    def parse_message(self, raw):
        """Modify a message to display coherently on the LCD"""
        message = raw.strip()
        if len(message) <= lcd_columns:
            self.update_disp(message)
            return message

        segments = self.parse(message)
        if len(segments) == 2:
            # extra blank row for LCD order
            segments.insert(1, self.ext(lcd_columns))
        elif len(segments) <= lcd_rows:
            segments = self.flip(segments)
        else:
            segments = self.flip(segments)
            warning = '** Too Long ** '  # alert user of length error
            segments[3] = warning + \
                self.ext(lcd_columns - len('** Too Long ** '))
            for i in range(len(segments) - 4):
                segments.pop()
        full_msg = ''
        for segment in segments:
            full_msg += segment

        self.update_disp(full_msg)
        return full_msg

    def disp(self, status):
        """Parse text input for display state"""
        status = status.lower()
        if re.match('on', status):
            self.set_disp(0.4, 0.7, 0.4)
            cg.send('Turned display on')
        elif re.match('off', status):
            self.set_disp(1.0, 1.0, 1.0)
            cg.send('Turned display off')
        elif re.match('alt', status):
            self.set_disp(0.5, 0.1, 0.2)
            cg.send('Turned display to alt state')
        else:
            try:
                data = eval(status)
                self.set_disp(data)
            except:
                raise ValueError('Unknown display input: {}'.format(status))

    #
    # Keep the display with up-to-date weather data
    #

    def display_weather(self):
        if not self._started:
            # Start a fresh thread for weather updates
            self.update_weather()
            self._running = True
            self._started = True
            schedule.every(5).minutes.do(self.update_weather)
            cg.thread(self.run_sched)  # Start a separate thread
            # cg.send('>> Started Thread')
        elif self._running:
            cg.send('Error: Weather Update is already running')
        else:
            # Allow the weather updates to continue
            self._running = True
            cg.send('Toggling weather updates back on')

    def run_sched(self):
        """Loop through the schedule to check if new task"""
        # cg.send('> Ran Thread')
        while self._running:
            schedule.run_pending()
            # cg.send('> Still running')
            sleep(1)

    def update_weather(self):
        """Request, then parse weather data for LCD display """
        msg = []
        both_commutes = weather.hourly(quiet=False)
        for wthr in both_commutes:
            msg.append(['{}-{} {}'.format(wthr["day"],
                                          wthr["fc"], wthr["tmp"])[0:20]])
            msg.append(['{}-{}p{} {}'.format(
                wthr['pop'], wthr['snow'], wthr['precip'],
                wthr['wspd'])[0:20]])
        self.custom_msg(msg)
        cg.send('LCD Weather: {}'.format(msg))
        return msg

    def stop_weather(self):
        """Stop the schedule run pending loop"""
        self._running = False
        self._started = False
        cg.send('Stopped weather thread')


#
# Point of entry:
#

this_disp = char_disp()


def brightness(raw):
    """Set the display brightness based on raw input"""
    global this_disp
    this_disp.disp(raw)


def text(msg):
    """Set the display text using smart parser"""
    global this_disp
    this_disp.custom_msg(msg)


def cycle_weather():
    global this_disp
    this_disp.display_weather()


def stop_weather():
    global this_disp
    this_disp.stop_weather()


if __name__ == "__main__":
    brightness('alt')
    text('THIS PROBABLY WORKS!')
