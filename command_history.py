#!/usr/bin/env python3

# Description: Stored captured history data in database for logging and metrics
#
# Flow:
# (1) Generate Program Path -> Just in case files need to be referenced in project directory
# (2) Retrieve arguments passed in upon execution
# (3) Send arguments to controller to start processes

from lib.core.arguments import Arguments
from lib.controller.controller import Controller
import sys
import os

if sys.version_info < (3, 6):
    sys.stdout.write("Requires Python 3.7\n")
    sys.exit(1)

class Program(object):

    def __init__(self):
        self.path = (os.path.dirname(os.path.realpath(__file__)))
        self.arguments = Arguments(self.path)
        self.controller = Controller(self.path, self.arguments)

if __name__ == "__main__":
    main = Program()
