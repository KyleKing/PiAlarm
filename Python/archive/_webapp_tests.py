import os
import json
import requests

from modules import all_off
from modules import config as cg
import _tests


print '** Getting started! Turning everything off **'
all_off.all_off()
print 'Booting Pi-Blaster'
os.system('sudo python ./bootPiBlaster.py')
print ''

#####################
# Test exit/enter capabilities
#####################

with open('../secret.json') as secrets_file:
    secrets = json.load(secrets_file)
    key = secrets["maker"]
    ip = secrets["ip"]

# Query the server:
print "connecting to: " + "http://{}/{}/exit".format(ip, key)
requests.post("http://{}/{}/exit".format(ip, key))
pass_exit = _tests.test_passed(True, cg.check_status())
print "With URL, set to Exit: {}".format(pass_exit)
_tests.ask('Is the away LED on?')

requests.post("http://{}/{}/enter".format(ip, key))
pass_enter = _tests.test_passed(True, cg.check_status())
print "With URL, set to Enter: {}".format(pass_enter)
