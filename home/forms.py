from django import forms
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    subject = forms.CharField(
        widget=forms.HiddenInput(), initial=_('question'), required=False, label='')
    name = forms.CharField(max_length=100, label=_('Name'), required=True)
    email = forms.EmailField(label=_('Email'), required=True)
    phone = forms.CharField(max_length=100, label=_('Phone'), required=False)
    message = forms.CharField(label=_(
        'Message: (image references, black or with color, size and place)'), widget=forms.Textarea(), required=True)
    image = forms.ImageField(label=_('Image'), required=False)
    confirm_age = forms.BooleanField(label=_('Confirm you are over 16'), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['phone'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['message'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['image'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['confirm_age'].widget.attrs.update(
            {'class': 'form-check-input'})
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['subject'] == 'complaint':
            cleaned_data['confirm_age'] = True
        return cleaned_data
    
    
