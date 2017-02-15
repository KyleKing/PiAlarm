# -*- coding: utf-8 -*-
import re
import sys

# import display_controller as d_con
from modules import config as cg
from modules import tests, alarm, lcd

cg.quiet_logging(False)


class action_input():

    def __init__(self, operation, args, message=''):
        self.msg = message
        """Determine the proper action based on the arguments"""
        if re.match(operation, 'test'):
            self.mjr('Starting tests!')
            tests.t_hw()  # just hello world
            # tests.t_weather()  # *watch the 1 min. API limit

        elif re.match(operation, 'alarm'):
            self.mjr('Starting alarm!')
            alarm.run()

        elif re.match(operation, 'lcd'):
            self.mjr('Updating Character lcd!')
            self.lcd_logic(args)

        elif re.match(operation, 'status'):
            self.mjr('Starting status!')
            cg.send()

        else:
            self.mjr('Error: No known op for: {}'.format(self.msg))
        # if any(re.match("weather", arg) for arg in args):

    def mjr(self, msg):
        cg.send('\n{}\n'.format(msg))

    def exist(self, args, key):
        try:
            return args[key]
        except:
            cg.send('{} not found in `{}`'.format(key, args))
            return False

    def lcd_logic(self, args):
        print 'LCD....{}'.format(self.msg)
        disp = self.exist(args, "display")
        msg = self.exist(args, "message")
        run = self.exist(args, "run")
        if disp:
            lcd.disp(disp)
        if msg:
            lcd.custom_msg(msg)
        if run:
            lcd.run()


class try_eval():

    def val(self, raw):
        """Try to find a True/False, Integer, etc. value in str input"""
        raw = raw.strip()
        try:
            return eval(raw)
        except:
            return raw


class read_input():

    def __init__(self):
        self.op_regex = ur'.*\[([^\]]*)\].*'
        self.parsed_sysarg = False

    def start(self):
        while True:
            self.check()

    def check(self):
        # Accept an optional sys arg or open a readline prompt
        if not self.parsed_sysarg and len(sys.argv) > 1:
            message = ''
            for arg_num in range(len(sys.argv) - 1):
                arg_num += 1
                message += ' {}'.format(cg.parse_argv(sys, arg_num))
            self.parsed_sysarg = True
        else:
            message = sys.stdin.readline()
        message = message.strip()
        print 'Raw Message: {}'.format(message)

        # Parse the arguments received
        if not re.match(self.op_regex, message):
            raise ValueError('Argument passed does not have proper format')
        else:
            chunks = message.split('@')

            # Parse operation and remove brackets:
            # operation = chunks[0].strip()[1:-1]
            matches = re.finditer(self.op_regex, chunks[0])
            # 'next' - hack for iterable obj
            operation = next(matches).group(1)
            cg.send('Running Operation: {}'.format(operation))

            # Organize the args into a dict:
            if len(chunks) > 1:
                te = try_eval()
                args = [x.split(':') for x in chunks[1:]]
                _arg = '{'
                for arg in args:
                    _arg += '"{}": "{}",'.format(
                        te.val(arg[0]), te.val(arg[1]))
                arguments = _arg[:-1] + '}'
                cg.send('w/ Args: {}'.format(arguments))
                try:
                    arguments = te.val(arguments)
                except:
                    raise ValueError('Could not eval({})'.format(arguments))
            else:
                arguments = ''
            # Decide on the appropriate action:
            action_input(operation, arguments, message)


#
# Point of Entry
#


# d_con.start()
read_input().start()
