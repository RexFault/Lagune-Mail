from django.shortcuts import render_to_response as render
from django.core.context_processors import csrf
import cgi
import random
import hmac
import hashlib
import smtplib

def render_to_response(request, template_name, dict):
    """
    A replacement render_to_response function that replaces the one located in django.shortcuts.
    The main addition to this functio is that it now incorporates the CSRF() form field into the output dictionary context.
    """
    dict.update(csrf(request))
    return render(template_name, dict)


def nl2br(str):
    str = str.replace('\r\n', '<br />')
    return str.replace('\n', '<br />')

def escape(str):
    return cgi.escape(str)

#Password Handling Functions
def make_salt(salt_len = 10):
    """
    Makes a random string of salt_len characters in length
    """
    
    password_char_list = []
    
    for i in range(0, salt_len):
        random.seed(None)
        password_char_list.append(chr(random.randrange(33,126)))
    return ''.join(password_char_list)

def make_hash(secret_key, password, salt = ''):
    """
    Creates a salted password hash of the contents of password, if salt is 
    provided than salt is used otherwise a random salt is generated.
    """
    if len(salt) == 0:
        salt = make_salt()
    
    password = password + salt
    
    hm = hmac.new(secret_key, password, hashlib.sha1)
    return hm.hexdigest()+':'+salt

def parse_hash(hash):
    """
    Parses a supplied hash into its individual pieces returning a tuple of hash,salt
    """
    hash, salt = hash.split(':')
    return hash, salt

def check_password(password, hash, secret_key):
    """
    Checks a password against a password Hash, returns True if it matches, False
    otherwise
    """
    phash, salt = parse_hash(hash)
    phash = make_hash(secret_key, password, salt)
    
    if hash == phash:
        return True
    
    return False

def send_email(settings, source, target, subject, message):
    """
    Used to send an email that appears to be from "Source" to "Target" email.
    Returns True on success, False on error.
    
    settings is a dictionary object with members 'SERVER', 'PORT', 'USERNAME' ,'PASSWORD'
    all fields of settings are strings except for PORT which is an integer
    """
    message = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s") % (source, target, subject, message)
    
    try:
        smtp_instance = smtplib.SMTP(settings['SERVER'], settings['PORT'])
        smtp_instance.login(settings['USERNAME'], settings['PASSWORD'])
        smtp_instance.sendmail(source, [target], message)
        smtp_instance.quit()
    except:
        return False
    