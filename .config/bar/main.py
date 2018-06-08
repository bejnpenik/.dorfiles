#! /usr/bin/env python
from datetime import datetime
from barstatus import BarStatus
from bspccontrol import BspcControl
from threading import Thread
import re
import subprocess
from time import strftime
from time import sleep

bar = BarStatus()

    
    
def getcurrenttime():
    current_time = strftime("%H:%M")
    bar.time = " " + current_time + " "
def getvolume():
    volume = subprocess.check_output(("/home/branislav/.config/tint2/volume.sh")).decode("utf-8").strip().splitlines()[-1]
    bar.volume = " VOL " + volume+" "
def gettaskbaritems():
    root_items = subprocess.check_output(('xprop', "-root")).decode("ascii").strip().splitlines()
    net_client_list = None
    active_id = None
    for line in root_items:
        try:
            name, value = line.split(":")
        except:
            name, value = None, None
        if name == '_NET_CLIENT_LIST(WINDOW)':
            net_client_list = value.split("#")[-1].split(",")
        if name == '_NET_ACTIVE_WINDOW(WINDOW)':
            active_id = value.split("#")[-1]
    all_windows = []
    for item in net_client_list:
        if item==active_id:
            all_windows.append("A"+item)
        else:
            all_windows.append(item)
    #print(all_windows)


    client_instance = []
    taskbar = ""
    if all_windows:
        for item in all_windows:
            is_window = False
            is_active = False
            if item.startswith("A"):
                item = item[1:]
                is_active = True
            try: 
                window_class, window_instance, window_name = subprocess.check_output(("xwinfo", item, "-c", "-i", "-n")).decode("ascii").strip().splitlines()
                is_window = True
            except:
                is_window = False
                window_class, window_instance, window_name = None, None, None
            if is_window:
                if is_active:
                   
                    client_instance.append(("A" + window_name,"A" + window_class, item))
                else:
                    client_instance.append((window_name, window_class, item))
        active_instance = None
        if active_id:
            is_client = False
            try:
                window_class, window_instance, window_name = subprocess.check_output(("xwinfo", active_id, "-c", "-i", "-n")).decode("ascii").strip().splitlines()
                is_client = True
            except:
                is_client = False
            if is_client:
                active_instance = window_instance
        taskbar = ""
        for item_instance, item_name, item in client_instance:
            if len(client_instance) >= 10 and len(client_instance)<30:
                taskbar += " | [" + item_name + "] "  + item_instance[:10] + "| "
            elif len(client_instance)>=30:
                taskbar += "| [" + item_name + "] "
            else:
                if item_instance.startswith("A"):
                    taskbar += "%{R}"
                    taskbar += " | [" + item_name[1:] + "] " + item_instance[1:] + "| "
     
                    taskbar += "%{R}"
                else:
                    taskbar += "%{A1:xdo activate"+item + ":}%{A3:xdo close"+item+":}| [" + item_name[:] + "] " + item_instance[:5] + "...| %{A}%{A}"






    bar.taskbar = taskbar
     
        
def main():
    while True:
        getcurrenttime()
        gettaskbaritems()
        

#Start continious jobs
bspccontrol = BspcControl(bar)
Thread(target=bspccontrol.inputhandler).start()
while True:
    getcurrenttime()
    #getvolume()
    sleep(1)
