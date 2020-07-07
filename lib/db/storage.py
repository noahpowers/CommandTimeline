from shutil import copyfile
from lib.models.command import Command
import base64
import psycopg2
import getpass
import subprocess
import sys
import time
import re
import os


""" Server configuration will utilize this class when writing to the internal database """
class Storage(object):

    def __init__(self, path, user):
        self.path = path
        self.user = user
        self.database_user = "chu"
        self.database_password = None

        self.postgres_cursor = None
        self.command_cursor = None

    """ Initialize Database Instance if First Run """
    def init(self):

        while True:
            password = getpass.getpass("[?] Enter Database Password: ")
            if password:
                self.database_password = password
                break
            else:
                print("[!] Password Needed to Connect to Database ! ")

        if not self.test_connection():
            print("[*] Check Credentials !")

        print("[*] Database Connected !")
        time.sleep(1)

    """ Creates Database User """
    def create_user(self):

        while True:
            password = getpass.getpass("[?] Database Account Password: ")

            if password:
                confirm = getpass.getpass("[?] Confirm Password: ")
                if confirm:
                    if password == confirm:
                        break
                    else:
                        print("[!] Passwords Do Not Match !")
                else:
                    print("[!] Passwords Do Not Match !")
            else:
                print("[!] Password Required !")

        s = ["sudo", "-u", "postgres", "createuser", "-d", "chu"]

        if subprocess.call(s, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
            print("[*] Issues Creating Account !")
            sys.exit()
        else:

            s = [ "sudo", "-u", "postgres", "psql", "-c", "alter USER chu PASSWORD '%s'; " %self.database_password]
            if subprocess.call(s, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
                print("[*] Issue Configuring Password")
                sys.exit()

        return True

    """ Test Initial Server Configurations """
    def test_connection(self):
        """ If Database service is running and connection returns logged in"""
        status_check = subprocess.call(["service", "postgresql", "status"], stdout=subprocess.DEVNULL)

        if status_check == 0:
            """ Check If Account Is Configured """
            try:
                self.postgres_cursor = psycopg2.connect(user=self.database_user,
                                                        password=self.database_password, host="127.0.0.1",
                                                        dbname="postgres").cursor()
            except psycopg2.OperationalError:
                print("[*] Creating database user !")
                time.sleep(1)
                self.create_user()

            try:
                self.command_cursor = psycopg2.connect(user=self.database_user,
                                                       password=self.database_password, host="127.0.0.1",
                                                       dbname="commandhistory").cursor()
                self.check_table()
            except psycopg2.OperationalError:
                print("[*] Initializing Database !")
                time.sleep(1)
                self.create_database()


            return True
        else:
            print("[*] POSTGRESQL is not running or installed")
            sys.exit(1)

    """ Creates the Database """
    def create_database(self):

        try:
            self.command_cursor = psycopg2.connect(user=self.database_user, password=self.database_password, host='127.0.0.1', dbname="commandhistory").cursor()
            self.check_table()
            return
        except psycopg2.OperationalError:
            print("[*] Creating Database !")
            time.sleep(1)

            self.postgres_cursor = psycopg2.connect(user=self.database_user, password=self.database_password, host='127.0.0.1', dbname="postgres").cursor()

        command = "CREATE DATABASE commandhistory;"
        self.postgres_cursor.execute("rollback;")

        try:
            self.postgres_cursor.execute(command)
            print("[*] Database Created !")
            time.sleep(1)
            self.check_table()
        except psycopg2.ProgrammingError:
            self.check_table()
            return True
        except psycopg2.OperationalError:
            self.postgres_cursor.execute("rollback;")
            return False

        return

    """ Check Tables """
    def check_table(self):

        s = " select table_schema, table_name "
        s += "from information_schema.tables where "
        s += "table_schema = 'public' and table_name = 'command';"

        try:
            if self.command_cursor:
                self.command_cursor.execute("rollback;")
                self.command_cursor.execute(s)
            else:
                self.command_cursor = psycopg2.connect(user=self.database_user, password=self.database_password, host='localhost',
                                           dbname='commandhistory').cursor()
                self.command_cursor.execute(s)

            results = self.command_cursor.fetchone()
            if results:
                if results[0] == 'public' and results[1] == 'command':
                    return True
            else:
                print("[*] Creating Tables ")
                self.create_tables()
        except psycopg2.OperationalError:
            self.command_cursor.execute('rollback;')
            print("[*] Creating Tables ")
            time.sleep(1)
            self.create_tables()

    """ Creates Tables in Database """
    def create_tables(self):

        s = "CREATE TABLE command ( timestamp text, command text, arguments text, raw text )"

        try:
            if not self.command_cursor:
                self.command_cursor = psycopg2.connect(user=self.database_user, password=self.database_password,
                                       host='localhost', dbname='commandhistory').cursor()

            self.command_cursor.execute('rollback')
            self.command_cursor.execute(s)
            return True
        except psycopg2.ProgrammingError as e:
            print("[*] Table Already Exists !")
            return True

    def append(self):
        pass

    """ Fetches all Records from Database """
    def fetch(self):

        if not self.command_cursor:
            self.command_cursor = psycopg2.connect(user=self.database_user, password=self.database_password,
                                                   host='localhost', dbname='commandhistory').cursor()

        s = "SELECT raw FROM command;"
        self.command_cursor.execute('rollback')
        self.command_cursor.execute(s)

        return self.command_cursor.fetchall()

    """ Rebuild Fetched Records into Command Objects """
    def revo(self):

        print("[*] Unpacking From Database ")
        time.sleep(1)
        stored_commands = self.fetch()

        for stored_command in stored_commands:
            self.user.commands.append(Command(base64.b64decode(stored_command[0].encode()).decode()))

    """ Decode Commands """
    def command_decoder(self, commands):

        cache = []

        for command in commands:
            command.argument_string = base64.b64decode(command.argument_string.encode()).decode()
            command.raw_command = base64.b64decode(command.raw_command.encode()).decode()
            cache.append(command)

        return cache

    """ Cleans the Commands to Remove ' before executing a statement """
    def clean(self, command):
        try:
            while True:
                if str(command.tool).startswith("'") or str(command.tool).endswith("'"):
                    str(command.tool).lstrip("'").rstrip("'")
                else:
                    break

            argument_string = ""
            for arg in command.arguments:
                argument_string += str(arg) + " "

            command.argument_string = argument_string
        except KeyboardInterrupt:
            print(command.argument_string)

        return command

    """ Commands may need to be base64 encoded before storing into database """
    def encoded_commands(self, commands):

        cache = []
        for command in commands:
            command.raw_command = base64.b64encode(command.raw_command.encode())
            cache.append(command)

        return cache

    """ Inserts Commands into Table """
    def insert_row(self, commands):

        for command in commands:
            command = self.clean(command)
            s = " INSERT INTO command ( timestamp, command, arguments, raw ) VALUES ( '%s', '%s', '%s', '%s' )" %\
                (command.time_stamp, command.tool, base64.b64encode(command.argument_string.encode()).decode(), base64.b64encode(command.raw_command.encode()).decode())

            self.command_cursor.execute('rollback;')
            self.command_cursor.execute(s)

    def store(self):
        pass

