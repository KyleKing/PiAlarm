"""Handle importing stubbed Python libraries if not on Raspberry Pi."""

import sys
import os

# Add path to stub files so stubs can be loaded if they exist
stubs_path = os.path.expanduser('~/Developer/My-Programming-Sketchbook/Python/Stubs')
if os.path.isdir(stubs_path):
    sys.path.append(stubs_path)

try:
    import stub_RPiGPIO as IO
except ImportError:
    import RPi.GPIO as IO  # noqa
