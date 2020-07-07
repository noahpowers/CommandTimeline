# -*- coding: utf-8 -*-

import sqlite3
from sys import exit
from shutil import copyfile

class Persist(object):

    def __init__(self, path, arguments):

        # Pass arguments to retrieve specified options
        # Pass Path around just in case something needs to be accessed from project directory

        self.arguments = arguments
        self.path = path
        self.db = None
        self.table_name = "CommandHistory"

        if self.arguments.unpack is False:
            self.load()

    # Insert Command Data
    def insert_row(self, command):

        c = self.db.cursor()

        # Insert Row
        try:
            c.execute('''INSERT INTO CommandHistory VALUES ('%s','%s','%s', '%s')
                      '''%(command.time_stamp, command.tool, " ".join(command.arguments), command.raw_command))
        except sqlite3.OperationalError:
            pass

        self.persist()
        return

    # Load database file
    def load(self):
        self.db = sqlite3.connect(self.arguments.db_file)
        return

    # Create Database
    def creation(self):

        c = self.db.cursor()

        # Create table
        c.execute('''CREATE TABLE CommandHistory( 
                     TimeStamp text, 
                     Command text, 
                     Arguments text,
                     Raw text            
                                     )''')
        return

    # Check instance
    def check_table(self, database=None):

        if database is None:
            c = self.db.cursor()
        else:
            c = database.cursor()

        for row in c.execute('SELECT name FROM sqlite_master WHERE name="%s"' %self.table_name):
            if bool(row):
                return True

        return False

    # Save Database
    def persist(self):
        self.db.commit()
        return

    # Unpacks selected database to add to another
<<<<<<< HEAD
    def unpack_database(self, filename=None):

        if filename:
            db_unpack = sqlite3.connect(self.path + "uploads/%s" %filename)
        else:
            db_unpack = sqlite3.connect(self.arguments.input)

=======
    def unpack_database(self):

        db_unpack = sqlite3.connect(self.arguments.input)
>>>>>>> b0a9da9c1499b0491f56eb45f1373b4f06ba8ff8
        c = db_unpack.cursor()

        temp = []

        if self.check_table(database=db_unpack):
            for row in c.execute('SELECT Raw FROM CommandHistory'):
                if bool(row):
                    temp.append(list(row))
        else:
            print("Ingested Database is not initialized")
            exit()

        return temp

  # Backup archive file being reading and writing
    def backup_archive(self):
        copyfile(self.arguments.db_file, self.path + "/%s.backup" % self.arguments.db_file)
        return