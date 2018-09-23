"""Handle importing stubbed Python libraries if not on Raspberry Pi."""

import os
import sys

# Add path to stub files so stubs can be loaded if they exist
stubs_path = os.path.expanduser('~/Developer/My-Programming-Sketchbook/Python/Stubs')
if os.path.isdir(stubs_path):
    sys.path.append(stubs_path)

try:
    import stub_RPiGPIO as IO
except ImportError:
    import RPi.GPIO as IO  # noqa

try:
    import stub_Adafruit_CharLCD as LCD
except ImportError:
    import Adafruit_CharLCD as LCD  # noqa

try:
    import stub_Adafruit_GPIOMCP230xx as MCP
except ImportError:
    import Adafruit_GPIO.MCP230xx as MCP  # noqa
