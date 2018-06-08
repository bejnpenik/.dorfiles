import subprocess

class BarStatus:
    COLOR_FOREGROUND = '#616161'
    COLOR_BACKGROUND = '#1b1b1b'
    COLOR_ACTIVE_MONITOR_FG = '#FF34322E'
    COLOR_ACTIVE_MONITOR_BG = '#FF58C5F1'
    COLOR_INACTIVE_MONITOR_FG = '#FF58C5F1'
    COLOR_INACTIVE_MONITOR_BG = '#FF34322E'
    COLOR_FOCUSED_OCCUPIED_FG = '#9e9e9e'
    COLOR_FOCUSED_OCCUPIED_BG = '#303030'
    COLOR_FOCUSED_FREE_FG = '#FFF6F9FF'
    COLOR_FOCUSED_FREE_BG = '#FF6D561C'
    COLOR_FOCUSED_URGENT_FG = '#FF34322E'
    COLOR_FOCUSED_URGENT_BG = '#FFF9A299'
    COLOR_OCCUPIED_FG = '#616161'
    COLOR_OCCUPIED_BG = '#1b1b1b'
    COLOR_FREE_FG = '#FF6F7277'
    COLOR_FREE_BG = '#FF34322E'
    COLOR_URGENT_FG = '#FFF9A299'
    COLOR_URGENT_BG = '#FF34322E'
    COLOR_LAYOUT_FG = '#FFA3A6AB'
    COLOR_LAYOUT_BG = '#FF34322E'
    COLOR_UNDERLINE = "#665c54"
    COLOR_URGENT = "#752a2a"
    COLOR_TITLE_FG = '#FFA3A6AB'
    COLOR_TITLE_BG = '#FF34322E'
    COLOR_STATUS_FG = '#FFA3A6AB'
    COLOR_STATUS_BG = '#FF34322E'
    COLOR_RED = '#FFFF0000'
    COLOR_WHITE = '#FFFFFF'
    FONT_TEXT = "Fira Mono:pixelsize=15"
    FONT_AWESOME = "Font Awesome 5 Free:style=Regular:pixelsize=15;1"
    FONT_ICONS = " icomoon:pixelsize=15;1"
    PANEL_WIDTH = ""
    PANEL_HEIGHT = "30"
    PANEL_OFFSET_X = ""
    PANEL_OFFSET_Y = "0"
    PIXEL_UNDERLINE = "5"
    def __init__(self):
        self.bar_geometry = "%sx%s+%s+%s"%(BarStatus.PANEL_WIDTH, 
                                              BarStatus.PANEL_HEIGHT,
                                              BarStatus.PANEL_OFFSET_X,
                                              BarStatus.PANEL_OFFSET_Y)
        self.bar = subprocess.Popen(('lemonbar', '-p', '-g', self.bar_geometry, "-u", BarStatus.PIXEL_UNDERLINE,'-f', BarStatus.FONT_TEXT, '-f', BarStatus.FONT_AWESOME, '-f', BarStatus.FONT_ICONS, '-F', BarStatus.COLOR_FOREGROUND, '-B', BarStatus.COLOR_BACKGROUND, "-a" ,"100"), stdin=subprocess.PIPE)
        self.monitorline = ''
        self._time = ''
        self._taskbar = ''
        self._volume = ''
        self._task_click = lambda x: "bspc node %s -g hidden=off -f"%str(x)
        print("Bar initialized")
    
    def refresh(self):
        
        output = '%{l}' + self.monitorline +  '%{r}'  + str(FormattedText(self._volume, fgcolor=BarStatus.COLOR_FOCUSED_OCCUPIED_FG, bgcolor=BarStatus.COLOR_FOCUSED_OCCUPIED_BG)) + " " +  str(FormattedText(self._time, fgcolor=BarStatus.COLOR_FOCUSED_OCCUPIED_FG, bgcolor=BarStatus.COLOR_FOCUSED_OCCUPIED_BG)) + ' \n'
        #print(self.monitorline)
        self.bar.stdin.write(output.encode('utf-8'))
        self.bar.stdin.flush()
    
    @property
    def taskbar(self):
        return self._taskbar
    
    @taskbar.setter
    def taskbar(self, items):

        self._taskbar = items
        self.refresh()
    
    @property
    def volume(self):
        return self._volume
    
    @volume.setter
    def volume(self, level):
        dorefresh = False
        if self._volume != level:
            dorefresh = True
        self._volume = level
        if dorefresh:
            self.refresh()
    
    @property
    def time(self):
        return self._time
    
    @time.setter
    def time(self, time):
        self._time = time
        self.refresh()
        
    def setmonitors(self, monitors):
        self.monitors = monitors
        self.monitorline = ''
        index = 0
        for monitor in monitors:
            
            self.monitorline += '%{S' + str(index) + '} ' 
            #index += 1
            for desktop in monitor.desktops:
                text = ""
                if desktop.active:
                    if desktop.name != "MAIN":
                        _text = FormattedText(' ' + desktop.name + ' ' )
                        _text.fgcolor = BarStatus.COLOR_FOCUSED_OCCUPIED_FG
                        _text.bgcolor = BarStatus.COLOR_FOCUSED_OCCUPIED_BG
                        _text.ucolor = BarStatus.COLOR_UNDERLINE
                        text += str(_text)
                        for task in desktop.tasks:
                            if task.active:
                                _text = FormattedText(" " + str(task) + " ")
                                _text.fgcolor = BarStatus.COLOR_FOCUSED_OCCUPIED_FG
                                _text.bgcolor = BarStatus.COLOR_FOCUSED_OCCUPIED_BG
                            
                                text += str(_text)
                    else:
                        _text = FormattedText(' ' + "" + ' ' )
                        _text.fgcolor = BarStatus.COLOR_FOCUSED_OCCUPIED_FG
                        _text.bgcolor = BarStatus.COLOR_FOCUSED_OCCUPIED_BG
                        text += str(_text)
                        for task in desktop.tasks:
                            _ = str(ClickableArea(str(task), lcact = self._task_click(task.task_id)))
                            if task.active:
                                _text = FormattedText(" "+ _ + " ")
                                _text.fgcolor = BarStatus.COLOR_FOCUSED_OCCUPIED_FG
                                _text.bgcolor = BarStatus.COLOR_FOCUSED_OCCUPIED_BG
                            
                                _text.ucolor = BarStatus.COLOR_UNDERLINE
                            else:
                                _text = FormattedText(" " + _  + " ")
                                _text.fgcolor = BarStatus.COLOR_OCCUPIED_FG
                                _text.bgcolor = BarStatus.COLOR_OCCUPIED_BG
                            text += str(_text)

                elif desktop.used:
                    if desktop.name == "MAIN":
                        text = FormattedText(' ' + "" + ' ' + " ". join([str(task) for task in desktop.tasks]) + " ")
                        text.fgcolor = BarStatus.COLOR_OCCUPIED_FG
                        text.bgcolor = BarStatus.COLOR_OCCUPIED_BG
                    else:
                        text = FormattedText(' ' + desktop.name + ' ')
                        text.fgcolor = BarStatus.COLOR_OCCUPIED_FG
                        text.bgcolor = BarStatus.COLOR_OCCUPIED_BG
                self.monitorline += str(text)
            #self.monitorline += ' %{S' + str(index) + "}"
            index += 1
        self.refresh()
    def settaskbar(self, tasks, active_task):
        taskbar_string = ""
        for task in tasks:
            if active_task:
                if task.task_id == active_task.task_id:
                    taskbar_string += "%{R} | [" + task._instance +"] " + task._name[:5] + "%R"
                else:
                    taskbar_string += "| [" + task._instance +"] " + task._name[:5]
            else:
                taskbar_string += "| [" + task._instance +"] " + task._name[:5]
        #print(taskbar_string)
        self.taskbar = taskbar_string
