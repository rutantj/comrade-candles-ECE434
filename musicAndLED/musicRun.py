#!/usr/bin/python3

import os
import sys

file = sys.argv[1]

os.system("mplayer -ao alsa:device=sysdefault=AT2020USB ../mp3folder/"+file)