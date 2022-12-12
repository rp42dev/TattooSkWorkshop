from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage, EmailMultiAlternatives
from django.utils.translation import gettext as _
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect
from .models import Page, Section
from django.contrib import messages
from pytube import *
# try:
#     video = YouTube('https: // www.youtube.com/watch?v=XBSEn2pUa84')
#     video.streams.get_highest_resolution().download()
# except:
#     pass


def index(request):
    """A view to return the index page"""
    page = Page.objects.get(name='home')
    sections = Section.objects.filter(page=page)

    context = {
        'sections': sections,
        'page': page,
    }
    return render(request, 'index.html', context)


def send_email(request):
    subject = request.POST.get('subject', '')
    name = request.POST.get('name', '')
    phone = request.POST.get('phone', '')
    from_email = request.POST.get('from_email', '')
    message = request.POST.get('message', '')
    attachment = request.FILES.get('attachment', '')
    to = settings.EMAIL_HOST_USER

    if subject == 'complaint':
        subject = _('Complaint')
        complaint = True
    else:
        subject = _('Question')
        complaint = False
        

    mail_body = 'email/mail_body.html'
    reply_body = 'email/reply_body.html'

    message_success = _('Thank you for your message. We will get back to you as soon as possible.')
    message_error = _('There was an error sending your message. Please check your form and try again.')


    if message and from_email and name:
        try:
            subject = subject + ' ' + _('from Tattoo SK Workshop')
            mail = EmailMultiAlternatives(subject, from_email, to=[to])
            mail.attach_alternative(render_to_string(mail_body, {'subject': subject, 'name': name, 'email': from_email, 'message': message, 'phone': phone}), 'text/html')
            if attachment: mail.attach(attachment.name, attachment.read(),attachment.content_type)
            mail.send()
            subject = _('Auto-reply from Tattoo SK Workshop - Thank you for your message')
            reply = EmailMultiAlternatives(subject, from_email=to, to=[from_email])
            reply.attach_alternative(render_to_string(reply_body, {'name': name, 'complaint': complaint,}), 'text/html')
            reply.send()
            messages.success(request, message_success)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, message_error)
        
        return render(request, 'email/reply_body.html', {'subject': subject, 'name': name, 'email': from_email, 'message': message})
