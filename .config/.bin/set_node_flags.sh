#!/bin/sh


ACTION=$(echo -e "hidden\nprivate\nsticky\nlocked" | dmenu -i -p "Chose flag for selected window?" -b)

bspc node pointed -g $ACTION
