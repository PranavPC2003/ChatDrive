from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0, null=True)
    name = models.CharField(max_length=100, default=None, null=True)
    owner = models.CharField(max_length=100, default=None, null=True)
    pdf = models.FileField(upload_to='pdfs/', null=True)

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        super().delete(*args, **kwargs)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    attached_file = models.FileField(upload_to='message_attachments/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return self.subject
    
    def delete(self, *args, **kwargs):
        if self.attached_file:
            self.attached_file.delete()
        super().delete(*args, **kwargs)

