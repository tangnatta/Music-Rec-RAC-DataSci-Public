from django import forms
from .models import Voice


class VoiceForm(forms.ModelForm):
    voice = forms.FileField(widget=forms.TextInput(attrs={
        "name": "voice-form",
        "type": "File",
        "class": "form-control",
        "accept": "audio/*",
        "multiple": "False",
    }), label="")

    class Meta:
        model = Voice
        fields = ['voice']
