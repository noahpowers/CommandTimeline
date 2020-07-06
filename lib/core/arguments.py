# -*- coding: utf-8 -*-
from optparse import OptionParser, OptionGroup
import magic
import re
import sys

class Arguments(object):

    def __init__(self, path):
        self.path = path

        options = self.ParseOptions()
        self.copy_options = options

        ####################
        # Configure Required
        ####################

        if options.input is None:
            print('Usage: ./command-time-liner.py [-i|--input] [options]')
            sys.exit()


        self.input = options.input
        self.unpack = self.check_input_file()

        ####################
        # Configure Optional
        ####################

        self.db_file = options.db_file


    def ParseOptions(self):

        usage = 'Usage: ./command-time-liner.py [-i|--input] [options]'
        parser = OptionParser(usage)

        # Required options
        required = OptionGroup(parser, 'Required')
        required.add_option('-i', '--input', help='Terminal History File', action='store', type='string',
                                dest='input', default=None)

        # Optional Options
        optional = OptionGroup(parser, "Optional")
        optional.add_option("--db-file",help="Specify Database Filename", action="store", type="string",
                            dest="db_file", default="archive.db")

        parser.add_option_group(required)
        parser.add_option_group(optional)

        options, arguments = parser.parse_args()

        return options

    # Determine the type of file being ingested
    def check_input_file(self):

        if re.search("sqlite 3", magic.from_file(self.input).lower()):
            return True
        else:
            return False
