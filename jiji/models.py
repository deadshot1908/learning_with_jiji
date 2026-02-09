from django.db import models

# Create your models here.

class Query(models.Model):
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
