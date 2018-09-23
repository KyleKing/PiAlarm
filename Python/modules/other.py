import config as cg
import lcd
from context import IO

###########################
# Configuration:
###########################

disp_btn = cg.get_pin('Input_Pins', 'disp_btn')
_last = True  # Toggle between brightening the display and turning it off


def toggle():
    global _last
    disp = (0.9, 0.4, 0.8) if _last else (1.0, 1.0, 1.0)
    lcd.brightness(disp)
    cg.send('Toggled LCD w/ l:{} > {} '.format(_last, disp))
    _last = (not _last)  # update last display status


cg.send('Set GPIO mode and event detection')
IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(disp_btn, IO.IN)
IO.add_event_detect(disp_btn, IO.RISING, callback=toggle, bouncetime=300)
