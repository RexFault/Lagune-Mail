from utils import render_to_response

#The following is a list of dictionaries where each dictionary has 2 keys, question and answer
#where question is the frequently asked question and answer is the answer to that question
#This is static because its much faster and much less likely to change over time than most pages.
faq_questions = [
    
    #{
    #    'question' : '',
    #    'answer' : ''
    #},
    
    { 
        'question' : 'Does your service allow us to recieve emails with attachments?',
        'answer' : """No. Unfortunately while the SMTP daemon will accept emails with attachments only the text
        body of the message will be displayed as storing and forwarding attachments allows our service to be abused greatly."""
    },
    
    {
        'question' : 'Can I have the source code to run a copy on my own server?',
        'answer' : 'While at the current time we do not have the source available we intend to upload the source once we have ironed out any major bugs in the software.'
    },
    
    {
        'question' : 'Can I use POP3 or x protocol to recieve messages via a 3rd party client?',
        'answer' : 'This feature is planned but not yet implemented. Stay tuned.'
    },
    
    {
        'question' : 'I found a bug or error! Where can I report it so that it can be fixed??',
        'answer' : 'You can email Shane personally by sending the message to binary@lagune-software.com and he will do his best to fix it immediately.'
    },
    
    {
        'question': "What does YAAMS stand for?",
        'answer' : "YAAMS stands for Yet Another Anonymous Mailing System. It is the name under which Lagune Mail was developed."
    },
    
]

def show_faq(request):
    return render_to_response(request, 'FAQ.html', {'faqs': faq_questions})