import sys
import requests
import ConfigParser

quiet_STDOUT = True


def quiet_logging(new_value=True):
    global quiet_STDOUT
    quiet_STDOUT = new_value


def send(info):
    """Force output to parent application"""
    if not quiet_STDOUT:
        print info
        sys.stdout.flush()


def get_pin(component, param, file="./scripts/pins.ini", raw=False):
    """Get pin numbering value from a shared ini file"""
    pin_numbering = ConfigParser.RawConfigParser()
    try:
        pin_numbering.read(file)
        raw_val = pin_numbering.get(component, param)
        if raw:
            return raw_val
        else:
            # Convert to number and return
            return eval(raw_val)
    except:
        print "Failed to load pins.ini"
        raise


def write_ini(component, param, value, file="./scripts/pins.ini"):
    pin_config = ConfigParser.RawConfigParser()
    pin_config.read(file)
    with open(file, 'w') as cfgfile:
        pin_config.set(component, param, value)
        pin_config.write(cfgfile)


def ifttt(event, dataset={'value1': ''}):
    key = get_pin('IFTTT', 'key', "./scripts/secret.ini", True)
    requests.post("https://maker.ifttt.com/trigger/" +
                  event + "/with/key/" + str(key), data=dataset)


# ifttt('PiAlarm_StartAlarm')
# ifttt('test', {'value1': 123, 'value2': 'Kyle', 'value3': 'OneMore'})
