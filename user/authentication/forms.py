from django import forms
from .models import Student, Message
from django.forms import ModelForm
from django.contrib.auth.models import User

class StudentUpload(ModelForm):
    class Meta:
        model = Student
        fields = ('name', 'owner', 'pdf')

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'message', 'attached_file']
