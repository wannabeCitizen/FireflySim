#!/usr/bin/python
import time
import sys

import neopixel as np
import ff_sim as ffs

# ColorRGB = (255, 100, 0)
PINS = [18, 27, 23, 25]

def runner(per_strip, strip, my_flies, strip_handle, t):
    #update state of all ffs
    my_flies1 = ffs.update_state(my_flies, t, strip, per_strip)

    #check who blinked
    for i in xrange(strip):
        for j in xrange(per_strip):
            strip_handle[i].setPixelColorRGB(j, my_flies1[i][j].brightnessR, my_flies1[i][j].brightnessG, 0)

    #update strip
    for i in xrange(strip):
        strip_handle[i].show()

    return my_flies1


#Expects to run with 2 arguments:
#num of strips and num of ff's per strip
if __name__ == '__main__':
    #Grab input arguments
    ff_num = int(raw_input("How many fireflies are on a strip?:  "))
    strip_num = int(raw_input("How many strips?:  "))
    stim_w = float(raw_input("Stimulus Period?:  "))
    A_min = float(raw_input("Minimum Reset Strength A?:  "))
    A_max = float(raw_input("Maximum Reset Strength A?:  "))
    w_min = float(raw_input("Minimum Period:  "))
    w_max = float(raw_input("Maximum Period?:  "))
    update_time = float(raw_input("What time step would you like to use? (takes about .02s to clear GPIO buffer):  "))
    t_up = float(raw_input("Blink up time?:  "))
    t_down = float(raw_input("Blink down time?:  "))

    try: 
        PINS[strip_num - 1]
    except IndexError:
        print "You're trying to use too many strips given the set pins"
        print "Consider changing the pin settings or chaining your strips\n\n"


    #Create FF Agents
    FFs = ffs.make_ff_array(ff_num, strip_num, A_max, A_min, stim_w, w_max, w_min, update_time, t_up, t_down)

    #Create Strip Objects
    strips = []
    for i in range(strip_num):
        next_strip = np.Adafruit_NeoPixel(ff_num, PINS[i])
        strips.append(next_strip)
        next_strip.begin()


    #May eventually need a reset so that memory doesn't overflow
    #Start Running
    print "Press Ctrl-C to stop at any time"
    while True:
        FFs = runner(ff_num, strip_num, FFs, strips, update_time)
        time.sleep(update_time)




    
