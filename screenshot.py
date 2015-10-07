#!/usr/bin/env python
# Take root window screen and upload to imgur with pyimgur

import os
import webbrowser
import sys
import time
import ImageGrab
from datetime import datetime
import windowing
sys.path.append("c:/users/matthew/PyImgur/")
from pyimgur import UploadImage


def outputstring(ext):
    d = datetime.now()
    datestring = "".join([str(x) for x in [d.day, d.month, d.microsecond]])
    dirstring = os.path.dirname(__file__)

    return os.path.join(dirstring, datestring+ext)

def snapshot(wait=3, doupload=False):
    time.sleep(wait)
    top = windowing.getWindowSizes(location=True)[0]
    box = top[1]

    output = outputstring(".png")
    img = ImageGrab.grab(box)
    img.save(output, "PNG")

    if doupload:
        upload(output)

def upload(image):
    result = UploadImage(image)
    if not result.error:
        url = result.imageURL['url']
        webbrowser.open(url)
    else:
        print result.error

if __name__ == "__main__":
    snapshot(wait=3, doupload=True)
