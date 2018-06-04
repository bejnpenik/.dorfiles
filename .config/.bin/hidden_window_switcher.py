#!/usr/bin/env python

from subprocess import check_output, Popen, PIPE, call
window_id = None
try:
    window_id = check_output(["bspc", "query", "-N", "-d", "focused", "-n", ".hidden"]).decode("utf-8").strip().splitlines()
except Exception:
    pass
if window_id:
    windows = {}
    window_names = []
    for wid in window_id:
        _title = check_output(["xtitle", wid]).decode("utf-8").strip()
        if _title in window_names:
            i = 1
            while True:
                _title_new = _title + " " + str(i)
                if _title_new not in window_names:
                    _title = _title_new
                    break
                i=i+1
        window_names.append(_title)
        windows[wid] = _title
    dmenu = Popen(("dmenu", "-i", "-p", "Unhide window: ", "-b"),
            stdin=PIPE, stdout=PIPE)
    menu_str = "\n".join(window_names)
    win_str = dmenu.communicate(menu_str.encode('utf-8'))[0].decode('utf-8').rstrip()
    for wid in windows:
        if win_str==windows[wid]:
            call(("bspc", "node", wid, "-g", "hidden=off"))
