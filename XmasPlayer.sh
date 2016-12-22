#!/bin/bash
cd /home/pi/XmasPlayer
if ps ax| grep 'Xma[s]Player.py'
then 
   :
else
   python XmasPlayer.py &
fi

if ps ax| grep 'fla[s]k_app.py'
then 
   :
else
   python flask_app.py &
   sudo iptables -A PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-port 8080
fi
