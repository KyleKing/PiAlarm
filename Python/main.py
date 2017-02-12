# -*- coding: utf-8 -*-
import re
import sys

# import display_controller as d_con
from modules import config as cg
from modules import tests

cg.quiet_logging(False)

# if any(re.match("weather", arg) for arg in args):

# def lcd_logic(message):
#     if 'display:on' in message:
#         set_disp(*default_b)
#         cg.send('Turned display on')
#     elif 'display:off' in message:
#         set_disp(*off_b)
#         cg.send('Turned display off')
#     else:
#         try:
#             # Accept a message already in a list (i.e. ['1','2'])
#             segments = eval(message)
#             if len(segments) == 2:
#                 segments.insert(1, ext(lcd_columns))
#             elif len(segments) > 2:
#                 flip(segments)
#             comp = ''
#             for segment in segments:
#                 comp += segment + ext(lcd_columns - len(segment))
#             # cg.send('Received pre-parsed message: ' + comp)
#         except:
#             # Otherwise parse whatever string was sent
#             comp = parse_message(message)
#             # cg.send('Auto-parsed message: {}'.format(comp))
#         lcd.clear()
#         lcd.message(comp)
#     sys.stdout.flush()

# d_con.start()
op_regex = ur'\[([^\]]*)\].*'
parsed_sysarg = False

while True:
    if not parsed_sysarg and len(sys.argv) > 1:
        message = cg.parse_argv(sys)
        parsed_sysarg = True
    else:
        # [run] |arg:value |var:this is useful |jade:15,40,56
        message = sys.stdin.readline().rstrip()
        print message

    if not re.match(op_regex, message):
        print 'Argument passed does not have proper format'
        # raise ValueError('Argument passed does not have proper format')
    else:
        chunks = message.split('|')
        # Remove brackets:
        # operation = chunks[0].strip()[1:-1]
        matches = re.finditer(op_regex, chunks[0])
        operation = next(matches).group(1)  # hack for iterable objects
        cg.send('Running Operation: {}'.format(operation))

        args = [x.split(':') for x in chunks[1:]]
        cg.send('w/ Args: {}'.format(args))

        if re.match(operation, 'test'):
            cg.send('Starting tests!')
            tests.t_hw()
            # tests.t_weather()
        elif re.match(operation, 'alarm'):
            cg.send('Starting alarm!')
        elif re.match(operation, 'lcd'):
            cg.send('Starting lcd!')
            # lcd_logic(args)
        elif re.match(operation, 'status'):
            cg.send('Starting status!')
            cg.send()
        else:
            cg.send('no known op for: {}'.format(message))
