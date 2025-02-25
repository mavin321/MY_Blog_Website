from django.db import models
from datetime import datetime 

class Post(models.Model):
    title=models.CharField(max_length=200)
    category=models.CharField(max_length=40)
    content = models.TextField()
    date = models.DateTimeField(default=datetime.now, blank=True)
    image = models.CharField(max_length=50)


