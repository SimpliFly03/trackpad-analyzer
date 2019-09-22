import subprocess, sys
import time
# command to get data from trackpad
cmd = "evtest /dev/input/event9"
 
# run it
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
# some predefined variables
fingers = []
test = 0
touchx = 0
testis = 0
x_int = 0
merge = "Start"

while True:
    out = p.stdout.readline().rstrip()
    outstr = str(out)
    
    # merging outputs for more reliable results
    while "MSC_TIMESTAMP" not in outstr:
        out = p.stdout.readline().rstrip()
        outstr = str(out)
        merge = merge + outstr
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
            #print("y=" + y_axis)
    
        pos = -1

        # finger count
        if len(fingers) > 4:
            fingers[:1] = []
        
        pos = merge.find("ABS_MT_SLOT")
        posx = merge.find("'", pos)
        if pos != -1:
            f_count = merge[pos+20:posx]
            if f_count == "3":
                fingers.append(4)
            elif f_count == "2":
                fingers.append(3)
            elif f_count == "1":
                fingers.append(2)
            #print("finger=" + f_count)
            #print(fingers)
            if 4 in fingers:
                print("4 fingers")
            elif 3 in fingers:
                print("3 fingers")
            elif 2 in fingers:
                print("2 fingers")
        pos = -1

        # Touch detection
        pos = merge.find("BTN_TOUCH")
        posx = merge.find("'", pos)
        if pos != -1:
            is_touching = merge[pos+18:posx]
            if is_touching is "1":
                print("touching")
                touchx = 1
            elif is_touching is "0":
                print("released")
                touchx = 0
    
        pos = -1
        
        # Change in position detection
        if touchx is 1:
            if testis == 0:
                if x_axis != '':
                    test = x_int
                    testis = 1
            print(x_int - test)
        elif touchx is 0:
            test = x_int
            testis = 0
            #print(test)
        
    #print(merge)
    merge = "Start"
    
            
