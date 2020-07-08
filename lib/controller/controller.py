# -*- coding: utf-8 -*-
# Controls Program Flow and population of model data
from lib.models.server.server import ServerMode
from lib.models.command import Command
from lib.db.persist import Persist
from lib.db.storage import Storage
from lib.utils.utiliites import Redactor
import os
import sys


class Controller(object):

    def __init__(self, path, arguments):

        self.arguments = arguments
        self.commands = []
        self.path = path
        self.storage = None

        if self.arguments.server:
            self.storage = Storage(self.path, self)
            self.storage.init()

            self.server = ServerMode(self.path, self)
            self.server.path = self.path
            self.server.start()

        else:
            self.history = arguments.input

            if self.arguments.unpack is False:
                self.GenerateFromHistoryFile()
                Redactor(self.path, self.commands)

                for command in self.commands:
                    command.redact_raw_command()

                self.PersistDatabase()
            else:
                self.UnpackData()

    # Generates command objects using history file
    def GenerateFromHistoryFile(self):

        temp = open(self.history, "r").readlines()

        for line in temp:
            line = line.rstrip()
            if bool(line):
                self.commands.append(Command(line))

    # Generates command objects using database
    def GenerateFromDatabase(self, temp):

        for command in temp:
            self.commands.append(Command(" ".join(command)))

    # Saves command objects to SQLite3 file
    def PersistDatabase(self):

        database = Persist(self.path, self.arguments)
        if os.path.isfile(self.path + "/archives/" + self.arguments.db_file):
            if database.check_table() is False:
                database.creation()
            else:
                database.backup_archive()

        for command in self.commands:
            if command is not None:
                database.insert_row(command)
            database.persist()

        return

    # Take DB file and unpack
    def UnpackData(self, filename=None):

        if filename:
            database = Persist(self.path, self.arguments, filename=filename)
            temp = database.unpack_database(filename=filename, server=True)

        else:
            database = Persist(self.path, arguments=self.arguments)
            temp = database.unpack_database(filename=filename)

        self.arguments.unpack = False

        if not temp:
            self.server.busy = False
            return

        self.GenerateFromDatabase(temp)

        if filename:
            Storage(self.path, self).insertRows(self.commands)
        else:
            self.PersistDatabase()

        return


