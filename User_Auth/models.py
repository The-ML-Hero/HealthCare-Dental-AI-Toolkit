from django.db import models

# Create your models here.

class Verify_F(models.Model):
    verification_code = models.TextField(max_length=30)
