from django.db import models

# Create your models here.

class Flurosis_Model(models.Model):
    flurosis_name = models.CharField(max_length=250)
    flurosis_file = models.FileField(upload_to='images/flurosis_Detection')
    flurosis_image = models.ImageField()
    date_uploaded_flurosis = models.DateField(auto_now=True)