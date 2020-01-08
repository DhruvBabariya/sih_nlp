from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    key = models.CharField(max_length=50)
    document = models.FileField(upload_to='documents/',null=True)
    
    def __str__(self):
        return self.name
