alarm_stage_time = [0, 120, 70, 60]
fade_stage = 0
fade_stages = ['pin_green', 'pin_red', 'pin_blue',
               'pin_green', 'pin_red', 'pin_blue']
time_total = alarm_stage_time[3] / len(fade_stages)


def set_PWM(fs, value):
    print('Set: ' + str(fs) + ' with ' + str(value))


def fade_led_strip(counter):
    global fade_stage
    time_step = (counter % time_total) + 1.0
    if fade_stage % 2 == 0:
        # Increment the LED value
        value = 1 - (1 / time_step)
    elif fade_stage % 2 == 1:
        # Decrement the LED value
        value = 1 / time_step
    else:
        print('Unknown fade counter value')
    set_PWM(fade_stages[fade_stage], value)
    if time_step == time_total:
        fade_stage += 1


# Test
for counter in range(20):
    # print(((counter % 2) + 0.0) / 2)
    fade_led_strip(counter)
