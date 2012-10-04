import smtpd
import asyncore
import memcache

#Change the following list to include the domains you want to allow mail to be sent to
#If a message is sent to the server and the target users domains isn't one of the following domains it will be
#rejected
valid_domains = ['yaams.lagune-software.com', 'gizmo.lagune-software.com', 'gizmo.packetunderground.com']
PU_DBG = True

class PU_SMTPResponses():
	""" A simple class that contains a couple of message responses used in PU_SMTPServer()"""
	user_not_local = "551 User not local; please try " #Append new address
	ok = "250 OK"
	

class PU_SMTPServer(smtpd.SMTPServer):
	#Contains the validated recipients of the message, only valid recipients will recieve the message
	valid_destination_boxes = []

	def process_message(self, peer, mailfrom, rcpttos, data):
		""" Overrides parent classes default implementation of throwing NotImplementedError
		peer is a tuple containing (ipaddr, port) of the client that made the
		socket connection to our smtp port.

		mailfrom is the raw address the client claims the message is coming
		from.
		
		rcpttos is a list of raw addresses the client wishes to deliver the
		message to.
		
		data is a string containing the entire full text of the message,
		headers (if supplied) and all. It has been `de-transparencied'
		according to RFC 821, Section 4.5.2. In other words, a line
		containing a `.' followed by other text has had the leading dot
		removed.
		
		This function should return None, for a normal `250 Ok' response;
		otherwise it returns the desired response string in RFC 821 format.
		"""
		if self.validate_recipients(rcpttos):
			self.store_message(data)
			return PU_SMTPResponses.ok
			
		return PU_SMTPResponses.user_not_local + "gmail.com" #Quick hack, repair this later pl0x
	
	def validate_recipients(self, recipients):
		""" Checks the list of emails for valid users (Users belonging to one of the valid_domains) and 
		stores ONLY the valid recipients in the valid_destination_boxes list for message storage
		
		Returns True if there are ANY valid users otherwise it returns FALSE
		"""
		if (PU_DBG):
			print "validate_recipients()"
		
		valid_destination_boxes = []
		for address in recipients:
			domain_start = address.rfind('@')
			if (PU_DBG):
				print "Domain Start: " + str(domain_start)
				print "Address: " + address
				print "Domain: " + address[domain_start+1:]
			
			if (domain_start == -1):
				continue;
			domain = address[domain_start+1:]
			if (domain in valid_domains):
				valid_destination_boxes.append(address)
		
		self.valid_destination_boxes = valid_destination_boxes
		
		if (len(valid_destination_boxes) > 0):
			return True
		return False
	
	def store_message(self, msg):
		""" Peforms the actual storage of the recieved message in the inboxes of the users listed in valid_destination_boxes list 
		By design since this mailserver doesn't ensure that ALL mail is stored and recieved all the time (This is designed for One-off emails)
		there is no error checking, maybe in the future
		"""
		
		if (PU_DBG):
			print "store_message()"
			print "Target Emails:"
			print self.valid_destination_boxes
			print msg
			
		mc = memcache.Client(['127.0.0.1:11211'], debug=0)
		
		for dest in self.valid_destination_boxes:
			inbox = mc.get(dest)
			if not inbox:
				inbox = [{"Message" : msg, "Read_State" : False, 'Message_ID' : 0}]
			else:
				inbox.append({"Message" : msg, "Read_State" : False, 'Message_ID' : ( (inbox[-1]['Message_ID']) + 1 ) })
			mc.set(dest, inbox)
		
#MAIN
smtp_server = PU_SMTPServer(('0.0.0.0',25), None)
print "YAAMS server started!"
asyncore.loop()
