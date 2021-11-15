# comrade-candles-ECE434
This repository stores the programs for the Comrade Candles project in ECE434.

To run pagekite (after downloading it onto your bone) run the following
python pagekite.py 8081 [INSERT YOUR PAGEKITE URL]

for example I ran the follwoing (no quotes)
"python pagekite.py 8081 vandensp.pagekite.me"

In the mplayer commands, the sysdefault="_____" (no quotes) parameter will depend on the audio output device
that you have plugged into the BeagleBone. To see what this parameter is run command "aplay -L"
on the BeagleBone, and change the parameter in the mplayer command.

