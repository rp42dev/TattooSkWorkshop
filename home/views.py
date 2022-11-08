from django.http import HttpResponse
from django.utils import translation
from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import BadHeaderError
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.utils import translation
import smtplib



    #put your host and port here 

def index(request):
    """A view to return the index page"""

    return render(request, 'home/index.html')


def send_email(request):

    if request.method == 'POST':

        subject = request.POST['subject'].capitalize()
        name = request.POST['name'].capitalize()
        email_from = request.POST['email']
        message = request.POST['message']
        number = request.POST['phone_number']
        my_email = settings.EMAIL_HOST_USER


        if subject == 'Undefined':
            subject = 'Inquiry'

        body = f'''
        Name: {name},
        email: {email_from},
        Phone Nmber: {number}.
        {message}'''

        subjects_lines = {
            'en': 'Autoreply... From Tattoo SK Workshop',
            'nb': 'Automatisk svar.. Fra Tattoo SK Workshop'
        }

        templates = {
            'Inquiry': {
                'en': render_to_string('emails/email_body.txt'),
                'nb': render_to_string('emails/email_body_no.txt')
            },
            'Complaint': {
                'en': render_to_string('emails/email_complaint.txt'),
                'nb': render_to_string('emails/email_complaint_no.txt')
            }
        }

        if name and message and email_from:
            subject_line = subject + ' ' + name
            subject_line2 = subjects_lines[request.LANGUAGE_CODE]
            body2 = templates[subject][request.LANGUAGE_CODE]
            try:
                mail = EmailMessage(subject_line, body, my_email, [my_email])
                mail2 = EmailMessage(subject_line2, body2, my_email, [email_from])
                if request.FILES:
                    file = request.FILES['file']
                    mail.attach(file.name, file.read(), file.content_type)
                mail.send()
                mail2.send()
                if request.LANGUAGE_CODE == "en":
                    messages.success(request, f'Thank you {name} for your message. We will get back tou you as soon as possible')
                else:
                    messages.success(request, f'Takk for {name} meldingen. Vi vil komme tilbake til deg så snart som mulig')
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/')
        else:
            return redirect('/')

        return redirect('/')


