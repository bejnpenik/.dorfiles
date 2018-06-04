import subprocess
"""

Each report event message is composed of items separated by colons.

Each item has the form <type><value> where <type> is the first character of the item.

M<monitor_name>

    Focused monitor.
m<monitor_name>

    Unfocused monitor.
O<desktop_name>

    Occupied focused desktop.
o<desktop_name>

    Occupied unfocused desktop.
F<desktop_name>

    Free focused desktop.
f<desktop_name>

    Free unfocused desktop.
U<desktop_name>

    Urgent focused desktop.
u<desktop_name>

    Urgent unfocused desktop.
L(T|M)

    Layout of the focused desktop of a monitor.
T(T|P|F|=|@)

    State of the focused node of a focused desktop.
G(S?P?L?)

    Active flags of the focused node of a focused desktop.

"""
class BspcControl:
    START_TAG = "W"
    MONITOR_FOCUSED_TAG = "M"
    MONITOR_UNFOCUSED_TAG = "m"
    MONITOR_LAYOUT_TAG = "L"
    NODE_STATE_TAG = "T"
    NODE_ACTIVE_TAG = "G"
    DESKTOP_OCCUPIED_FOCUSED_TAG = "O"
    DESKTOP_OCCUPIED_UNFOCUSED_TAG = "o"
    DESKTOP_FREE_FOCUSED_TAG = "F"
    DESKTOP_FREE_UNFOCUSED_TAG = "f"
    DESKTOP_URGENT_FOCUSED_TAG = "U"
    DESKTOP_URGENT_UNFOCUSED_TAG = "u"
    def __init__(self, bar):
        self.bar = bar
        self.bspc = subprocess.Popen(('bspc', 'subscribe', 'report'), stdout=subprocess.PIPE)
        self.monitors = []


    def inputhandler(self):
        while True:
            input = self.bspc.stdout.readline().decode('ascii').strip()[1:]
            self.monitors = []
            self.parseline(input)

    def parseline(self,line):

        split = line.split(':')
        for item in split:
            self.parseitem(item)
        self.outputbar()
    def parseitem(self, item):
        monitor_item = item.startswith(BspcControl.START_TAG) or item.startswith(BspcControl.MONITOR_FOCUSED_TAG) or item.startswith(BspcControl.MONITOR_UNFOCUSED_TAG)
        monitor_layout = item.startswith(BspcControl.MONITOR_LAYOUT_TAG)
        node_state = item.startswith(BspcControl.NODE_STATE_TAG)
        node_active = item.startswith(BspcControl.NODE_ACTIVE_TAG)
        if monitor_item:
            if item.startswith(BspcControl.MONITOR_FOCUSED_TAG) or item.startswith(BspcControl.MONITOR_UNFOCUSED_TAG):
                self.monitors.append(Monitor(item[1:], item[:1]))
            else:
                self.monitors.append(Monitor(item[2:], item[1:2]))
        elif monitor_layout or node_active or node_state:
            pass
        else:
            self.monitors[-1].add_desktop(Desktop(item[1:], item[:1]))

    def outputbar(self):
        self.bar.setmonitors(self.monitors)

    def __str__(self):
        return 'Test'

class Monitor:
    def __init__(self, name, status):
        self.name = name
        self.desktops = []

    def add_desktop(self, desktop):
        self.desktops.append(desktop)

    def __str__(self):
        returnstring = 'Monitor: ' + self.name + '\n'
        for desktop in self.desktops:
            returnstring += str(desktop) + '\n'
        return returnstring

class Desktop:
    def __init__(self, name, status):
        self.name = name
        if status == 'F':
            self.active = True
            self.used = False
            self.urgent = False
        elif status == 'f':
            self.active = False
            self.used = False
            self.urgent = False
        elif status == 'o':
            self.active = False
            self.used = True
            self.urgent = False
        elif status == "U":
            self.active = True
            self.used = True
            self.urgent = True
        elif status == "u":
            self.active = False
            self.used = True
            self.urgent = True
        else:
            self.active = True
            self.used = True
            self.urgent = False
        self.tasks = self.get_tasks()

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def __str__(self):
        return self.name + ': ' + str(self.active) + ' ' + str(self.used)
    def get_tasks(self):
        task_ids = None
        active_id = ""
        if self.used and self.active:
            active_id=None
            try:
                active_id = subprocess.check_output(("bspc", "query", "-N", "-n", "focused.window")).decode("ascii").strip()
            except Exception:
                pass
        if self.used:
            task_ids =  subprocess.check_output(("bspc", "query", "-N", "-n", ".window", "-d", self.name)).decode("ascii").strip().splitlines()
        task_names = []
        if task_ids:
            for task in task_ids:
                if self.active:
                    if task == active_id:
                        task_names.append("ACTIVEWINDOWJBT!#$%&VALDASENECEOVOPONOVITIUIMENU " + subprocess.check_output(("xtitle","-e", task)).decode("utf-8").strip()[:15]+"...")
                    else:
                        task_names.append(" "+subprocess.check_output(("xtitle","-e", task)).decode("utf-8").strip()[:15] + "...")
                else:
                    task_names.append(" " + subprocess.check_output(("xtitle","-e", task)).decode("utf-8").strip()[:15]+"...")
 
        return task_names     
