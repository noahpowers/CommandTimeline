from lib.models.globals import ServerGlobals
from flask import request, jsonify
import threading
import logging
import flask
import magic
import time
import re
import os


app = flask.Flask(__name__)
job_queue = []
busy = False

""" Defines the Server Instance """
class Server(object):
    def __int__(self, path, user):

        global app

        self.path = path
        self.user = user
        self.allowed_extensions = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

        app.config['UPLOAD_FOLDER'] = self.path + "/uploads/"

        upload_worker = threading.Thread(target=self.uploadWorker)
        upload_worker.start()

    def start(self):

        log = logging.getLogger('werkzeug')
        log.disabled = True
        app.name = "Command History Archiver"
        app.run(host="0.0.0.0", port=ServerGlobals.PORT)

    """ Add Posted File into database """
    def addHistoryFiles(self, filename):
        self.user.UnpackDatabase(filename=filename, server=True)

    """ Unpack Data """
    def unpackData(self, filename):
        pass

    """ May not be necessary but wanna have one pipe line into program """
    def directRequest(self):
        pass

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    """ Secures """
    def secure_filename(self, upload, test=False):

        if test:
            return True

        if re.search("sqlite 3", magic.from_file(upload)):
            return upload
        else:
            return False

    """ Retrieves the posted file """
    @app.route ("/push-history", methods=["POST"])
    def postFile(self):

        """ If FIle is Sent Over """
        if request.method == "POST":
            if 'file' not in request.files:
                flask.flash("No File Data")
                return flask.redirect(request.url)
            file = request.files["file"]

            if file.filename == "":
                flask.flash("No File Selected")
                return flask.redirect(request.url)

            if file and self.allowed_file(file.filename):
                filename = self.secure_filename(file.filename)
                if filename:
                    file.save(self.path + "uploads/", filename)
                    job_queue.append(filename)

                    return flask.redirect(flask.url_for('uploaded_file',filename=filename))

        return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form> '''

    """ Watches the uploads directory to process and add files"""
    def uploadWorker(self):

        if not os.path.exists(self.path + "/uploads"):
            os.makedirs(self.path + "/uploads")

            while True:
                if job_queue:
                    self.busy = True
                    for job in job_queue:
                        self.user.UnpackDatabase(filename=job)
                    self.busy = False
                else:
                    time.sleep(3)




