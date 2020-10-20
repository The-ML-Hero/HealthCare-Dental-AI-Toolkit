from django.db import models

# Create your models here.
class CBCT_Model(models.Model):
    CBCT_name = models.CharField(max_length=250)
    CBCT_file = models.FileField(upload_to='images/root_segmentation')
    CBCT_image = models.ImageField()
    date_uploaded_CBCT = models.DateField(auto_now=True)