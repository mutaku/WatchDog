#!/usr/bin/env python
import Queue
import os
from watchdog import WatchDog
import threading


class WD(threading.Thread):
    '''Run WatchDog instances as threads'''
    def __init__(self, upload=False, timing=2):
        self.upload = upload
        self.timing = timing
        threading.Thread.__init__(self)

    def run(self):
        while True:
            path = pathPool.get()
            if path:
                w = WatchDog(path,
                        self.timing,
                        self.upload)
                w.monitor()

cwd = os.getcwd()
watched = raw_input(
        "Directories to monitor (comma sep): [{}] ".format(cwd))
if not watched:
    dirs = [cwd]
else:
    dirs = [dir.strip() for dir in watched.split(",")]

upload = raw_input("Upload new images to imgur (y/n): [n] ")
print
if upload in ["y", "Y"]:
    upload = True
else:
    upload = False

#pathPool = Queue.Queue(0)
#for x in xrange(len(dirs)):
#    WD(upload).start()

#for dir in dirs:
#    pathPool.put(dir)

# do we lose some output when firing up from the queues...
#   maybe we need to pause briefly before firing up the next
#   instantiation of WatchDog to give output time to show up
