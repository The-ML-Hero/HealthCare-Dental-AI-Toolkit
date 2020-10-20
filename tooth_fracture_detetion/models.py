from django.db import models

# Create your models here.

class Fracture_Model(models.Model):
    fracture_name = models.CharField(max_length=250)
    fracture_file = models.FileField(upload_to='images/flurosis_Detection')
    fracture_image = models.ImageField()
    date_uploaded_fracture = models.DateField(auto_now=True)