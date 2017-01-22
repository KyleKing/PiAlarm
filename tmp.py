last_beep = 0
counter = 0
while counter < 4:
    if counter % 2 <= 1 and last_beep == 0:
        print 'new buzz {}'.format(counter)
        last_beep = 0.2
    elif counter % 2 > 1 and last_beep == 0.2:
        print 'NO buzz {}'.format(counter)
        last_beep = 0
    counter += 0.1
