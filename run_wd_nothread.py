#!/usr/bin/env python

from watchdog import WatchDog
import os
import tkwindow
import threading

cwd = os.getcwd()

watched = raw_input(
        "Directory to monitor: [{}] ".format(cwd))
if not watched:
    watched = cwd

upload = raw_input("Upload new images to imgur (y/n): [n] ")
print
if upload in ["y", "Y"]:
    upload = True
else:
    upload = False
