from django import forms


class ChatForm(forms.Form):
    message = forms.CharField(label="Your message", max_length=1000)
