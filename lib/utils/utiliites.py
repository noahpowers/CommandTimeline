import json

""" Reads in the redactor JSON file to clean up commands before storing """
class Redactor(object):

    def __init__(self, path, commands, redact_file=None):
        self.path = path
        self.commands = commands

        """ Open Default Redactor File if not Specified """
        if redact_file:
            self.redact = json.loads(open(redact_file, "r").read())
        else:
            self.redact = json.loads(open(self.path + "/default/default.json", "r").read())

        self.perform_redaction()

    """ Read the JSON File to redact applicable commands """
    def perform_redaction(self):

        for command in self.commands:
            if command.tool in self.redact:
                for arg in range(len(command.arguments)):
                    if command.arguments[arg] in self.redact[command.tool]:
                        command.arguments[arg+1] = "####"




