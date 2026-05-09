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


from django.views.generic import TemplateView, View, FormView
from .models import Page, Section
from .forms import ContactForm

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = Page.objects.select_related('seo').get(name_en='home')
        context['sections'] = Section.objects.filter(page=context['page'])
        return context

class ContactFormView(View):
    """A view to return the contact form snippet via htmx get"""
    def get(self, request, *args, **kwargs):
        if not request.htmx:
            return HttpResponseRedirect('/')
        
        subject = request.GET.get('subject', _('question'))
        form = ContactForm(initial={'subject': subject})
        
        if subject == _('complaint'):
            form.fields['message'].label = _('Complaint Message:')
            btn_text = _('question')
        else:
            btn_text = _('complaint')

        context = {
            'form': form,
            'subject': subject,
            'btn_text': btn_text
        }
        return render(request, 'includes/form_snippet.html', context)

class ContactEmailView(FormView):
    """A view to send an email via the contact form"""
    form_class = ContactForm
    template_name = 'includes/form_snippet.html'

    def form_valid(self, form):
        subject = form.cleaned_data.get('subject')
        name = form.cleaned_data.get('name')
        phone = form.cleaned_data.get('phone')
        from_email = form.cleaned_data.get('email')
        message = form.cleaned_data.get('message')
        to = settings.EMAIL_HOST_USER
        
        is_complaint = (subject == 'complaint')
        subject_label = _('complaint') if is_complaint else _('question')
        
        mail_body = 'email/mail_body.html'
        reply_body = 'email/reply_body.html'

        try:
            # Send Email to Admin
            full_subject = f"{subject_label} form {name}"
            mail = EmailMultiAlternatives(full_subject, from_email, to=[to])
            mail_context = {
                'subject': full_subject, 
                'name': name, 
                'email': from_email, 
                'message': message, 
                'phone': phone
            }
            mail.attach_alternative(render_to_string(mail_body, mail_context), 'text/html')
            
            if self.request.FILES:
                attachment = self.request.FILES['image']
                mail.attach(attachment.name, attachment.read(), attachment.content_type)
            
            mail.send()

            # Send Auto-reply to User
            reply_subject = _('Auto-reply from Tattoo SK Workshop - Thank you for your message')
            reply = EmailMultiAlternatives(reply_subject, from_email=to, to=[from_email])
            reply.attach_alternative(render_to_string(reply_body, {'name': name, 'complaint': is_complaint}), 'text/html')
            reply.send()

            messages.success(self.request, _('Thank you for your message. We will get back to you as soon as possible.'))
        except Exception as e:
            messages.error(self.request, _('There was an error sending your message. Please try again later.'))
            # In production you might want to log 'e'
            
        return redirect(reverse('contact_form'))

    def form_invalid(self, form):
        subject = self.request.POST.get('subject', 'question')
        btn_text = _('question') if subject == 'complaint' else _('complaint')
        
        context = {
            'form': form,
            'subject': subject,
            'btn_text': btn_text
        }
        messages.error(self.request, _('There was an error sending your message. Please check your form and try again.'))
        return self.render_to_response(context)
