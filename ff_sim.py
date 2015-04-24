#!/usr/bin/python
import numpy as np

class FireFlyAdaptive:
    
    # Firefly period is set in seconds
    def __init__(self, T, A):
        self.T = T
        self.w0 = ((2*np.pi)/T)
        self.wn = ((2*np.pi)/T)
        self.A = A
        self.theta = -np.pi
        self.theta1 = -1
        self.blink = 0
        self.brightnessR = 0
        self.brightnessG = 0
        self.count = 0
        self.b_up = .3 
        self.b_down = .4
        self.R_colors_up = np.linspace(0, 160, round(.3/t)+1)
        self.R_colors_down = np.linspace(0, 160, round(.4/t)+1)
        self.G_colors_up = np.linspace(0, 250, round(.3/t)+1)
        self.G_colors_down = np.linspace(0, 250, round(.4/t)+1)

    def next_state(self, t):
        self.theta1 = self.theta + self.wn * t
        if (np.sin(self.theta) < 0) and (np.sin(self.theta1) >= 0):
            self.blink = 1
            self.brightnessR = 1
            self.brightnessG = 1
        self.theta = self.theta1

        if self.blink == 1:
            self.count += 1
            self.brightnessR = int(self.R_colors_up[self.count])
            self.brightnessG = int(self.G_colors_up[self.count])
            if self.count >= self.b_up:
                self.blink = 0
                self.count = self.b_down
        elif self.count > 0:
            self.count -= 1 
            self.brightnessR = int(self.R_colors_down[self.count])
            self.brightnessG = int(self.G_colors_down[self.count])

                

    def update(self, theta_stim):
        self.wn = self.wn + (self.A * np.sin(theta_stim - self.theta1))


class FireflyLock():

    def __init__(self, T, T_min, T_max, t)
        self.T = T
        self.w0 = ((2*np.pi)/T)
        self.wn = ((2*np.pi)/T)
        self.wmin = ((2*np.pi)/T_min) 
        self.wmax = ((2*np.pi)T_max) 
        self.theta = -np.pi
        self.theta1 = -1
        self.blink = 0
        self.brightnessR = 0
        self.brightnessG = 0
        self.count = 0
        self.b_up = .3 
        self.b_down = .4
        self.R_colors_up = np.linspace(0, 160, round(.3/t)+1)
        self.R_colors_down = np.linspace(0, 160, round(.4/t)+1)
        self.G_colors_up = np.linspace(0, 250, round(.3/t)+1)
        self.G_colors_down = np.linspace(0, 250, round(.4/t)+1)
        #time of system updates
        self.t = t

        def next_state(self):
            self.theta1 = self.theta + self.wn*self.t
            if (np.sin(self.theta) < 0) and np.sin(self.theta1) >= 0):
                self.blink = 1

            self.brightnessR = 1
            self.brightnessG = 1
            self.theta = self.theta1

            if self.blink == 1:
                self.count += 1
                self.brightnessR = int(self.R_colors_up[self.count])
                self.brightnessG = int(self.G_colors_up[self.count])
                if self.count >= self.b_up:
                    self.blink = 0
                    self.count = self.b_down
            elif self.count > 0:
                self.count -= 1 
                self.brightnessR = int(self.R_colors_down[self.count])
                self.brightnessG = int(self.G_colors_down[self.count])

        def update(self):
            self.wn = self.wn + (np.log(self.w0/self.wn)*.1) + \
                ( max( np.sin(self.theta1), 0 ) * (self.wmin - self.wn) ) - \
                ( min( np.sin(self.theta1), 0 ) * (self.wmax - self.wn) )

            
class Grid():
    """
    Handles the state for a grid of fireflies 
    Meant to be simulated with WS2812's connected

    Needs update frequency, style of pulse-locking, number of fireflies
    Strip Numbers and lengths are needed, too (for now)
    """

    def __init__(self, strip_length, num_strips, w_stim, w_max, w_min, t):
        #set up arrays
        #generate max and min periods for each FF
        #make array a property of self
        self.per_strip = strip_length
        self.groups = num_strips
        self.FFs = {}
        
    def update_state(self):
        #Run the state update


#Expects number of FF's to evenly divide into strips
#This is because this is meant to work with LED or other lighting strips
#Thus, if you ask for more FF's than LEDs, we need to pitch a few (or do unnecessary computational work)
def make_ff_array(strip_length, num_strips, A_max, A_min, w_stim, w_max, w_min, t):

    ff_arrays = {}

    ff_arrays['stim'] = FireFly(w_stim, A_min, up, down, R_colors_up, R_colors_down, G_colors_up, G_colors_down)
    for i in xrange(num_strips):
        ff_strip = []
        for j in range(strip_length):
            _w = (np.random.random() * (w_max - w_min)) + w_min
            _A = (np.random.random() * (A_max - A_min)) + A_min

            next_ff = FireFly(_w, _A, up, down, R_colors_up, R_colors_down, G_colors_up, G_colors_down)
            ff_strip.append(next_ff)
        ff_arrays[i] = ff_strip
   OA return ff_arrays

def update_state(ff_array, t, num_strips, strip_length):
    phase1 = ff_array['stim'].theta
    ff_array['stim'].next_state(t)
    phase2 = ff_array['stim'].theta1
    for i in xrange(num_strips):
        for j in xrange(strip_length):
            ff_array[i][j].next_state(t)
    if (np.sin(phase1) < 0) and (np.sin(phase2) >= 0):
        for i in xrange(num_strips):
            for j in xrange(strip_length):
                ff_array[i][j].update(phase2)
    return ff_array
