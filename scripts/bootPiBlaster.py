import subprocess
import os
import config as cg

cg.quiet_logging(False)

# output = 256 if running, else = 0
output = os.system("ps aux | grep 'pi-blaster\/[p]i-blaster'")
cg.send('Pi-Blaster ps aux task returned: ' + str(output))
if output == 0:
    cg.send('Pi-Blaster is already running')
    # # Stop pi-blaster:
    # print os.system("sudo kill $(ps aux | grep 'pi-blaster\/[p]" +
    #                 "i-blaster' | awk '{print $2}')")
else:
    cg.send('Starting fresh instance of Pi-Blaster')
    cg.send(subprocess.call(['bash', './scripts/bootPiBlaster.sh']))


# sudo kill $(ps aux | grep 'pi-blaster\/[p]i-blaster' | awk '{print $2}')
