from utils import render_to_response

ABOUT_CONTENT = """

<h1>About Lagune Mail / YAAMS</h1>
<p>
Lagune mail is a anonymous email web service that allows users to receive email via our website
without registering an account and potentially compromising their anonymity. We guarantee that we log nothing
and store nothing. We store all messages in memory meaning that if our server is to be shut down for any reason all messages
are lost.
</p>

<p>
Because of the potential for abuse of this system we do not allow messages containing any type of attachment to be recieved
and forwarded. This service is meant for those who do not want to a separate email account for a new website that could potentially
be flooded by spam. Use this service to register for a website new to you that you are unsure of and later on we recommend if you trust them
then you register with a proper email account. 
</p>

<p>
To use this service simply register an account at the site of your choice and as your email enter <span class='colorize'>&ltwhatever_you_want&gt@yaams.lagune-software.com</span>
Then come to this website and in the check email form enter the same email address you used to register and view your messages! It is that simple.
</p>

"""

def show_about(request):
    return render_to_response(request, 'base.html', { 'content' : ABOUT_CONTENT })