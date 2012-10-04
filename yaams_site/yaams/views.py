# Create your views here.
from django.http import HttpResponse
from django.conf import settings
from yaams.models import NewsPost, EmailUser
import yaams.yaams_exceptions
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from utils import render_to_response, send_email
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
	news_posts = NewsPost.get_posts()
        
        return render_to_response(request, 'news.html', { 'news_items' : news_posts })

def redirect_to_email(request):
    if not request.POST['email_addr']:
        return redirect(reverse('index'))
    else:
        return redirect(reverse('check_inbox', args=[request.POST['email_addr']]))

def check_inbox(request, email):
	try:
                eu = EmailUser.get_obj(email)
                if not eu:
                    return render_to_response(request, 'error.html', {'error_message' : 'Uh Oh!!!!! eu is None!!!?'})
                if not request.session.get(email + '-auth', False):
                    mb = eu.get_inbox()
                    if not mb:
                        return render_to_response(request,'error.html', {'error_message' : 'Uh - oh Mb is None?!'})
                else:
                    password = request.session.get(email + '-pass', None)
                    mb = eu.get_inbox(password)
                output_dict = { 'messages' : mb.get_latest_messages(mb.get_message_count()), 'email' : email}
                return render_to_response(request, 'listing.html', output_dict)
	except yaams.yaams_exceptions.NoSuchUser:
		return render_to_response(request, 'error.html', {'error_message' : 'Email Address Not Found!'})
        except yaams.yaams_exceptions.PasswordProtected:
            password = request.POST.get('password', None)
            if not password:
                return render_to_response(request, 'password_protected.html', {})
            else:
                if eu.check_password(password):
                    request.session[email + '-auth'] = True
                    request.session[email + '-pass'] = password
                    mb = eu.get_inbox(password)
                    output_dict = { 'messages' : mb.get_latest_messages(mb.get_message_count()), 'email' : email}
                    return render_to_response(request, 'listing.html', output_dict)
                else:
                    return render_to_response(request, 'error.html', { 'error_message' : 'Invalid Password!' })

@csrf_exempt
def check_message_json_api(request, email, msg_id):
    #return HttpResponse('Checking Message in JSON API Format')
    try:
        password = request.POST.get('password', '')
        eu = EmailUser.get_obj(email)
        mb = eu.get_inbox(password)
        msg = mb.get_message(msg_id, True)
        output = HttpResponse(msg);
    except (yaams.yaams_exceptions.NoSuchUser, yaams.yaams_exceptions.NoSuchMessage):
        output = HttpResponse(json.dumps({'Error' : "No Such User"}))
    except yaams.yaams_exceptions.PasswordProtected:
        output = HttpResponse(json.dumps({'Error' : "Password Required"}))
    
    output['Content-Type'] = 'application/json'
    return output

@csrf_exempt
def check_inbox_json_api(request, email):
	try:
                password = request.POST.get('password', '')
                eu = EmailUser.get_obj(email)
		mb = eu.get_inbox(password)
                output = HttpResponse(mb.get_latest_messages(mb.get_message_count(), True))
	except yaams.yaams_exceptions.NoSuchUser:
		output = HttpResponse(json.dumps({'Error' : "No Such User"}))
        except yaams.yaams_exceptions.PasswordProtected:
                output = HttpResponse(json.dumps({'Error' : 'Password Required'}))
                
        output['Content-Type'] = 'application/json'
        return output
    
@csrf_exempt
def send_message_json_api(request):
    source_address = request.POST.get('source_address', None)
    target_address = request.POST.get('target_address', None)
    subject = request.POST.get('subject', None)
    body = request.POST.get('body', None)
    
    if (not source_address) or (not target_address) or (not subject) or (not body):
        return HttpResponse(json.dumps({'Error' : 'Required Field Not Supplied'}))
    else:
        if send_email(settings.SMTP_SETTINGS, source_address, target_address, subject, body):
            return HttpResponse(json.dumps({'Success' : 'Message Successfully Sent!'}))
        else:
            return HttpResponse(json.dumps({'Error' : 'Internal Server Error Sending Message!'}))

