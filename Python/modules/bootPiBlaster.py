"""Start the pi-blaster instance."""

import subprocess

import config as cg

cg.quiet_logging(False)

if cg.is_running("'pi-blaster\/[p]i-blaster'"):
    cg.send('Pi-Blaster is already running')
else:
    cg.send('Starting fresh instance of Pi-Blaster')
    if cg.is_pi():
        cg.send(subprocess.call(['bash', cg.get_path('modules/bootPiBlaster.sh')]))
