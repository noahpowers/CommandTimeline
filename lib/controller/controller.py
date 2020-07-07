# -*- coding: utf-8 -*-
# Controls Program Flow and population of model data
<<<<<<< HEAD
from lib.models.server.server import ServerMode
from lib.models.command import Command
from lib.db.persist import Persist
from lib.db.storage import Storage
from lib.utils.utiliites import Redactor
import os
import sys
=======

from lib.models.command import Command
from lib.db.persist import Persist
from lib.utils.utiliites import Redactor
import os
>>>>>>> b0a9da9c1499b0491f56eb45f1373b4f06ba8ff8

class Controller(object):

    def __init__(self, path, arguments):
        self.arguments = arguments
<<<<<<< HEAD
        self.commands = []
        self.path = path
        self.storage = None
        self.user = self

        if self.arguments.server:
            self.storage = Storage(self.path, self)
            self.storage.init()
            # ServerMode() - For some reason its not reading my class file

        else:
            self.history = arguments.input

            if self.arguments.unpack is False:
                self.GenerateFromHistory()
                Redactor(self.path, self.commands)

                for command in self.commands:
                    command.redact_raw_command()

                self.PersistDatabase()
            else:
                self.UnpackData()
=======
        self.history = arguments.input
        self.commands = []
        self.path = path

        if self.arguments.unpack is False:
            self.GenerateFromHistory()
            Redactor(self.path, self.commands)

            for command in self.commands:
                command.redact_raw_command()

            self.PersistDatabase()
        else:
            self.UnpackData()
>>>>>>> b0a9da9c1499b0491f56eb45f1373b4f06ba8ff8

    # Generates command objects using history file
    def GenerateFromHistory(self):

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

        database = Persist(self.path,self.arguments)

        if os.path.isfile(self.arguments.db_file):
            if database.check_table() is False:
                database.creation()
            else:
                database.backup_archive()

        for command in self.commands:
            if command is not None:
                database.insert_row(command)

        database.persist()
        return

<<<<<<< HEAD

    # Take DB file and unpack
    def UnpackData(self, filename=None):
=======
    # Take DB file and unpack
    def UnpackData(self):
>>>>>>> b0a9da9c1499b0491f56eb45f1373b4f06ba8ff8

        database = Persist(self.path,self.arguments)
        temp = database.unpack_database()
        self.arguments.unpack = False

        self.GenerateFromDatabase(temp)
<<<<<<< HEAD

        if filename:
            Storage(self.path, self).insertRows(self.commands)
        else:
            self.PersistDatabase()
=======
        self.PersistDatabase()
>>>>>>> b0a9da9c1499b0491f56eb45f1373b4f06ba8ff8

        return


