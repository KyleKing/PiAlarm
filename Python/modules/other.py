import lcd
import config as cg

if cg.is_pi():
    import RPi.GPIO as GPIO

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


if cg.is_pi():
    cg.send('Set GPIO mode and event detection')
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(disp_btn, GPIO.IN)
    GPIO.add_event_detect(disp_btn, GPIO.RISING,
                          callback=toggle, bouncetime=300)
