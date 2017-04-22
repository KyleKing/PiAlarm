# -*- coding: utf-8 -*-
import re
import sys
import datetime
# import shutil
from time import sleep

from modules import config as cg
from modules import tests, alarm, lcd
from modules import status, all_off

if cg.is_pi():
    from modules import tm1637


cg.quiet_logging(False)


class action_input():
    """
    Break input of [`cmd`] into one of if statements listed below
        (i.e. test, alarm, lcd, status, etc...)
    Then act on supplied arguments
    """

    def __init__(self, operation, args, message=''):
        self.delay = 1
        self.msg = message
        operation = operation.lower().strip()
        cg.send('Acting on: {} w/ msg: {}'.format(operation, self.msg))
        """Determine the proper action based on the arguments"""
        if re.match(operation, 'test'):
            self._mjr('Starting tests!')
            tests.t_hw()  # just hello world
            # tests.t_weather()  # *watch the 1 min. API limit
        elif re.match(operation, 'alarm'):
            self._mjr('Starting alarm!')
            alarm.run()
        elif re.match(operation, 'all_off'):
            self._mjr('Deactivating all pins')
            all_off.run()
        elif re.match(operation, 'lcd'):
            self._mjr('Updating Character lcd!')
            self.lcd_logic(args)
        elif re.match(operation, 'status'):
            self._mjr('Starting status!')
            arg = cg.dict_arg(args, "arg")
            if arg:
                status.run(arg)
            else:
                status.set_LED_state()
        else:
            self._mjr('Error: No known op for: {}'.format(self.msg))
        # if any(re.match("weather", arg) for arg in args):

    def _mjr(self, msg):
        """Easy extra line-break print"""
        # cg.send('\n{}\n'.format(msg))
        cg.send('<*> {}'.format(msg))

    def resume(self):
        """Restart the LCD display at some delay"""
        _delay = int(round(self.delay * 60))
        cg.send('Delaying Weather-LCD updates for {}sec'.format(_delay))
        sleep(_delay)
        cg.send('Resuming weather LCD updates')
        lcd.cycle_weather()

    def lcd_logic(self, args):
        """Toggle LCD back light / new text"""
        cg.send('LCD Args: {}'.format(self.msg))
        disp = cg.dict_arg(args, "display")
        if disp:
            lcd.brightness(disp)
        msg = cg.dict_arg(args, "message")
        if msg:
            # Prep the display for before/after the message
            lcd.stop_weather()
            delay = cg.dict_arg(args, "delay")
            try:
                self.delay = float(delay)
            except:  # noqa
                self.delay = 1
            lcd.text(msg)
            cg.thread(self.resume)
        start = cg.dict_arg(args, "start")
        if start:
            lcd.cycle_weather()
        # insomnia = cg.dict_arg(args, "insomnia")
        # if insomnia:
        #     cg.send('INSOMNIA! Everything is running')


class read_input():
    """
    Open read line that parses input in format:
        [`cmd`] @>`key`:>>`value` @>`key`:>>`value` ...etc
    """

    def __init__(self):
        self.op_regex = ur'.*\[([^\]]*)\].*'
        self.parsed_sysarg = False

        # Initialize the clock (GND, VCC=3.3V)
        clock = cg.get_pin('7Segment', 'clk')
        digital = cg.get_pin('7Segment', 'dio')
        if cg.is_pi():
            Display = tm1637.TM1637(CLK=clock, DIO=digital, brightness=1.0)
            Display.StartClock(military_time=True)
        else:
            cg.send('Would run TM1637 w/ C:{}, D:{}'.format(clock, digital))
        all_off.run()
        # Toggle display based on time of day
        evening = int(datetime.datetime.now().hour) >= 20
        lcd.brightness('off') if evening else lcd.brightness('on')

    def start(self):
        """Loop indefinitely"""
        while True:
            # Accept an optional sys arg or open a readline prompt
            #   Warn: The sysarg must be escaped with single quotes
            #   python main.py '[lcd] @>start'
            if not self.parsed_sysarg and len(sys.argv) > 1:
                message = ''
                for arg_num in range(len(sys.argv) - 1):
                    arg_num += 1
                    message += ' {}'.format(cg.parse_argv(sys, arg_num))
                self.parsed_sysarg = True
            else:
                try:
                    message = sys.stdin.readline()
                except KeyboardInterrupt:
                    sys.exit()
                    # raise Exception('Trying to exit the app?')
            self.message = message.strip()
            cg.send('Raw Message: {}'.format(message))
            if not re.match(self.op_regex, self.message):
                raise ValueError('Argument passed does not have proper format')
            else:
                self.parse_input()

    def parse_input(self):
        # Parse the arguments received
        chunks = self.message.split('@>')

        # Parse operation and remove brackets:
        # operation = chunks[0].strip()[1:-1]
        matches = re.finditer(self.op_regex, chunks[0])
        # 'next' - hack for iterable obj
        operation = next(matches).group(1)
        cg.send('Running Operation: {}'.format(operation))

        def parse(y):
            return y.split(':>>') if ':>>' in y else [y, 'N/A']

        # Organize the args into a dict:
        if len(chunks) > 1:
            te = cg.try_eval  # shorthand the f_name
            args = [parse(x) for x in chunks[1:]]
            _arg = '{'
            for arg in args:
                _arg += '"{}": "{}",'.format(te(arg[0]), te(arg[1]))
            arguments = _arg[:-1] + '}'
            cg.send('w/ Args: {}'.format(arguments))
            try:
                arguments = te(arguments)
            except:  # noqa
                raise ValueError('Could not eval({})'.format(arguments))
        else:
            arguments = ''
        # Decide on the appropriate action:
        action_input(operation, arguments, self.message)


# Point of Entry
if __name__ == "__main__":
    # FIXME/TODO: Is this unnecessary?
    # pth = './Python/modules/status'
    # shutil.copyfile('{}.py'.format(pth), '{}_alt.py'.format(pth))
    # cg.send('Duplicating Status File: {}'.format(pth))
    #
    read_input().start()
