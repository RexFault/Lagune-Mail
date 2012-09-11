# Create your views here.
from django.http import HttpResponse
from yaams.models import Mailbox, NewsPost
import yaams.yaams_exceptions
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from utils import render_to_response
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
		mb = Mailbox(email)
                output_dict = { 'messages' : mb.get_latest_messages(mb.get_message_count()), 'email' : email}
                return render_to_response(request, 'listing.html', output_dict)
	except yaams.yaams_exceptions.NoSuchUser:
		return render_to_response(request, 'error.html', {'error_message' : 'Email Address Not Found!'})
            
def check_message_json_api(request, email, msg_id):
    #return HttpResponse('Checking Message in JSON API Format')
    try:
        mb = Mailbox(email)
        msg = mb.get_message(msg_id, True)
        output = HttpResponse(msg);
    except (yaams.yaams_exceptions.NoSuchUser, yaams.yaams_exceptions.NoSuchMessage):
        output = HttpResponse(json.dumps({'Error' : "No Such User"}))
    
    output['Content-Type'] = 'application/json'
    return output


def check_inbox_json_api(request, email):
	try:
		mb = Mailbox(email)
                output = HttpResponse(mb.get_latest_messages(mb.get_message_count(), True))
	except yaams.yaams_exceptions.NoSuchUser:
		output = HttpResponse(json.dumps({'Error' : "No Such User"}))
        output['Content-Type'] = 'application/json'
        return output

def check_message(request, email, msg_id):
	try:
                msg_dict = { 'msg_user_exists' : True }
		mb = Mailbox(email)
		msg = mb.get_message(msg_id)
                msg_dict['message'] = msg
                output = render_to_response(request, 'view_message.html', msg_dict)
	except (yaams.yaams_exceptions.NoSuchUser, yaams.yaams_exceptions.NoSuchMessage):
                msg_dict['msg_user_exists'] = False
		output = render_to_response(request, 'view_message.html', msg_dict)
	except Exception as i:
		output = "Unexpected error!<br />%s" % i
	return HttpResponse(output)