import schedule
from time import sleep

from modules import config as cg
from modules import lcd


cg.quiet_logging(False)
started = False
running = True


def start():
    """Point of entry from main.py"""
    global started, running
    if started:
        running = True
    else:
        started = True
        update_lcd()  # Run the process right away:
        schedule.every(1).minutes.do(update_lcd)
        cg.thread(run_sched)  # Start a separate thread


def run_sched():
    """Loop through the schedule to check if new task"""
    global running
    # schedule.every().hour.do(job)
    # schedule.every().day.at("10:30").do(job)
    while running:
        schedule.run_pending()
        sleep(1)


def update_lcd():
    """Show a new weather statement"""
    lcd.cycle_weather()


def stop():
    """Deactivate looping task"""
    global running
    running = False
