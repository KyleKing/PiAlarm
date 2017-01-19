import sys
import os
import requests
import ConfigParser
import subprocess

quiet_STDOUT = True


def quiet_logging(new_value=True):
    global quiet_STDOUT
    quiet_STDOUT = new_value


def send(info):
    """Force output to parent application"""
    if not quiet_STDOUT:
        print info
        sys.stdout.flush()


def _ini_path():
    if 'scripts' in os.getcwd():
        return os.getcwd() + '/pins.ini'
    else:
        return os.getcwd() + '/scripts/pins.ini'


def get_pin(component, param, _eval=False):
    """Get pin numbering value from a shared ini file"""
    pin_numbering = ConfigParser.RawConfigParser()
    file = _ini_path()
    try:
        pin_numbering.read(file)
        raw = pin_numbering.get(component, param)
        return eval(raw) if _eval else raw
    except:
        raise Exception("Failed to load " + file)


def write_ini(component, param, value, file="./scripts/pins.ini"):
    pin_config = ConfigParser.RawConfigParser()
    pin_config.read(file)
    with open(file, 'w') as cfgfile:
        pin_config.set(component, param, value)
        pin_config.write(cfgfile)


def check_status():
    """Returns True, if alarm is to continue running, else is False"""
    stat = get_pin('Alarm_Status', 'running')
    return 'true' in stat.lower()


def ifttt(event, dataset={'value1': ''}):
    """Trigger IFTTT Maker Event"""
    key = get_pin('IFTTT', 'key', _eval=True)
    try:
        requests.post("https://maker.ifttt.com/trigger/" +
                      "{}/with/key/{}".format(event, key), data=dataset)
    except:
        print 'IFTTT Failed - possible loss of INTERNET connection'


def set_PWM(pin_num, percent, quiet=False):
    """Run PWM commands through Pi-Blaster
        echo "22=0" > /dev/pi-blaster
    """
    cmd = 'echo "' + str(pin_num).zfill(2) + \
        '={0:0.2f}" > /dev/pi-blaster'.format(percent * 1.0)
    # cmd = 'echo "{:02}={:0.2}" > /dev/pi-blaster'.format(
    #        pin_num, percent * 1.0)
    if not quiet:
        send(cmd)
    return subprocess.call(cmd, shell=True)


def release_PWM(pin_num):
    """Release pin from Pi-Blaster
        echo "release 22" > /dev/pi-blaster
    """
    cmd = 'echo "release {:02}" > /dev/pi-blaster'.format(pin_num)
    send(cmd)
    return subprocess.call(cmd, shell=True)
