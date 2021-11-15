#!/usr/bin/env python3
import vlc 
import time

p = vlc.MediaPlayer("DLF4.mp3")
p.play()
time.sleep(60)
p.stop()