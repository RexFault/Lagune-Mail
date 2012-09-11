import memcache

def check_inbox(user):
	mc = memcache.Client(['127.0.0.1:11211'], debug=0)
	inbox = mc.get(user)
	if not inbox:
		print "User Does Not Exist in Memcached!"
		return None
	else:
		print 'Data exists! Returned'
		return inbox
