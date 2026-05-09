from django import forms
from django.utils.translation import gettext_lazy as _


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Hidden

class ContactForm(forms.Form):
    subject = forms.CharField(widget=forms.HiddenInput(), initial=_('question'), required=False)
    name = forms.CharField(max_length=100, label=_('Name'), required=True)
    email = forms.EmailField(label=_('Email'), required=True)
    phone = forms.CharField(max_length=100, label=_('Phone'), required=False)
    message = forms.CharField(
        label=_('Message: (image references, black or with color, size and place)'), 
        widget=forms.Textarea(attrs={'rows': 4}), 
        required=True
    )
    image = forms.ImageField(label=_('Image'), required=False)
    confirm_age = forms.BooleanField(label=_('Confirm you are over 16'), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.label_class = 'text-light'

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('subject') == 'complaint':
            # If it's a complaint, we don't necessarily need the age check
            # but the field is required, so we just pass it
            pass
        return cleaned_data
    
    
