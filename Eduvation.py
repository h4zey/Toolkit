# -*- coding: utf-8 -*-

"""
  Hazey~
"""

import sys
import enum
import socket
import logging

from queue import Queue
from threading import Thread
from itertools import repeat

class Options(enum.IntEnum):
    RANGE = 1024
    THREADS = 16
    TIMEOUT = 1

logging.basicConfig(format="%(asctime)-15s %(message)s", level=logging.INFO, stream=sys.stdout)

class Scanner(Thread):
    def __init__(self, queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = queue

    def run(self):
        while not self.queue.empty():
            item = self.queue.get()
            with socket.socket() as sock:
                sock.settimeout(Options.TIMEOUT)
                if not sock.connect_ex(item):
                    logging.info("{}:{} is open".format(*item))
            self.queue.task_done()


def init():
    host = input("Enter hostname: ")
    
    queue = Queue()
    for info in zip(repeat(host), range(1, Options.RANGE)):
        queue.put(info)

    threads = [Scanner(queue) for _ in range(Options.THREADS)]

    for t in threads:
        t.start()

    queue.join()

    for _ in range(Options.THREADS):
        queue.put(None)
    for t in threads:
        t.join()

if __name__ == "__main__":
    init()
