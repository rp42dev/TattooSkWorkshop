from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage, EmailMultiAlternatives
from django.utils.translation import gettext as _
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponse, HttpResponseRedirect
from .models import Page, Section
from django.contrib import messages
from pytube import *

from .forms import ContactForm


def index(request):
    """A view to return the index page"""
    page = Page.objects.get(name='home')
    sections = Section.objects.filter(page=page)

    context = {
        'sections': sections,
        'page': page,
    }
    return render(request, 'index.html', context)


@require_GET
def contact_form(request):
    """A view to return the contact form snippet vie htmx get"""

    if request.htmx:
        form = ContactForm()
        if request.GET.get('subject') == _('complaint'):
            form.initial['subject'] = _('complaint')
            form.fields['message'].label = _('Complaint Message:')
            btn_text = _('question')
        else:
            form.initial['subject'] = _('question')
            btn_text = _('complaint')

        context = {
            'form': form,
            'subject': form.initial['subject'],
            'btn_text': btn_text
        }

        return render(request, 'includes/form_snippet.html', context)
    else:
        return HttpResponseRedirect('/')


@require_POST
def send_email(request):
    """A view to send an email via the contact form"""
    # return render(request, 'email/reply_body.html', {'name': 'name', 'complaint': True, })

    form = ContactForm(request.POST, request.FILES)

    if form.is_valid():
        subject = request.POST.get('subject', '')
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        from_email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        to = settings.EMAIL_HOST_USER
    else:
        subject = request.POST.get('subject', '')
        btn_text = _('question') if subject == 'complaint' else _('complaint')
        for field in form:
            if field.errors:
                if field.name == 'confirm_age':
                    field.field.widget.attrs.update(
                        {'class': 'form-check-input is-invalid'})
                else:
                    field.field.widget.attrs.update(
                        {'class': 'form-control is-invalid'})
            else:
                field.field.widget.attrs.update(
                    {'class': 'form-control is-valid'})
        context = {
            'form': form,
            'subject': subject,
            'btn_text': btn_text
        }
        messages.error(request, _(
            'There was an error sending your message. Please check your form and try again.'))
        return render(request, 'includes/form_snippet.html', context)

    if subject == 'complaint':
        subject = _('complaint')
        complaint = True
    else:
        subject = _('question')
        complaint = False

    mail_body = 'email/mail_body.html'
    reply_body = 'email/reply_body.html'

    message_success = _(
        'Thank you for your message. We will get back to you as soon as possible.')
    message_error = _(
        'There was an error sending your message. Please check your form and try again.')

    if message and from_email and name:
        try:
            subject = subject + ' ' + 'form' + ' ' + name
            mail = EmailMultiAlternatives(subject, from_email, to=[to])
            mail.attach_alternative(render_to_string(mail_body, {
                                    'subject': subject, 'name': name, 'email': from_email, 'message': message, 'phone': phone}), 'text/html')
            if request.FILES:
                attachment = request.FILES['attachment']
                mail.attach(attachment.name, attachment.read(),
                            attachment.content_type)
            mail.send()
            subject = _(
                'Auto-reply from Tattoo SK Workshop - Thank you for your message')
            reply = EmailMultiAlternatives(
                subject, from_email=to, to=[from_email])
            reply.attach_alternative(render_to_string(
                reply_body, {'name': name, 'complaint': complaint, }), 'text/html')
            reply.send()
            messages.success(request, message_success)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect(reverse('contact_form'))
    else:
        messages.error(request, message_error)
        return redirect(reverse('contact_form'))
