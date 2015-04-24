#!/usr/bin/python

#Built-in Imports
import time
import sys

#Libraries
import RPi.GPIO as GPIO
import neopixel as npx
import ff_sim as ffs

# ColorRGB = (255, 100, 0)
PINS = [18, 27, 23, 25]
KEEP_GOING = True
last_press = 10

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

def take_user_input(ff_num, strip_num, FFs, stripts, update_time):

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN)
    GPIO.add_event_detect(23, GPIO.FALLING, input_handler, 400)

    while KEEP_GOING:
        FFs = runner(ff_num, strip_num, FFs, strips, update_time)
        time.sleep(update_time)

    GPIO.cleanup()

def input_handler(pin):
    press = time.time()
    global last_press
    since = press - last_press
    if since > 10:
        last_press = press
    else:
        KEEP_GOING = False
        new_frequency(since)

def new_frequency():


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
        next_strip = npx.Adafruit_NeoPixel(ff_num, PINS[i])
        strips.append(next_strip)
        next_strip.begin()
    

    #May eventually need a reset so that memory doesn't overflow
    #Start Running
    print "Press Ctrl-C to stop at any time"
    while True:
        FFs = runner(ff_num, strip_num, FFs, strips, update_time)
        time.sleep(update_time)

    
