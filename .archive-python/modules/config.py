"""Configuration Utilities."""

import configparser
import inspect
import os
import subprocess
import sys
import threading

import requests

quiet_STDOUT = True


#
# Interactions
#


def send(info, force=False):
    """Force output to parent application."""
    if not quiet_STDOUT or force:
        print('{}'.format(info))
        sys.stdout.flush()


def quiet_logging(new_value=True):
    """Toggle logging."""
    global quiet_STDOUT
    quiet_STDOUT = new_value


def ifttt(event, dataset={'value1': ''}):
    """Trigger IFTTT Maker Event."""
    key = read_ini('IFTTT', 'key', filename='secret')
    try:
        requests.post('https://maker.ifttt.com/trigger/{}/with/key/{}'.format(event, key), data=dataset)
    except:  # noqa
        print('IFTTT Failed - possible loss of INTERNET connection')


#
# INI tools
#


def _ini_path(filename='pins'):
    """Get ini file path."""
    cwd = os.getcwd()
    if 'Python' in cwd:
        if 'modules' in cwd:
            return '{}/../{}.ini'.format(cwd, filename)
        else:
            return '{}/{}.ini'.format(cwd, filename)
    else:
        return '{}/Python/{}.ini'.format(cwd, filename)


def get_pin(component, param, _eval=True):
    """Get pin numbering value from a shared ini file."""
    raw = read_ini(component, param, filename='pins')
    return eval(raw) if _eval else raw


def read_ini(component, param, filename='pins'):
    """Read ini file."""
    config = configparser.RawConfigParser()
    file = _ini_path(filename)
    try:
        config.read(file)
        return config.get(component, param)
    except:  # noqa
        raise Exception('Failed to load `{}` and `{}` from: {}'.format(
            component, param, file))


def write_ini(component, param, value):
    """Write to ini file."""
    pin_config = configparser.RawConfigParser()
    file = _ini_path()
    pin_config.read(file)
    with open(file, 'w') as cfgfile:
        pin_config.set(component, param, value)
        pin_config.write(cfgfile)


def check_status():
    """Return True, if alarm is to continue running, else is False."""
    stat = get_pin('Alarm_Status', 'running', _eval=False)
    return 'true' in stat.lower()


#
# PWM Tools
#


def set_pwm(pin_num, percent, quiet=False):
    """Run PWM commands through Pi-Blaster."""
    # ex: echo '22=0.0' > /dev/pi-blaster
    cmd = 'echo "{:02}={:0.2f}" > /dev/pi-blaster'.format(int(pin_num), float(percent))
    if not quiet:
        send(cmd)
    return False if not is_pi() else subprocess.call(cmd, shell=True)


def release_pwm(pin_num):
    """Release pin from Pi-Blaster."""
    cmd = 'echo "release {:02}" > /dev/pi-blaster'.format(pin_num)
    send(cmd)
    return subprocess.call(cmd, shell=True)

#
# Try evaluating unknown inputs:
#


def try_eval(raw):
    """Try to find a True/False, Integer, etc. value in string input."""
    raw = raw.strip()
    try:
        return eval(raw)
    except:
        return raw


def dict_arg(args, key):
    """Try to decode the dictionary key or return False."""
    try:
        this = args[key]
        send('@> {} found in `{}`'.format(key, args))
        return this
    except:
        # send('@X {} not found in `{}`'.format(key, args))
        return False

#
# File system
#


def is_pi():
    """Check if running on a Raspberry Pi."""
    return 'pi' in os.path.abspath('')


def get_path(raw):
    """Get full path."""
    if 'Python' not in raw:
        full = '{}/Python/{}'.format(os.path.abspath(''), raw)
        send('Setting r: {} to f: {}'.format(raw, full))
        return full
    else:
        return raw


def is_running(task):
    """Use `ps aux` to check if a script is actively running."""
    # output = 256 if running, else = 0
    output = os.system('ps aux | grep {}'.format(task))
    is_active = output == 0
    send('Is `{}` running? > {} ({})'.format(task, is_active, output))
    return is_active


#
# Other
#


def parse_argv(sys_in, arg_num=1):
    """Parse arguments."""
    return str(sys_in.argv[arg_num]).strip().lower()


def thread(target, args=()):
    """Start thread for parallel processes."""
    this = threading.Thread(target=target, args=args)
    this.daemon = True  # will only run if main thread running
    this.start()
    return this


# # Stop pi-blaster / or any process:
# print os.system('sudo kill $(ps aux | grep 'pi-blaster\/[p]' +
#                 'i-blaster' | awk '{print $2}')')
# sudo kill $(ps aux | grep 'pi-blaster\/[p]i-blaster' | awk '{print $2}')


class Logger(object):
    """Simple custom logger handler.

    lgr = cg.logger('name')
    lgr.lit(lgr.ln(), 'A little alert!! With line number!')

    """

    def __init__(self, origin=False):
        """Initializer."""
        assert len(origin) == 6, 'Origin must be 6 letters ({} - is not)'.format(origin)
        self.__origin = origin if origin else '    br'

    def ln(self):
        """Get line number for logging."""
        return '{:03d}'.format(inspect.currentframe().f_back.f_lineno)

    def _format(self, ln, message):
        return '{} (#{}): {}'.format(self.__origin, ln, message.strip())

    def lit(self, ln, message, print_out=True):
        """Minor - two line comment."""
        send(self._format(ln, message))
        send(self._format(ln, ''))
        send(self._format(ln, message))

    def big(self, ln, message):
        """Major - five line comment."""
        send(self._format(ln, '__'))
        send(self._format(ln, ''))
        send(self._format(ln, message))
        send(self._format(ln, ''))
        send(self._format(ln, '__'))
