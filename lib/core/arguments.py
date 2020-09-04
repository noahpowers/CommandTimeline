# -*- coding: utf-8 -*-
from optparse import OptionParser, OptionGroup
from lib.utils.transform import Transform
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
        if options.server:
            self.server = True
            return

        else:
            self.server = False

            if options.input is None and options.transform is None:
                print('Usage: ./command-time-liner.py [-i|--input] [options]')
                sys.exit()

            if options.transform:
                Transform(options.transform)
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
        optional.add_option("--transform", help="Transform history to archival format", action="store", type="string",
                            dest="transform")

        # Server Mode Settings
        server = OptionGroup(parser, "Server")
        server.add_option("--server", help="Configures Server using POSTGRESQL", action="store_true", dest="server")
        server.add_option("--port", help="Port to run service on, default is 5000", action="store", type="int", dest="port")

        parser.add_option_group(required)
        parser.add_option_group(optional)
        parser.add_option_group(server)

        options, arguments = parser.parse_args()

        return options

    # Determine the type of file being ingested
    def check_input_file(self):

        if re.search("sqlite 3", magic.from_file(self.input).lower()):
            return True
        else:
            return False
