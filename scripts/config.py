import sys

write_to_stdout = True


def quiet_logging(new_value):
    global write_to_stdout
    write_to_stdout = new_value


def send(info):
    """Force output to parent application"""
    if write_to_stdout:
        print info
        sys.stdout.flush()
