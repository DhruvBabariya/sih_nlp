from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    key = models.CharField(max_length=50)
    document = models.FileField(null=True)
    aspects = models.CharField(max_length=100,null=True)
    
    def __str__(self):
        return self.name

class ProjectResults(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE,null=True)
    positive = models.IntegerField()
    negative = models.IntegerField()
    neutral = models.IntegerField()
    percentages =  models.TextField(max_length=5000)

    def __str__(self):
        return self.project.name

class ContextResults(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE,null=True)
    original_average_rating = models.FloatField()
    predicted_average_rating = models.FloatField()
    num_of_reviews = models.IntegerField(max_length=10)
    aspects_rating = models.TextField(max_length=5000)

    def __str__(self):
        return self.project.name




