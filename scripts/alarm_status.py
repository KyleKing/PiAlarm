# -*- coding: utf-8 -*-
import sys
import config as cg

cg.quiet_logging(False)

# Parse STDIN
arg = str(sys.argv[1])
cg.send('Setting alarm status to: ' + arg)
cg.write_ini('Alarm_Status', 'running', arg)

sys.exit()
