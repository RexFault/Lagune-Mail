from django.shortcuts import render_to_response as render
from django.core.context_processors import csrf
import cgi

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