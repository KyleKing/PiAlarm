import sys
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


def get_pin(component, param):
    """Get pin numbering value from a shared ini file"""
    pin_numbering = ConfigParser.RawConfigParser()
    try:
        pin_numbering.read("./scripts/pins.ini")
        raw_val = pin_numbering.get(component, param)
        # Convert to number and return
        return eval(raw_val)
    except:
        print "Failed to load pins.ini"
        raise
