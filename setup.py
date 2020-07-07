from setuptools import setup
import os

setup(
    name='CommandHistory',
    version='',
    packages=['lib', 'lib.db', 'lib.core', 'lib.controller'],
    url='',
    license='',
    author='Tarrell Fletcher & Noah Powers',
    author_email='',
    description=''
)

os.system("python3 -m pip install -r requirements.txt")

""" For Server Section """
#os.system("/usr/lib/postgresql/10/bin/initdb -d /etc/command_history")
#os.system("/usr/lib/postgresql/10/bin/createuser -d --host=localhost chu")
#os.system("sudo -u postgres psql -c \"CREATE USER chu CREATEDB\"")
#os.system("sudo -u postgres psql -c \"ALTER USER chu PASSWORD 'password';\"")
#sudo -u postgres psql -c \"CREATE DATABASE commandhistory;\"")
#CREATE USER john WITH ENCRYPTED PASSWORD 'Postgr@s321!';


