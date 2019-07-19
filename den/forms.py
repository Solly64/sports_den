# Import django forms and models

from django import forms
from django.utils.html import strip_tags

from .models import Den

class DenForm(forms.ModelForm):
  body = forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={'placeholder': 'Den', 'class': 'form-control'}))

  class Meta:
    model = Den
    exclude = ('user',)
