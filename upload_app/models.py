from django.db import models


class ImageModel(models.Model):
    image = models.ImageField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image
