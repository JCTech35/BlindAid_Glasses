#!/bin/bash
echo "Running start.sh"
sleep 3
FILE=/home/pi/Cameron_scripts/DOESITWORK.txt
if [ -f $FILE ];
then
	echo "NOOOOOOOOOO"
	# exit 0
else
	touch /home/pi/Cameron_scripts/DOESITWORK.txt
	# python /home/pi/Cameron_scripts/startup_scripts.py >> /home/pi/Cameron_scripts/DOESITWORK.txt
	lxterminal -e python /home/pi/Cameron_scripts/startup_scripts.py
	DATE="$(date)"
	echo $DATE
fi
# exit 0
sleep 5
exit 0
