#!/bin/bash


new_workspace=$(( $(bspc query -D | wc -l) + 1 ))
current_monitor=$(bspc query -M -m focused)
last_monitor=$(bspc query -M | tail -n 1)
bspc monitor ${last_monitor} --add-desktops ${new_workspace}
bspc desktop ${new_workspace} --to-monitor ${current_monitor}
# Renumber the desktops (this is necessary to maintain proper numbering
# order in multihead setups)
bspc desktop $new_workspace -f
~/rename_desktop.sh ${new_workspace}
