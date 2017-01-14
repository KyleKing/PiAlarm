for pin_num in [1, 10]:
    for percent in [0, 0.2, 0.12341234]:
        # cmd = 'echo "' + str(pin_num).zfill(2) + \
        # cmd = 'echo "{:02}'.format(pin_num) + \
        #     '={0:0.2f}" > /dev/pi-blaster'.format(percent * 1.0)
        cmd = 'echo "{:02}={0:0.2f}" > /dev/pi-blaster'.format(pin_num, percent * 1.0)
        print cmd
