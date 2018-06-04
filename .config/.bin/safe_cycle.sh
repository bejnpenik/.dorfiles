#!/bin/sh


NOH=$(bspc query -N -n .hidden -d focused)
for LINE in $NOH; do
	bspc node $LINE -g hidden=off
done
bspc node -f next.local
