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
    """A view host_email return the index page"""
    page = Page.objects.get(name='home')
    sections = Section.objects.filter(page=page)

    context = {
        'sections': sections,
        'page': page,
    }
    return render(request, 'index.html', context)


def send_email(request):
    subject = request.POST.get('subject', _('question'))
    name = request.POST.get('name', '')
    phone = request.POST.get('phone', '')
    user_email = request.POST.get('from_email', '')
    message = request.POST.get('message', '')
    attachment = request.FILES.get('attachment', '')
    host_email = settings.EMAIL_HOST_USER, ''
    reply_to = user_email

    if subject == _('complaint'):
        complaint = True
    else:
        subject = _('question')
        complaint = False
        

    mail_body = 'email/mail_body.html'
    reply_body = 'email/reply_body.html'

    message_success = _('Thank you for your message. We will get back host_email you as soon as possible.')
    message_error = _('There was an error sending your message. Please check your form and try again.')
    user_subject = 'Tattoo SK workshop - ' + _('Thank you for your message')
    host_subject = 'Tattoo SK workshop - ' + _('New message') + ' - ' + subject + ' - ' + name
  

    if message and user_email and name:
        try:
            mail = EmailMultiAlternatives(user_subject, user_email, host_email,)
            mail.attach_alternative(render_to_string(mail_body, {'subject': subject, 'name': name, 'email': user_email, 'message': message, 'phone': phone}), 'text/html')
            if attachment: mail.attach(attachment.name, attachment.read(),attachment.content_type)
            mail.send()
            reply = EmailMultiAlternatives(host_subject, host_email, user_email)
            reply.attach_alternative(render_to_string(reply_body, {'name': name, 'complaint': complaint,}), 'text/html')
            reply.send()
            messages.success(request, message_success)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, message_error)
        return render(request, 'email/reply_body.html', {'subject': subject, 'name': name, 'email': user_email, 'message': message})
