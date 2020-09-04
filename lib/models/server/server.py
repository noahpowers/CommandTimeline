from lib.models.globals import ServerGlobals
from werkzeug.utils import secure_filename
from flask import request, jsonify
import shutil
import queue
import threading
import logging
import flask
import magic
import time
import sys
import re
import os

allowed_extensions = ['db']
app = flask.Flask(__name__)
app.secret_key = 'applesauce'
app.config['SESSION_TYPE'] = 'filesystem'
job_queue = []
program_path = None
busy = False
file = None

# Implementing this at some point better handles threads
# queue = queue.Queue()

""" Defines the Server Instance """
class ServerMode():

    def __init__(self, path, user):

        global app, program_path
        self.user = user
        program_path = path
        app.config['UPLOAD_FOLDER'] = program_path + "/uploads/"

        """ Kick off Watch Thread For Events """
        worker_process = threading.Thread(target=work, args=(self.user,))
        worker_process.start()

    def start(self):
        log = logging.getLogger('werkzeug')
        log.disabled = True
        app.name = "Command History Archiver"
        app.run(host="0.0.0.0", port=ServerGlobals.PORT)

    """ Add Posted File into database """
    def addHistoryFiles(self, filename):
        self.user.UnpackDatabase(filename=filename, server=True)

    """ May not be necessary but wanna have one pipe line into program """
    def directRequest(self):
        pass


""" Retrieves the Request From the Server """
def porter(request):
    """ Check If Proper Method is Sent """
    if request.method == "POST":
        if 'file' not in request.files:
            flask.flash("No File Data")
           # return flask.redirect(request.url)
            return flask.get_flashed_messages()
        if request.args.get("uploadFile"):

            if request.args["uploadFile"] == "true":
                file_upload = request.files["file"]
            else:
                return jsonify({400: "Invalid Parameters"})

            if file_upload:
                if process(file_upload):
                    return jsonify({200: "Success"})
                else:
                    return jsonify({400: "File Not Uploaded"})
        else:
            return jsonify({400: "Invalid"})
    pass

""" Watches the uploads directory to process and add files"""
def work(user):
    if not os.path.exists(program_path + "/uploads"):
        os.makedirs(program_path + "/uploads")

    user.arguments.server = True

    while True:
        if job_queue:
            cache = job_queue
            busy = True
            for i in range(len(cache)):
                user.UnpackData(filename=cache[i])

                if i in job_queue:
                    job_queue.pop(i)

            cache = []
            busy = False
        else:
            time.sleep(5)


""" Retrieves the posted file """
@app.route("/pushHistory", methods=["POST"])
def postFile():

    """ If FIle is Sent Over """
    if request.method == "POST":
        if 'file' not in request.files:
            flask.flash("No File Data")
            return flask.redirect(request.url)

        if request.args.get("uploadFile"):
            if request.args["uploadFile"] == "true":
                file_upload = request.files["file"]
            else:
                return jsonify({400: "Invalid Parameters"})

            if file_upload:
                if process(file_upload):
                    return jsonify({200: "Success"})
                else:
                    return jsonify({400: "File Not Uploaded"})
        else:
            return jsonify({400: "Invalid"})


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def checkFileType(upload):

    filename = upload.filename
    location = os.path.join(program_path + '/uploads/temp/', filename)
    upload.save(location)

    if re.search("sqlite 3".lower(), magic.from_file(program_path + "/uploads/temp/%s" %filename).lower()):
        shutil.move(program_path + "/uploads/temp/" + filename, program_path + "/uploads/%s" %filename)
        return True
    else:
        shutil.copyfile(program_path + "/uploads/temp/%s" %filename, "/dev/null")
        return False

def process(file_upload):

    file_upload.filename = secure_filename(file_upload.filename)
    if file_upload.filename == "":
        flask.flash("No File Selected")
        return flask.redirect(request.url)

    if file_upload and allowed_file(file_upload.filename):
        if checkFileType(file_upload):
            #file_upload.save(os.path.join(app.config['UPLOAD_FOLDER'], file_upload.filename))
            job_queue.append(file_upload.filename)
            return True
        else:
            return False

