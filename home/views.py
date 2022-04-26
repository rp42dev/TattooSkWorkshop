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

        name = request.POST['name']
        email_from = request.POST['email']
        message = request.POST['message']
        number = request.POST['phone_number']

        body = f'''
        Name: {name},
        email: {email_from},
        Phone Nmber: {number}.

        {message}'''
        
        if name and message and email_from:
            subject = 'Question from' + name
            my_email = settings.EMAIL_HOST_USER

            subject2 = 'Fra Tattoo SK studio | From Tattoo SK studio'
            
            if request.LANGUAGE_CODE == "en":
                body2 = render_to_string('emails/email_body.txt')
            else:
                body2 = render_to_string('emails/email_body_no.txt')
            try:
                mail = EmailMessage(subject, body, my_email, [my_email])
                mail2 = EmailMessage(subject2, body2, my_email, [email_from])
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


