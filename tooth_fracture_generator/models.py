from django.db import models

# Create your models here.
class Document(models.Model):
    document = models.FileField(upload_to='image-regeneration')
    document_image = models.ImageField()
    document_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
