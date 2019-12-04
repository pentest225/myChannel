from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Salon(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_salon')
    nom=models.CharField(max_length=255)
    date_add=models.DateTimeField(auto_now=True)
    date_upd=models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=True)
    
    def __str__(self):
        return self.nom

class Message(models.Model):
    salon=models.ForeignKey(Salon,on_delete=models.CASCADE,related_name='salon_message')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_message')
    message=models.TextField()
    date_add=models.DateTimeField(auto_now=True)
    date_upd=models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=True)
