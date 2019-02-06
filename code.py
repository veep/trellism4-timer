# Trellis M4 Timer - Simple visual timer for Trellis M4
# Written by Eric Prestemon, ecp@prestemon.com  2019
# This is free and unencumbered software released into the public domain.

import time
import adafruit_trellism4
import random

trellis = adafruit_trellism4.TrellisM4Express(rotation=270)
trellis.pixels.fill((0,0,0))

SECONDS=60*60
DIVISIONS=12
COLUMNS=trellis.pixels.width
BRIGHTNESS=100

timer_running = False

width = trellis.pixels.width
height = trellis.pixels.height


def draw_idle():
    trellis.pixels[width-2,height-2] = (0,20,0)
    trellis.pixels[width-1,height-2] = (0,20,0)
    trellis.pixels[width-2,height-1] = (0,20,0)
    trellis.pixels[width-1,height-1] = (0,20,0)

def draw_timer_start():
    trellis.pixels.fill((0,0,0))
    trellis.pixels[width-2,height-2] = (20,0,0)
    trellis.pixels[width-1,height-2] = (20,0,0)
    trellis.pixels[width-2,height-1] = (20,0,0)
    trellis.pixels[width-1,height-1] = (20,0,0)

def draw_fractional(fraction):
    for cell in range(DIVISIONS):
        x = cell % COLUMNS
        y = int((cell-x)/COLUMNS)
        if (fraction < cell/DIVISIONS):
            trellis.pixels[x,y] = (0,0,0)
        elif fraction > ((cell+1)/DIVISIONS):
            trellis.pixels[x,y] = (0,BRIGHTNESS,BRIGHTNESS)
        else:
            prorated = int((fraction-cell/DIVISIONS)*DIVISIONS*BRIGHTNESS)
            trellis.pixels[x,y] = (prorated, prorated, prorated)
            
def draw_full(count,bottom_left_x,bottom_left_y):
    for column in range(4):
        if (count >= (4-column)*5):
            trellis.pixels[bottom_left_x+column,bottom_left_y-1] = (0,0,100)
        else:
            trellis.pixels[bottom_left_x+column,bottom_left_y-1] = (0,0,0)
        if ((count % 5) >= (4-column)):
            trellis.pixels[bottom_left_x+column,bottom_left_y] = (50,0,50)
        else:
            trellis.pixels[bottom_left_x+column,bottom_left_y] = (0,0,0)
            
draw_idle()
while True:
    if timer_running:
        run_time = time.monotonic()-start_time
        fractional_time = run_time % SECONDS
        draw_fractional(fractional_time/SECONDS)
        draw_full(int(run_time/SECONDS),0,5)
        
        pressed = trellis.pressed_keys
        if pressed:
            draw_idle()
            print (int(run_time/3600),'hours',int ((run_time %3600)/60), 'minutes',int(run_time %60),'seconds')
            timer_running = False
            time.sleep(0.5)
    else:
        pressed = trellis.pressed_keys
        if pressed:
            draw_timer_start()
            timer_running = True
            start_time = time.monotonic()
            time.sleep(0.5)
    time.sleep(0.1)

    
            
    
    

# Don't write auto-backups, since I'm usually working directly in device directory
    
# Local Variables:
# backup-inhibited: t
# eval: (auto-save-mode -1)
# End:
