#!/bin/bash



if [ -z $(bspc query -N -n pointed) ]; then
	mygtkmenui -- /home/branislav/.config/GTKMENU/GTKMENU
fi
