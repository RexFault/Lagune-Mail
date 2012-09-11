#!/bin/sh
screen -ls | grep yaams_screen
if [ $? -eq 1 ]; then 
screen -S yaams_screen -d -m -c /home/yaams/yaams_chron/yaams.scr
fi
exit 0

