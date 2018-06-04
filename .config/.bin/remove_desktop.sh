#!/bin/sh


NAME=$(bspc query -D --names | dmenu -b -i -p "Which one to remove?")

if [ $NAME = "MAIN" ]
then
	echo "I can't remove MAIN"
else
	notify-send "I removed workspace $NAME\nIf there were some clients i moved it to MAIN"
	NODES=$(bspc query -N -d $NAME)
	for LINE in $NODES; do
		bspc node $LINE -d MAIN	
	done
	bspc desktop $NAME --remove

fi
