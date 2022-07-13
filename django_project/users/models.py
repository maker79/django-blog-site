from django.db import models
from django.contrib.auth.models import User


# Create your models here. Don't forget to register new models to admin.py file
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # profile_pics directory will be location for our images uploaded by users
    # MEDIA_URL is set inside the settings.py file - we set up there a base directory media
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
