import subprocess, sys
import time
from tkinter import *
from PIL import Image, ImageTk

# gui
root=Tk()
root.minsize(1280, 720)
root.title('Touchpad ')
win1_img = ImageTk.PhotoImage(Image.open('./win1.jpg'))
win1_loc_x = 0
win1_loc_y = 0
win1_last_loc_x = 0
#c_w_diff_x = 0
#c_w_diff_y = 0
win1 = Label(root, image=win1_img)
win1.pack()
win1.image=win1_img
win1.place(x=0, y=0)
win2_img = ImageTk.PhotoImage(Image.open('./win2.jpg'))
win2_loc_x = 1280
win2_loc_y = 0
#c_w_diff_x = 0
#c_w_diff_y = 0
win2 = Label(root, image=win2_img)
win2.pack()
win2.image=win2_img
win2.place(x=1280, y=0)
initial_4_f_drag_x_is_get = 0
initial_4_f_drag_y_is_get = 0
x_text = StringVar()
Label(root, textvariable=x_text).pack()
x_text.set("X:           ")
y_text = StringVar()
Label(root, textvariable=y_text).pack()
y_text.set("Y:           ")
f_text = StringVar()
Label(root, textvariable=f_text).pack()
f_text.set("Fingers:     ")
c_last_loc_x = 640
c_last_loc_y = 360
c_loc_x = 640
c_loc_y = 360
click = StringVar()
cursor=Label(root, textvariable=click)
click.set("X")
cursor.pack()
cursor.place(x=c_last_loc_x, y=c_last_loc_y)

# command to get data from trackpad
cmd = "evtest /dev/input/event9"

# run it
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
# some predefined variables
fingers = []
origin_x = 0
origin_y = 0
is_touching_int = 0
is_pressing_int = 0
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
        
        '''
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
        else:
            if "EV_ABS" in outstr:
                fingers.append(1)
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
        
        pos = -1
        '''

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
        
        # Finger count (new)
        if len(fingers) > 10:
            fingers[:1] = []

        if "ABS_MT_SLOT" in merge:
            check_finger_4 = merge.find("(ABS_MT_SLOT), value 3")
            check_finger_3 = merge.find("(ABS_MT_SLOT), value 2")
            check_finger_2 = merge.find("(ABS_MT_SLOT), value 1")
            if check_finger_4 != -1:
                fingers.append(4)
            else:
                if check_finger_3 != -1:
                    fingers.append(3)
                else:
                    if check_finger_2 != -1:
                        fingers.append(2)
        else:
            fingers.append(1)
        
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


        # Click detection
        pos = merge.find("BTN_LEFT")
        posx = merge.find("'", pos)
        if pos != -1:
            is_pressing = merge[pos+17:posx]
            if is_pressing is "1":
                #print("pressing")
                is_pressing_int = 1
                click.set("x")
            elif is_pressing is "0":
                #print("unpressed")
                is_pressing_int = 0
                click.set("X")
    
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
            c_loc_x = c_last_loc_x + x_int - origin_x
            c_loc_y = c_last_loc_y + y_int - origin_y
            cursor.place(x=c_loc_x, y=c_loc_y)
        elif is_touching_int is 0:
            origin_x = x_int
            initial_x_is_get = 0
            origin_y = y_int
            initial_y_is_get = 0
            fingers = []
            c_last_loc_x = c_loc_x
            c_last_loc_y = c_loc_y
            initial_4_f_drag_x_is_get = 0
            if win1_last_loc_x > - 640:
                win1_last_loc_x = 0
                win1.place(x=0 , y=0)
                win2.place(x=1280 , y=0)
            elif win1_last_loc_x <= -640:
                win1_last_loc_x = -1280
                win1.place(x=-1280 , y=0)
                win2.place(x=0 , y=0)
        
        
        '''
           if 0 > win1_last_loc_x > - 640:
                for smooth_x in range(win1_last_loc_x, 0):
                    win1_last_loc_x = smooth_x
                    win1.place(x=smooth_x , y=0)
                    win2.place(x=1280 + smooth_x , y=0)
                    smooth_x += 1
                    print(smooth_x)
                    time.sleep(0.0001)
                    root.update()
            elif win1_last_loc_x <= -640:
                for smooth_x in range(-1280 , win1_last_loc_x):
                    win1_last_loc_x = smooth_x
                    win1.place(x=smooth_x , y=0)
                    win2.place(x=1280 + smooth_x , y=0)
                    smooth_x += 1
                    print(smooth_x)
                    time.sleep(0.0001)
                    root.update()
            '''   

        '''
        # Dragging
        if is_pressing_int == 1:
            if win_loc_x < c_loc_x < (win_loc_x + 766) and win_loc_y < c_loc_y < (win_loc_y + 423):
                print(win_loc_x)
                c_w_diff_x = c_loc_x - win_loc_x
                c_w_diff_y = c_loc_y - win_loc_y
                win_loc_x = c_loc_x - c_w_diff_x
                win.place(x=win_loc_x , y=c_loc_y - c_w_diff_y)
                win.image=ph
        '''

        # Switching windows
        if finger_count == 3:
            if initial_4_f_drag_x_is_get == 0:
                f_swipe_start_x = c_loc_x - win1_last_loc_x
                f_swipe_start_y = c_loc_y
                initial_4_f_drag_x_is_get = 1
            win1_loc_x = c_loc_x
            win1_last_loc_x = c_loc_x - f_swipe_start_x
            win1.place(x= win1_last_loc_x , y=0)
            win2.place(x=1280 + win1_last_loc_x , y=0)


        # When default finger released from trackpad it causes jump to mitigate it i will change reference when finger number is decreased


    #print(merge)
    merge = "Start"
    root.update()            