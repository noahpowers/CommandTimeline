# -*- coding: utf-8 -*-
# Controls Program Flow and population of model data

from lib.models.command import Command
from lib.db.persist import Persist
from lib.utils.utiliites import Redactor
import os

class Controller(object):

    def __init__(self, path, arguments):
        self.arguments = arguments
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

    # Take DB file and unpack
    def UnpackData(self):

        database = Persist(self.path,self.arguments)
        temp = database.unpack_database()
        self.arguments.unpack = False

        self.GenerateFromDatabase(temp)
        self.PersistDatabase()

        return


