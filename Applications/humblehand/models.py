from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Volunteer(models.Model):
    PROFESSION_CHOICES = [
        ('STUDENT', 'Student'),
        ('PRIVATE', 'Private Employee'),
        ('GOVERNMENT', 'Government Employee'),
        ('BUSINESS', 'Self Business'),
        ('SOCIAL', 'Social Worker'),
        ('OTHER', 'Other')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    age = models.IntegerField()
    profession = models.CharField(max_length=20, choices=PROFESSION_CHOICES)
    message = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.profession}"



class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"