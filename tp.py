import subprocess, sys
import time
from tkinter import *

# gui
root=Tk()
root.minsize(400, 200)
root.title('Touchpad ')
x_text = StringVar()
Label(root, textvariable=x_text).pack()
x_text.set("X:           ")
y_text = StringVar()
Label(root, textvariable=y_text).pack()
y_text.set("Y:           ")
f_text = StringVar()
Label(root, textvariable=f_text).pack()
f_text.set("Fingers:     ")
w=Label(root, text='X')
w.pack()
w.place(x=200, y=100)
# command to get data from trackpad
cmd = "evtest /dev/input/event9"

# run it
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
# some predefined variables
fingers = []
origin_x = 0
origin_y = 0
is_touching_int = 0
initial_x_is_get = 0
initial_y_is_get = 0
x_int = 0
y_int = 0
finger_count = 1
merge = "Start"

while True:
    out = p.stdout.readline().rstrip()
    outstr = str(out)
    
    # merging outputs for more reliable results
    while "MSC_TIMESTAMP" not in outstr:
        out = p.stdout.readline().rstrip()
        outstr = str(out)
        merge = merge + outstr
        
        # finger count
        if len(fingers) > 40:
            fingers[:1] = []
        
        pos = outstr.find("ABS_MT_SLOT")
        posx = outstr.find("'", pos)
        if pos != -1:
            f_count = outstr[pos+20:posx]
            if f_count == "3":
                fingers.append(4)
            elif f_count == "2":
                fingers.append(3)
            elif f_count == "1":
                fingers.append(2)
            #print("finger=" + f_count)
            #print(fingers)
            if 4 in fingers:
                #print("4 fingers")
                finger_count = 4
            elif 3 in fingers:
                #print("3 fingers")
                finger_count = 3
            elif 2 in fingers:
                #print("2 fingers")
                finger_count = 2
            else:
                #print("1 fingers")
                finger_count = 1
        else:
            if "EV_ABS" in outstr:
                fingers.append(1)
        pos = -1
    
    merge = merge + "End"
    
    # getting values from merge string
    if outstr != '':
        # x axis
        pos = merge.find("ABS_X") #14
        posx = merge.find("'", pos)
        if pos != -1:
            x_axis = merge[pos+14:posx]
            if x_axis != '':
                x_int = int(x_axis)
            #print("x=" + x_axis)
    
        pos = -1
    
        # y axis
        pos = merge.find("ABS_Y") #14
        posx = merge.find("'", pos)
        if pos != -1:
            y_axis = merge[pos+14:posx]
            if y_axis != '':
                y_int = int(y_axis)
            #print("y=" + y_axis)
    
        pos = -1

        

        # Touch detection
        pos = merge.find("BTN_TOUCH")
        posx = merge.find("'", pos)
        if pos != -1:
            is_touching = merge[pos+18:posx]
            if is_touching is "1":
                #print("touching")
                is_touching_int = 1
            elif is_touching is "0":
                #print("released")
                is_touching_int = 0
    
        pos = -1
        
        # Change in position detection
        
        if is_touching_int is 1:
            if initial_x_is_get == 0:
                if x_axis != '':
                    origin_x = x_int
                    initial_x_is_get = 1
                if y_axis != '':
                    origin_y = y_int
                    initial_y_is_get = 1
            #print(x_int - origin_x, " , ", y_int - origin_y, " , ", finger_count, fingers)
            x_text.set("X: " + str(x_int - origin_x))
            y_text.set("Y: " + str(origin_y - y_int))
            f_text.set("Fingers: " + str(finger_count))
            w.place(x=200 + x_int - origin_x, y=100 + y_int - origin_y)
        elif is_touching_int is 0:
            origin_x = x_int
            initial_x_is_get = 0
            origin_y = y_int
            initial_y_is_get = 0
            fingers = []
        
        
        
    #print(merge)
    merge = "Start"
    root.update()            