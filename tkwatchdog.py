import multiprocessing
import os
import time
import Queue
import threading
from tkwindow import Report
from watchdog import WatchDog


class WD(threading.Thread):
    '''Run WatchDog instances as threads'''
    def __init__(self, threads, q, upload=False, timing=2):
        self.upload = upload
        self.threads = threads
        self.q = q
        self.timing = timing
        threading.Thread.__init__(self)

    def run(self):
        while True:
            path = pathPool.get()
            if path:
                win = WatchDog(
                        path,
                        self.timing,
                        self.q,
                        self.upload)
                t = multiprocessing.Process(
                        target=logGen,
                        args=(win,))
                t.start()
                self.threads.append(t)

def logGen(win):
    win.monitor()


if __name__ == "__main__":
    multiprocessing.freeze_support()

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

    q = multiprocessing.Queue()
    q.cancel_join_thread()
    gui = Report(q)

    threads = list()
    pathPool = Queue.Queue(0)
    for x in xrange(len(dirs)):
        WD(threads, q, upload).start()

    for dir in dirs:
        pathPool.put(dir)

    gui.root.mainloop()

    for thread in threads:
        thread.join()

