import os
import sys
import requests
import threading
import subprocess
import ConfigParser
# import datetime

quiet_STDOUT = True


#
# Interactions
#


def send(info, force=False):
    """Force output to parent application"""
    if not quiet_STDOUT or force:
        # now = datetime.datetime.now()
        # print '{:02}:{:02}> {}'.format(int(now.hour),
        #       int(now.minute), info)
        print '{}'.format(info)
        sys.stdout.flush()


def quiet_logging(new_value=True):
    global quiet_STDOUT
    quiet_STDOUT = new_value


def ifttt(event, dataset={'value1': ''}):
    """Trigger IFTTT Maker Event"""
    key = read_ini('IFTTT', 'key', filename='secret')
    try:
        requests.post("https://maker.ifttt.com/trigger/" +
                      "{}/with/key/{}".format(event, key), data=dataset)
    except:
        print 'IFTTT Failed - possible loss of INTERNET connection'


#
# INI tools
#


def _ini_path(filename='pins'):
    cwd = os.getcwd()
    if 'Python' in cwd:
        if 'modules' in cwd:
            return '{}/../{}.ini'.format(cwd, filename)
        else:
            return '{}/{}.ini'.format(cwd, filename)
    else:
        return '{}/Python/{}.ini'.format(cwd, filename)


def get_pin(component, param, _eval=True):
    """Get pin numbering value from a shared ini file"""
    raw = read_ini(component, param, filename='pins')
    return eval(raw) if _eval else raw


def read_ini(component, param, filename='pins'):
    config = ConfigParser.RawConfigParser()
    file = _ini_path(filename)
    try:
        config.read(file)
        return config.get(component, param)
    except:
        raise Exception("Failed to load `{}` and `{}` from: {}".format(
            component, param, file))


def write_ini(component, param, value):
    pin_config = ConfigParser.RawConfigParser()
    file = _ini_path()
    pin_config.read(file)
    with open(file, 'w') as cfgfile:
        pin_config.set(component, param, value)
        pin_config.write(cfgfile)


def check_status():
    """Returns True, if alarm is to continue running, else is False"""
    stat = get_pin('Alarm_Status', 'running', _eval=False)
    return 'true' in stat.lower()


#
# PWM Tools
#


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
    return False if not is_pi() else subprocess.call(cmd, shell=True)


def release_PWM(pin_num):
    """Release pin from Pi-Blaster
        echo "release 22" > /dev/pi-blaster
    """
    cmd = 'echo "release {:02}" > /dev/pi-blaster'.format(pin_num)
    send(cmd)
    return subprocess.call(cmd, shell=True)

#
# Try evaluating unknown inputs:
#


def try_eval(raw):
    """Try to find a True/False, Integer, etc. value in str input"""
    raw = raw.strip()
    try:
        return eval(raw)
    except:
        return raw


def dict_arg(args, key):
    """Try to decode the dictionary key or return False"""
    try:
        this = args[key]
        send('->- {} found in `{}`'.format(key, args))
        return this
    except:
        send('-X- {} not found in `{}`'.format(key, args))
        return False

#
# File system
#


def is_pi():
    return 'pi' in os.path.abspath('')


def get_path(raw):
    if 'Python' not in raw:
        full = '{}/Python/{}'.format(os.path.abspath(''), raw)
        send('Setting r: {} to f: {}'.format(raw, full))
        return full
    else:
        return raw


def is_running(task):
    """Use ps aux to check if a script is actively running"""
    # output = 256 if running, else = 0
    output = os.system("ps aux | grep {}".format(task))
    is_active = output == 0
    send('Is `{}` running? > {} ({})'.format(task, is_active, output))
    return is_active


#
# Other
#


def parse_argv(sys_in, arg_num=1):
    return str(sys_in.argv[arg_num]).strip().lower()


def thread(target, args=()):
    """Start thread for parallel processes"""
    this = threading.Thread(target=target, args=args)
    this.daemon = True  # will only run if main thread running
    this.start()
    return this


# # Stop pi-blaster / or any process:
# print os.system("sudo kill $(ps aux | grep 'pi-blaster\/[p]" +
#                 "i-blaster' | awk '{print $2}')")
# sudo kill $(ps aux | grep 'pi-blaster\/[p]i-blaster' | awk '{print $2}')