def check_message(request, email, msg_id):
	try:
                password = request.session.get(email + '-pass', '')
                msg_dict = { 'msg_user_exists' : True, 'email_address' : email, 'msg_id' : msg_id }
                eu = EmailUser.get_obj(email)
		mb = eu.get_inbox(password)
		msg = mb.get_message(msg_id)
                msg_dict['message'] = msg
                msg_dict['source_address'] = email
                output = render_to_response(request, 'view_message.html', msg_dict)
	except (yaams.yaams_exceptions.NoSuchUser, yaams.yaams_exceptions.NoSuchMessage):
                msg_dict['msg_user_exists'] = False
		output = render_to_response(request, 'view_message.html', msg_dict)
        except yaams.yaams_exceptions.PasswordProtected:
                return render_to_response(request, 'error.html', {'error_message' : 'Email requires password!<br /> Please enter a valid password to access this email.'})
	except Exception as i:
		output = "Unexpected error!<br />%s" % i
	return HttpResponse(output)
    
def protect_email(request):
    view_dict = { 'email_address' : '',
                    'error_msg' : '',
                }
    
    try:
        if request.method == 'GET':
            return render_to_response(request, 'protect_email.html', view_dict)
        elif request.method == 'POST':
            email_address = request.POST.get('email_address', '')
            new_pass = request.POST.get('new_password', '')
            verify_pass = request.POST.get('verify_password', '')
            password = request.POST.get('password', '')
            view_dict['email_address'] = email_address
            if len(email_address) <= 0 or len(new_pass) <= 0 or len(verify_pass) <= 0:
                view_dict['error_msg'] = 'All fields are required excluding password if a password is not already set.'
                return render_to_response(request, 'protect_email.html', view_dict)
            else:
                if verify_pass != new_pass:
                    view_dict['error_msg'] = 'New Password and Verify Password Fields Do Not Match!'
                    return render_to_response(request, 'protect_email.html', view_dict)
                else:
                    try:
                        eu = EmailUser.get_obj(email_address)
                        if eu.has_password():
                            if eu.check_password(password):
                                eu.set_password(new_pass)
                            else:
                                raise yaams.yaams_exceptions.PasswordProtected(email_address)
                                
                        return render_to_response(request, 'base.html', {'content' : 'Password Set On Inbox!'})
                    except yaams.yaams_exceptions.PasswordProtected:
                        view_dict['error_msg'] = 'Password Required on Email or Invalid Password Supplied!'
                        return render_to_response(request, 'protect_email.html', view_dict)
                
    except yaams.yaams_exceptions.NoSuchUser:
        return render_to_response(request, 'error.html', {'error_message' : 'The specified user does not exist!'})
    
def logout(request):
    request.session.clear()
    return redirect(reverse('index'))

def delete_message(request, email_address, msg_id):
    password = request.session.get(email_address + '-pass', '')
    view_dict = {}
    try:
        eu = EmailUser.get_obj(email_address)
        mb = eu.get_inbox(password)
        if mb.delete_message(msg_id):
            view_dict['content'] = 'Message Deleted Successfully!'
        else:
            view_dict['content'] = 'Message Does Not Exist!'
        return render_to_response(request, 'base.html', view_dict)
    except yaams.yaams_exceptions.PasswordProtected:
        view_dict['error_message'] = 'Password Required or Invalid Password Supplied!'
        return render_to_response(request, 'error.html', view_dict)

def send_message(request):
    """NOTE THAT I KNOW THIS DOESN'T SECURE THE SOURCE ADDRESS! THIS IS ANONYMOUS MAIL!"""
    source_address = request.POST.get('source_address', '')
    subject = request.POST.get('subject', '')
    target_address = request.POST.get('target_address', '')
    
    if request.POST.get('body', False):
        send_email(settings.SMTP_SETTINGS, source_address, target_address, subject, request.POST.get('body'))
        return render_to_response(request, 'base.html', { 'content' : 'Message Sent!'})
    else:
        view_dict = {
        
        'source_address' : source_address,
        'target_address' : target_address,
        'subject' : subject
        
        }
        return render_to_response(request, 'send_form.html', view_dict)
