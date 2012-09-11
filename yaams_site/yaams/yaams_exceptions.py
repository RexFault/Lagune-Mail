"""Exceptions for the yaams django application"""

class NoSuchUser(Exception):
    def __init__(self, username):
	self.username = username
    def __str__(self):
	return "User " + self.username + " Does Not Exist!"

class NoSuchMessage(Exception):
    def __init__(self, msg_id):
        self.msg_id = str(msg_id)
    def __str__(selfs):
        return "Message %s does not exist!" % self.msg_id