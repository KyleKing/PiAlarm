import subprocess
import os
import config as cg

# output = 256 if running, else = 0
output = os.system("ps aux | grep 'pi-blaster\/[p]i-blaster'")
if (output > 0):
    cg.send(subprocess.call(['bash', './scripts/bootPiBlaster.sh']))
else:
    cg.send('Pi-Blaster is already running!')
    # # Stop pi-blaster:
    # print os.system("sudo kill $(ps aux | grep 'pi-blaster\/[p]" +
    #                 "i-blaster' | awk '{print $2}')")
