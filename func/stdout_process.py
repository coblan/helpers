import threading
import sys
import os

"""
from Capturing import *
import time

capturing = Capturing()

def on_read(line):
    # do something with the line
    capturing.print("got line: "+line)

capturing.on_readline(on_read)
capturing.start()
print("hello 1")
time.sleep(1)
print("hello 2")
time.sleep(1)
print("hello 3")
capturing.stop()
"""
class Capturing():
    def __init__(self,stdout=True,stderr=True):
        self._stdout = None
        self._stderr = None
        self._r = None
        self._w = None
        self._thread = None
        self._on_readline_cb = None
        self.recieve_stdout = stdout
        self.recieve_stderr = stderr

    def _handler(self):
        while not self._w.closed:
            try:
                while True:
                    line = self._r.readline()
                    if len(line) == 0: break
                    if self._on_readline_cb: self._on_readline_cb(line)
            except:
                break

    def print(self, s, end=""):
        print(s, file=self._stdout, end=end)

    def on_readline(self, callback):
        self._on_readline_cb = callback

    def start(self):
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        r, w = os.pipe()
        r, w = os.fdopen(r, 'r',encoding='utf-8'), os.fdopen(w, 'w', 1,encoding='utf-8')
        self._r = r
        self._w = w
        if self.recieve_stdout:
            sys.stdout = self._w
        if self.recieve_stderr:
            sys.stderr = self._w
        self._thread = threading.Thread(target=self._handler)
        self._thread.start()

    def stop(self):
        self._w.close()
        if self._thread: self._thread.join()
        self._r.close()
        sys.stdout = self._stdout
        sys.stderr = self._stderr
