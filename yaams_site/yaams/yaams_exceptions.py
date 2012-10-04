"""Exceptions for the yaams django application"""

class NoSuchUser(Exception):
    def __init__(self, username):
	self.username = username
    def __str__(self):
	return "User " + self.username + " Does Not Exist!"

class NoSuchMessage(Exception):
    def __init__(self, msg_id):
        self.msg_id = str(msg_id)
    def __str__(self):
        return "Message %s does not exist!" % self.msg_id
    
class PasswordProtected(Exception):
    def __init__(self, email_address):
        self.email_address = email_address
    def __str(self):
        return "Inbox for user %s is password protected! Please provide a valid inbox password to continue." % self.email_address
    