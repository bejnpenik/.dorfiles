#!/bin/sh

NODES=$(bspc query -N -d focused)
for LINE in $NODES; do
	bspc node $LINE -d MAIN
done
bspc desktop focused --remove
NODES=$(bspc query -N -d MAIN -n .tiled)
for LINE in $NODES; do
	bspc node $LINE -t floating
done
