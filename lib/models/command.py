# -*- coding: utf-8 -*-
from datetime import datetime
import re

class Command(object):

    def __init__(self, raw_command):
        self.raw_command = raw_command
        self.tool = None
        self.arguments = []
        self.date = None
        self.time = None
        self.time_stamp = None
        self.parser()

        self.convertDate()

    """ Convert Date """
    def convertDate(self):

        if self.date and self.time:
            string = "%s %s" %(self.date, self.time)
            self.time_stamp = datetime.strptime(string, "%Y-%m-%d %H:%M:%S").timestamp()

    """ Regenerate Raw Command after Redaction """
    def redact_raw_command(self):

        self.raw_command = "%s %s %s " %(self.date, self.time, self.tool)

        for argument in self.arguments:
            self.raw_command += argument + " "

    # Parses raw command to save attributes
    def parser(self):

        skips = ["sudo", "python"]

        temp = self.raw_command.split(" ")
        previous_skip = False

        for index in range(len(temp)):

            if index == 0:
                self.date = temp[0]
            elif index == 1:
                self.time = temp[1]
            elif index == 2:

                # Avoid storing skips as tools
                for skip in skips:
                    if re.search(skip, temp[2].lower()) and len(temp) > 3:
                        temp[3] = temp[3].lstrip("\"")
                        temp[3] = temp[3].rstrip("\"")
                        self.tool = temp[3]
                        previous_skip = True
                    else:
                        temp[2] = temp[2].lstrip("\"")
                        temp[2] = temp[2].rstrip("\"")
                        self.tool = temp[2]

                    if previous_skip:
                        previous_skip = False
                        break
            else:
                if index == len(temp)-1:
                    temp[index] = temp[index].rstrip('\"')

                self.arguments.append(temp[index])
