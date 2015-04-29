#!/usr/bin/python

#Built-in Imports
import time
import sys

#Libraries
import RPi.GPIO as GPIO
import neopixel as npx
import sim_finalv1 as ffs

# Global for hardware system
PINS = [18, 27, 23, 25]
KEEP_GOING = True
last_press = 10
strip_handle = []
period_range = 1.0
mode = 0
ff_num = 0
strip_num = 0
next_grid = None

def runner(grid):
    #update state of all ffs
    global strip_handle
    grid.update_state()

    #check who blinked
    for i in xrange(grid.groups):
        for j in xrange(grid.group_size):
            strip_handle[i].setPixelColorRGB(j, grid.FFs[i][j].brightnessR, grid.FFs[i][j].brightnessG, 0) #grid.FFs[i][j].brightnessB)

    #update strip
    for i in xrange(grid.groups):
        strip_handle[i].show()

def take_user_input(current_grid):
    print "taking input"
    global KEEP_GOING
    KEEP_GOING = True

    while KEEP_GOING:
        runner(current_grid)
        time.sleep(.035)
    
    print "starting over"
    return True

def input_handler(pin):
    press = time.time()
    print "Got a press"
    global last_press
    since = press - last_press
    if since > 10:
        last_press = press
    else:
        run_again(since)

def run_again(since):
    global KEEP_GOING
    global strip_num
    global ff_num
    global mode
    global next_grid
    if mode == 1:
        if since <= .7:
            my_min = since - .2
        else:
            my_min = since - .4
        next_grid = ffs.GridAdapt(ff_num, strip_num, .6, .2, since, since + .5, my_min, .035)
        KEEP_GOING = False
    else:
        global period_range
        next_grid = ffs.GridLock(ff_num, strip_num, since, period_range, .035)
        KEEP_GOING = False

#Expects to run with 2 arguments:
#num of strips and num of ff's per strip
def make_sim():
    #Grab input arguments
    global mode
    global ff_num
    global strip_num

    mode = int(raw_input("What mode would you like to run in?: \n1. Phase Adapt \n2. Phase Lock\n"))

    if mode == 1:
        ff_num = int(raw_input("How many fireflies are on a strip?:  "))
        strip_num = int(raw_input("How many strips?:  "))
        stim_w = float(raw_input("Stimulus Period?:  "))
        A_min = .2
        A_max = .7
        if stim_w <=.7:
            w_min = stim_w - .2
        else:
            w_min = stim_w - .5
        w_max = stim_w + .5
        # A_min = float(raw_input("Minimum Reset Strength A?:  "))
        # A_max = float(raw_input("Maximum Reset Strength A?:  "))
        # w_min = float(raw_input("Minimum Period:  "))
        # w_max = float(raw_input("Maximum Period?:  "))
        # update_time = float(raw_input("What time step would you like to use? (takes about .02s to clear GPIO buffer):  "))
        # t_up = float(raw_input("Blink up time?:  "))
        # t_down = float(raw_input("Blink down time?:  "))
    else:
        ff_num = int(raw_input("How many fireflies are on a strip?:  "))
        strip_num = int(raw_input("How many strips?:  "))
        stim_w = float(raw_input("Stimulus Period?:  "))
        T_range = 1.0
        # T_range = float(raw_input("What range do you want for follow flies?:  "))

    try: 
        PINS[strip_num - 1]
    except IndexError:
        print "You're trying to use too many strips given the set pins"
        print "Consider changing the pin settings or chaining your strips\n\n"

    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(21, GPIO.RISING, input_handler, 500)
    
    #Create Strip Objects
    global strip_handle
    for i in range(strip_num):
        next_strip = npx.Adafruit_NeoPixel(ff_num, PINS[i])
        strip_handle.append(next_strip)
        next_strip.begin()

    if mode == 1:
        current_grid = ffs.GridAdapt(ff_num, strip_num, A_max, A_min, stim_w, w_max, w_min, .035)
    else:
        current_grid = ffs.GridLock(ff_num, strip_num, stim_w, T_range, .035)

    while take_user_input(current_grid):
        global next_grid
        current_grid = next_grid

    GPIO.cleanup()

if __name__ == '__main__':
    make_sim()

