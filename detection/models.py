from django.db import models

# Create your models here.
class postModel(models.Model):
    stream_image_1 = models.ImageField(upload_to="images", null=False, default=None)
    stream_image_2 = models.ImageField(upload_to="images", null=False, default=None)

    def __str__(self):
        return f"{self.stream_image_1}, {self.stream_image_2}"