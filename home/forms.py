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
    confirm_age = forms.BooleanField(label=_('Privacy Policy'), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.label_class = 'text-light'

        # Use placeholders instead of labels for text/email/textarea inputs
        for field_name in ['name', 'email', 'phone', 'message']:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs['placeholder'] = field.label
                field.label = ""

        # Set dynamic translated label with link for privacy policy
        from django.utils.safestring import mark_safe
        from django.urls import reverse
        from django.utils.translation import gettext as _
        from django.utils.translation import get_language
        try:
            lang = get_language()
            slug = 'personvern' if lang == 'no' else 'privacy-policy'
            url = reverse('page', args=[slug])
            label_text = _('Privacy Policy')
            self.fields['confirm_age'].label = mark_safe(
                f'<a href="{url}" target="_blank" class="text-decoration-underline text-light">{label_text}</a>'
            )
        except Exception:
            pass

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('subject') == 'complaint':
            # If it's a complaint, we don't necessarily need the age check
            # but the field is required, so we just pass it
            pass
        return cleaned_data
    
    
