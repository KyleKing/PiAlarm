"""Interface for status.py file."""

import sys

from modules import config as cg
from modules import status

# Quiet logging, so the only output is "forced"
cg.quiet_logging(True)

# Parse STDIN:
if len(sys.argv) > 1:
    arg = cg.parse_argv(sys)
    status.run(arg)
else:
    cg.send('No state change, only updating LED')
    status.set_led_state()
