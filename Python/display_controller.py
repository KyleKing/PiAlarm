import time
import schedule

from modules import config as cg

cg.quiet_logging(False)


def update_segment_clock():
    print("I'm working...")


def d_con():
    # schedule.every().hour.do(job)
    # schedule.every().day.at("10:30").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


def start():
    """Point of entry from main.py"""
    if cg.is_pi():
        schedule.every(1).minutes.do(update_segment_clock)
    else:
        cg.send('Not on Raspberry Pi, so not running 7-segment')

    # Start a new thread for updates
    cg.thread(d_con)
