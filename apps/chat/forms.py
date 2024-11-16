# chat/forms.py

from django import forms


class QuestionForm(forms.Form):
    question = forms.CharField(label="Ваш вопрос", max_length=500)
