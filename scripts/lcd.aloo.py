# !/usr/bin/python

# import time
# lcd_columns = 16


# def full_message(message):
#     if len(message) < lcd_columns:
#         # Normal Method
#         print(message)
#     elif len(message) <= 2 * lcd_columns:
#         # Split into two rows
#         first_line = message[:lcd_columns]
#         second_line = message[lcd_columns:]
#         print(first_line + "\n" + second_line)
#     else:
#         print(message)


# def pausebreak():
#     """Separate Manual Tests"""
#     print('------------')
#     time.sleep(.5)

# # Manual Tests
# full_message('Very long Message to Test Maximum String Allowed')
# pausebreak()
# full_message('Two Line Message That Bad Cuts')
# pausebreak()
# full_message('Long Two Line Message Cuts off')
# pausebreak()
# full_message('One Line Message')

AllKLB = 0
ALOO = "is really cool wow shark"
ice_cream_kangaroo_bike = ALOO.split(" ")
# Sample Code:
for i in range(len(ice_cream_kangaroo_bike)):
    KLB = len(ice_cream_kangaroo_bike[i])
    AllKLB = AllKLB + KLB
    # if ALLKLB = 14,
    #   KLB is = 3, then make newline, but if KLB = 2, keep on same line
    i = i + 1
