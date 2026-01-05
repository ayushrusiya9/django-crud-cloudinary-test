from django.db import models

from cloudinary_storage.storage import RawMediaCloudinaryStorage, MediaCloudinaryStorage

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/',storage=MediaCloudinaryStorage())
    documents = models.FileField(upload_to='documents/',storage=RawMediaCloudinaryStorage())
    city = models.CharField(max_length=50)

    class Meta:
        db_table = 'Students'

    def __str__(self):
        return self.name