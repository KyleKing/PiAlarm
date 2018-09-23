"""Manipulate a TM1637 7-segment display."""

import math
import threading
from time import localtime, sleep

import config as cg
from context import IO

IO.setwarnings(False)
IO.setmode(IO.BCM)

HexDigits = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d,
             0x07, 0x7f, 0x6f, 0x77, 0x7c, 0x39, 0x5e, 0x79, 0x71]

ADDR_AUTO = 0x40
ADDR_FIXED = 0x44
STARTADDR = 0xC0


class TM1637(object):
    """TM1637 7-Segment Display."""

    def __init__(self, clk, dio, brightness=1.0):
        """Initializer."""
        self.CLK = clk
        self.DIO = dio
        self.brightness = brightness

        self.double_point = False
        self.current_values = [0, 0, 0, 0]

        IO.setup(self.CLK, IO.OUT)
        IO.setup(self.DIO, IO.OUT)

    def cleanup(self):
        """Stop updating clock, turn off display, and cleanup GPIO."""
        self.stop_clock()
        self.clear()
        IO.cleanup()

    def clear(self):
        """Clear display."""
        b = self.brightness
        point = self.double_point
        self.brightness = 0
        self.double_point = False
        data = [0x7F, 0x7F, 0x7F, 0x7F]
        self.show(data)
        # Restore previous settings:
        self.brightness = b
        self.double_point = point

    def show(self, data):
        """Show data on display."""
        for i in range(0, 4):
            self.current_values[i] = data[i]

        self.start()
        self.write_byte(ADDR_AUTO)
        self.br()
        self.write_byte(STARTADDR)
        for i in range(0, 4):
            self.write_byte(self.coding(data[i]))
        self.br()
        self.write_byte(0x88 + int(self.brightness))
        self.stop()

    def set_digit(self, idx, data):
        """Set 7-segment digit by index [0, 3]."""
        assert not (idx < 0 or idx > 3), 'Index must be in (0,3). Args: ({},{})'.format(idx, data)

        self.current_values[idx] = data

        self.start()
        self.write_byte(ADDR_FIXED)
        self.br()
        self.write_byte(STARTADDR | idx)
        self.write_byte(self.coding(data))
        self.br()
        self.write_byte(0x88 + int(self.brightness))
        self.stop()

    def set_brightness(self, percent):
        """Set brightness in range 0-1."""
        max_brightness = 7.0
        brightness = math.ceil(max_brightness * percent)
        if (brightness < 0):
            brightness = 0
        if (self.brightness != brightness):
            self.brightness = brightness
            self.show(self.current_values)

    def show_colon(self, on):
        """Show or hide double point divider."""
        if (self.double_point != on):
            self.double_point = on
            self.show(self.current_values)

    def write_byte(self, data):
        """Write byte to display."""
        for i in range(0, 8):
            IO.output(self.CLK, IO.LOW)
            if (data & 0x01):
                IO.output(self.DIO, IO.HIGH)
            else:
                IO.output(self.DIO, IO.LOW)
            data = data >> 1
            IO.output(self.CLK, IO.HIGH)

        # Wait for ACK
        IO.output(self.CLK, IO.LOW)
        IO.output(self.DIO, IO.HIGH)
        IO.output(self.CLK, IO.HIGH)
        IO.setup(self.DIO, IO.IN)

        while IO.input(self.DIO):
            sleep(0.001)
            if (IO.input(self.DIO)):
                IO.setup(self.DIO, IO.OUT)
                IO.output(self.DIO, IO.LOW)
                IO.setup(self.DIO, IO.IN)
        IO.setup(self.DIO, IO.OUT)

    def start(self):
        """Send start signal to TM1637."""
        IO.output(self.CLK, IO.HIGH)
        IO.output(self.DIO, IO.HIGH)
        IO.output(self.DIO, IO.LOW)
        IO.output(self.CLK, IO.LOW)

    def stop(self):
        """Stop clock."""
        IO.output(self.CLK, IO.LOW)
        IO.output(self.DIO, IO.LOW)
        IO.output(self.CLK, IO.HIGH)
        IO.output(self.DIO, IO.HIGH)

    def br(self):
        """Terse break."""
        self.stop()
        self.start()

    def coding(self, data):
        """Set coding of display."""
        point_data = 0x80 if self.double_point else 0
        return 0 if data == 0x7F else HexDigits[data] + point_data

    def clock(self, military_time):
        """Clock thread script."""
        # Based on: https://github.com/johnlr/raspberrypi-tm1637
        self.show_colon(True)
        while (not self.__stop_event.is_set()):
            t = localtime()
            hour = t.tm_hour
            if not military_time:
                hour = 12 if (t.tm_hour % 12) == 0 else t.tm_hour % 12
            d0 = hour // 10 if hour // 10 else 0
            d1 = hour % 10
            d2 = t.tm_min // 10
            d3 = t.tm_min % 10
            digits = [d0, d1, d2, d3]
            self.show(digits)
            # # Optional visual feedback of running alarm:
            # print digits
            # for i in tqdm(range(60 - t.tm_sec)):
            for i in range(60 - t.tm_sec):
                if (not self.__stop_event.is_set()):
                    sleep(1)

    def start_clock(self, military_time=True):
        """Start clock thread."""
        # Stop event based on: http://stackoverflow.com/a/6524542/3219667
        self.__stop_event = threading.Event()
        self.__clock_thread = threading.Thread(target=self.clock, args=(military_time,))
        self.__clock_thread.daemon = True  # stops w/ main thread
        self.__clock_thread.start()

    def stop_clock(self):
        """Stop clock thread."""
        try:
            print 'Attempting to stop live clock'
            self.__stop_event.set()
            self.clear()
        except AttributeError:
            print 'No clock to close'


if __name__ == '__main__':
    """Confirm the display operation"""

    # Initialize the clock (GND, VCC=3.3V, Example Pins are DIO=20 and CLK=21)
    clock = cg.get_pin('7Segment', 'clk')
    digital = cg.get_pin('7Segment', 'dio')
    display = TM1637(CLK=clock, DIO=digital, brightness=1.0)
    print('clock', clock)
    print('digital', digital)

    display.clear()

    digits = [1, 2, 3, 4]
    display.show(digits)
    raw_input('1234  - Working? (Press Key)')

    print 'Updating one digit at a time:'
    display.clear()
    display.set_digit(1, 3)
    sleep(0.5)
    display.set_digit(2, 2)
    sleep(0.5)
    display.set_digit(3, 1)
    sleep(0.5)
    display.set_digit(0, 4)
    raw_input('4321  - (Press Key)')

    print 'Add double point\n'
    display.show_colon(True)
    sleep(0.2)
    print 'Brightness Off'
    display.set_brightness(0)
    sleep(0.5)
    print 'Full Brightness'
    display.set_brightness(1)
    sleep(0.5)
    print '30% Brightness'
    display.set_brightness(0.3)
    sleep(0.3)
    raw_input('Start the clock?')

    display.start_clock(military_time=True)
    raw_input('Stop the clock?')

    display.stop_clock()
