import Queue
import os
os.chdir("c:/users/matthew/watchdog")
from watchdog import WatchDog
import threading

dirs = ["c:/users/matthew/watchdog", "c:/users/matthew/pyimgur"]


class WD(threading.Thread):
    def run(self):
        while True:
            path = pathPool.get()
            if path:
                w = WatchDog(path, 2)
                w.monitor()

pathPool = Queue.Queue(0)
for x in xrange(len(dirs)):
    WD().start()

for dir in dirs:
    pathPool.put(dir)
