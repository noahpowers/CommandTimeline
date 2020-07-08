# -*- coding: utf-8 -*-

import os
import sys
import sqlite3
from sys import exit
from shutil import copyfile

class Persist(object):

    def __init__(self, path, arguments, filename=None):

        # Pass arguments to retrieve specified options
        # Pass Path around just in case something needs to be accessed from project directory

        self.arguments = arguments
        self.path = path
        self.db = None

        if filename:
            self.load(filename=filename)
        else:
            if self.arguments.unpack is False or filename:
                self.load()

    # Insert Command Data
    def insert_row(self, command):

        c = self.db.cursor()

        # Insert Row
        try:
            c.execute('''INSERT INTO command VALUES ('%s','%s','%s', '%s')
                      '''%(command.time_stamp, command.tool, " ".join(command.arguments), command.raw_command))
        except sqlite3.OperationalError:
            pass

        self.persist()
        return

    # Load database file
    def load(self, filename=None):

        if filename:
            self.db = sqlite3.connect(self.path + "/uploads/" + filename)

        else:
            if not os.path.exists(self.path + "/archives"):
                os.makedirs(self.path + "/archives")

            self.db = sqlite3.connect(self.path + "/archives/" + self.arguments.db_file)

        return

    # Create Database
    def creation(self):

        c = self.db.cursor()

        # Create table
        c.execute('''CREATE TABLE command ( timestamp text, command text, arguments text, raw text   )''')
        return

    # Check instance
    def check_table(self, database=None):

        if database is None:
            c = self.db.cursor()
        else:
            c = database.cursor()

        for row in c.execute('select name from sqlite_master where name="command";'):
            if bool(row):
                return True

        return False

    # Save Database
    def persist(self):
        self.db.commit()
        return

    # Unpacks selected database to add to another
    def unpack_database(self, filename=None, server=False):

        if filename:
            location = str(self.path + "/uploads/" + filename)
            db_unpack = sqlite3.connect(location)
        else:
            db_unpack = sqlite3.connect(self.arguments.input)

        temp = []
        if self.check_table(database=db_unpack):
            c = db_unpack.cursor()
            for row in c.execute('SELECT raw FROM command'):
                if bool(row):
                    temp.append(list(row))
        else:
            if server:
                return False
            else:
                print("Ingested Database is not initialized")
                exit()

        return temp

  # Backup archive file being reading and writing
    def backup_archive(self):
        copyfile(self.path + "/archives/%s" %self.arguments.db_file, self.path + "/archives/%s.backup" % self.arguments.db_file)
        return