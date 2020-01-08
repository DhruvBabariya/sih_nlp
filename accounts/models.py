from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CompanyInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    company_name = models.CharField(max_length=24)

    def __str__(self):
        return self.user.username