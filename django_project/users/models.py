from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Create your models here. Don't forget to register new models to admin.py file
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # profile_pics directory will be location for our images uploaded by users
    # MEDIA_URL is set inside the settings.py file - we set up there a base directory media
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):  # this is method that gets run after our model is saved - we are over-riding it
        super().save(*args, **kwargs)
        # if working on a project that requires more efficiency check out other options for resizing img
        # grab the image, resize it and save it to the same directory
        img = Image.open(self.image.path)
        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)
