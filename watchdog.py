#!/usr/bin/env python
# Test loop monitoring program

import time
import os
import webbrowser
import sys
import imghdr

try:
    sys.path.append("../PyImgur/")
    from pyimgur import UploadImage
except:
    pass



class WatchDog():
    '''
    I'm watching your directory.
    '''
    def __init__(self, watched, delay, q, upload=False):
        self.watched = watched
        self.delay = delay
        self.q = q
        self.upload = upload
        self.establish()

    def log(self, data):
        '''
        Output some log data with timestamp
        '''
        self.q.put("[{}] {} {}".format(
                time.strftime("%X"),
                self.watched,
                data))

    def build(self):
        '''
        Build a dictionary of files and stats.
        '''
        _build_dict = dict()
        for file_item in os.listdir(self.watched):
            _build_dict[file_item] = os.stat(
                    os.path.join(self.watched, file_item))
        return _build_dict

    def establish(self):
        '''
        Establish base identities for initial file discovery.
        '''
        self.log("[!] Building initial data")
        self.stats = self.build()
        self.log("[!] Monitoring {}".format(self.watched))
        if self.upload:
            self.log("[!] Uploading new/modified images to imgur.com")

    def compare(self):
        '''
        Do some basic file stat comparing.
        '''
        _current = self.build()
        _old_keys = set(self.stats.keys())
        _new_keys = set(_current.keys())
        self.added = list(_new_keys - _old_keys)
        self.modified = [y for y in _old_keys & _new_keys
                if self.stats[y] != _current[y]]
        self.removed = list(_old_keys - _new_keys)
        self.stats = _current

    def checkimage(self):
        _images = list()
        for image in self.added+self.modified:
            if imghdr.what(os.path.join(self.watched, image)):
                _images.append(image)
            else:
                pass
        return _images

    def imgur(self):
        '''
        Example uploading to imgur.
        '''
        for image in [x for x in self.checkimage()]:
            result = UploadImage(os.path.join(self.watched, image))
            if not result.error:
                url = result.imageURL['url']
                webbrowser.open(url)
		self.log("** Uploaded to {}".format(url))
            else:
                self.log(result.error)

    def monitor(self):
        '''
        Basic check->pause->check loop monitoring for file changes.
        '''
        while True:
            self.compare()
            _results = [
                ["[-] Removed", " ".join(self.removed)],
                ["[*] Modified", " ".join(self.modified)],
                ["[+] Added", " ".join(self.added)]]
            for result in _results:
                if len(result[1]):
                    self.log(" : ".join(result))
            if self.upload and globals().get("UploadImage"):
                self.imgur()
            time.sleep(self.delay)