class FormattedText:
    def __init__(self, text, fgcolor=None, bgcolor=None, ucolor=None):
        self.text = text
        self.fgcolor = fgcolor
        self.bgcolor = bgcolor
        self.ucolor = ucolor
    
    def __str__(self):
        returnstring = self.text
        if self.ucolor != None:
            returnstring = '%{U' + self.ucolor + '}%{+u}' + returnstring
            returnstring += '%{-u}'
        if self.fgcolor != None:
            returnstring = '%{F' + self.fgcolor + '}' + returnstring
            returnstring += '%{F-}'
        if self.bgcolor != None:
            returnstring = '%{B' + self.bgcolor + '}' + returnstring
            returnstring += '%{B-}'
        return returnstring
class ClickableArea:
    def __init__(self, text, lcact = None, rcact = None, mcact = None, mwuact = None, mwdact = None):
        self.text = text
        self.lcact = lcact
        self.rcact = rcact
        self.mcact = mcact
        self.mwuact = mwuact
        self.mwdact = mwdact
    def __str__(self):
        returnstring = self.text
        if self.lcact:
            returnstring = '%{A1:' + self.lcact+':}' + returnstring + '%{A}'
        if self.rcact:
            returnstring = '%{A3:' + self.rcact+':}' + returnstring + '%{A}'
        if self.mcact:
            returnstring = '%{A2:' + self.mcact+':}' + returnstring + '%{A}'
        if self.mwuact:
            returnstring = '%{A4:' + self.mwuact+':}' + returnstring + '%{A}'
        if self.mwdact:
            returnstring = '%{A5:' + self.mwdact+':}' + returnstring + '%{A}'
        return returnstring

        
