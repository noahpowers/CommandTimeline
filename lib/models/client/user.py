import re
import getpass
from lib.utils.utiliites import Utility

class User(object):

    def __init__(self):
        self.unique_id = None
        self.username = None
        self.password = None
        self.email_address = None

    def __repr__(self):
        pass

    def password_generator(self, password):
        self.password = Utility.hash_generator(password)

    def create_user(self):

        while True:

            try:
                while True:
                    self.username = input("[!] Username: ")
                    if not self.username:
                        print("[!] Enter Valid Username")
                    else:
                        break

                while True:
                    temporary_password = getpass.getpass("[!] Password: ")

                    if temporary_password:
                        confirm_password = getpass.getpass("[!] Confirm Password: ")

                        if temporary_password != confirm_password:
                            print("[!] Passwords Do Not Match")
                        else:
                            self.password_generator(temporary_password)
                            break
                    else:
                        print("[!] Enter Password!")

                while True:

                    self.email_address = input("[!] Enter Email Address: ")

                    if not self.email_address:
                        print("[*] Enter Valid Email Address")
                    if re.search("@", self.email_address):
                        break
                    else:
                        print("[*] Enter Valid Email Address")

                while True:
                    print("[+] Username: %s" %self.username)
                    print("[+] Email Address: %s" %self.email_address)

                    confirm = input("[!] Validate User Account [ y/(n) ]: ")
                    if confirm.lower() == 'y':
                        self.unique_id = Utility.unique_id_generator(12)
                        break
                break
            except KeyboardInterrupt:
                confirm = input("[!] Restart Creation [ y/(n) ]: ")
                if confirm.lower() == "y":
                    continue
                else:
                    break

    def delete_user(self):
        pass

    def update_user(self):
        pass




